from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.channels.models import Channel, ChannelGroup, Stream
from apps.m3u.models import M3UAccount
from apps.m3u.tasks import validate_account_streams_task

User = get_user_model()


class StreamValidationTests(TestCase):
    def setUp(self):
        # Disconnect signals to avoid background/periodic tasks executing during setup
        from django.db.models.signals import post_save
        from apps.m3u.signals import refresh_account_on_save, create_or_update_refresh_task
        
        post_save.disconnect(refresh_account_on_save, sender=M3UAccount)
        post_save.disconnect(create_or_update_refresh_task, sender=M3UAccount)

        # Force import url_utils to ensure it is loaded in sys.modules before we monkey-patch it
        from apps.proxy.live_proxy import url_utils

        # Patch Redis lock functions so they don't try to connect to localhost:6379
        self.patch_acquire = patch("apps.m3u.tasks.acquire_task_lock", return_value=True)
        self.patch_release = patch("apps.m3u.tasks.release_task_lock", return_value=True)
        self.patch_acquire.start()
        self.patch_release.start()

        # Monkey-patch validate_stream_url across all url_utils modules in sys.modules
        import sys
        self.original_validates = {}

        def mock_validate(url, **kwargs):
            if "invalid" in url:
                return False, url, 404, "Invalid HTTP status: 404"
            elif "valid" in url:
                return True, url, 200, "Valid (HEAD request)"
            else:
                # Fallback for non-http streams (like UDP) which bypass HTTP validation
                if url.startswith(('udp://', 'rtp://', 'rtsp://')):
                    return True, url, 200, "Non-HTTP protocol (UDP/RTP/RTSP) - validation skipped"
                return False, url, 0, "Unknown"

        for name, module in list(sys.modules.items()):
            if "url_utils" in name and hasattr(module, "validate_stream_url"):
                self.original_validates[name] = module.validate_stream_url
                module.validate_stream_url = mock_validate

        self.user = User.objects.create_user(
            username="tester", password="testpass123"
        )
        self.user.user_level = 10
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.account = M3UAccount.objects.create(
            name="TestProvider",
            server_url="http://example.com/playlist.m3u",
            timeout=10,
            skip_ssl_verification=True,
            proxy_url="http://localhost:8080",
        )
        self.group = ChannelGroup.objects.create(name="Entertainment")

        # 1. Valid stream
        self.stream_valid = Stream.objects.create(
            name="Valid Stream",
            url="http://example.com/valid.m3u8",
            m3u_account=self.account,
            channel_group=self.group,
            is_active=True,
        )
        # 2. Invalid stream (to be marked inactive)
        self.stream_invalid = Stream.objects.create(
            name="Invalid Stream",
            url="http://example.com/invalid.m3u8",
            m3u_account=self.account,
            channel_group=self.group,
            is_active=True,
        )
        # 3. Non-HTTP stream (e.g. UDP)
        self.stream_udp = Stream.objects.create(
            name="UDP Stream",
            url="udp://@239.1.1.1:1234",
            m3u_account=self.account,
            channel_group=self.group,
            is_active=True,
        )

    def tearDown(self):
        # Reconnect signals
        from django.db.models.signals import post_save
        from apps.m3u.signals import refresh_account_on_save, create_or_update_refresh_task
        
        post_save.connect(refresh_account_on_save, sender=M3UAccount)
        post_save.connect(create_or_update_refresh_task, sender=M3UAccount)

        # Restore monkey-patched functions
        import sys
        for name, original_func in self.original_validates.items():
            if name in sys.modules:
                sys.modules[name].validate_stream_url = original_func

        # Stop patches
        self.patch_acquire.stop()
        self.patch_release.stop()

    @patch("apps.m3u.tasks.send_m3u_update")
    def test_validate_account_streams_task_success(self, mock_send_m3u_update):
        # Execute the validation task synchronously
        result = validate_account_streams_task(self.account.id)
        
        # Verify results
        self.stream_valid.refresh_from_db()
        self.stream_invalid.refresh_from_db()
        self.stream_udp.refresh_from_db()

        # The valid stream should remain active
        self.assertTrue(self.stream_valid.is_active)
        self.assertIn("last_validation", self.stream_valid.custom_properties)
        self.assertTrue(self.stream_valid.custom_properties["last_validation"]["is_valid"])
        self.assertEqual(self.stream_valid.custom_properties["last_validation"]["status_code"], 200)

        # The invalid stream should be disabled
        self.assertFalse(self.stream_invalid.is_active)
        self.assertIn("last_validation", self.stream_invalid.custom_properties)
        self.assertFalse(self.stream_invalid.custom_properties["last_validation"]["is_valid"])
        self.assertEqual(self.stream_invalid.custom_properties["last_validation"]["status_code"], 404)

        # The UDP stream should bypass validation and remain active
        self.assertTrue(self.stream_udp.is_active)

        # The task should broadcast progress via WebSockets
        mock_send_m3u_update.assert_any_call(
            self.account.id, "validating_streams", 0, status="validating_streams", message="Validated 0/3 streams"
        )
        mock_send_m3u_update.assert_any_call(
            self.account.id, "validating_streams_done", 100, status="idle", message=result.replace("Validated 3 streams.", "Validation completed: 2 active, 1 inactive streams out of 3 total.")
        )

    @patch("apps.m3u.tasks.validate_account_streams_task.delay")
    def test_api_endpoint_triggers_task(self, mock_delay):
        response = self.client.post(
            f"/api/m3u/accounts/{self.account.id}/validate-streams/"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        mock_delay.assert_called_once_with(self.account.id)
