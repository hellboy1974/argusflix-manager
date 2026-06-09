from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.m3u.models import M3UAccount
from apps.channels.models import (
    Channel, ChannelGroup, Stream, ChannelStream, ChannelGroupM3UAccount
)
from apps.output.views import generate_m3u

User = get_user_model()


class ChannelGroupVisibilityTests(TestCase):
    def setUp(self):
        # Create test admin user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.user.user_level = 10
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create active and inactive accounts
        self.active_account = M3UAccount.objects.create(
            name="Active Account",
            server_url="http://active.com/m3u",
            is_active=True
        )

        # Create groups
        self.enabled_group = ChannelGroup.objects.create(name="Enabled Group")
        self.disabled_group = ChannelGroup.objects.create(name="Disabled Group")
        self.custom_group = ChannelGroup.objects.create(name="Custom Group")

        # Create relations (ChannelGroupM3UAccount)
        self.rel_enabled = ChannelGroupM3UAccount.objects.create(
            m3u_account=self.active_account,
            channel_group=self.enabled_group,
            enabled=True
        )
        self.rel_disabled = ChannelGroupM3UAccount.objects.create(
            m3u_account=self.active_account,
            channel_group=self.disabled_group,
            enabled=False
        )

        # Create channels
        self.channel_enabled = Channel.objects.create(
            channel_number=1.0,
            name="Channel Enabled",
            channel_group=self.enabled_group
        )
        self.channel_disabled = Channel.objects.create(
            channel_number=2.0,
            name="Channel Disabled",
            channel_group=self.disabled_group
        )
        self.channel_custom = Channel.objects.create(
            channel_number=3.0,
            name="Channel Custom",
            channel_group=self.custom_group
        )

        # Create streams
        self.stream_enabled = Stream.objects.create(
            name="Stream Enabled",
            url="http://stream.com/1",
            m3u_account=self.active_account,
            channel_group=self.enabled_group,
            is_active=True
        )
        self.stream_disabled = Stream.objects.create(
            name="Stream Disabled",
            url="http://stream.com/2",
            m3u_account=self.active_account,
            channel_group=self.disabled_group,
            is_active=True
        )
        self.stream_custom = Stream.objects.create(
            name="Stream Custom",
            url="http://stream.com/3",
            is_custom=True,
            is_active=True
        )

        # Link channels and streams
        ChannelStream.objects.create(channel=self.channel_enabled, stream=self.stream_enabled, order=1)
        ChannelStream.objects.create(channel=self.channel_disabled, stream=self.stream_disabled, order=1)
        ChannelStream.objects.create(channel=self.channel_custom, stream=self.stream_custom, order=1)

    def test_get_active_streams_filtering(self):
        """Channel.get_active_streams() should exclude streams belonging to disabled channel groups, but keep custom streams."""
        # 1. Enabled group stream -> should be active
        active_streams_1 = self.channel_enabled.get_active_streams()
        self.assertIn(self.stream_enabled, active_streams_1)

        # 2. Disabled group stream -> should NOT be active
        active_streams_2 = self.channel_disabled.get_active_streams()
        self.assertNotIn(self.stream_disabled, active_streams_2)

        # 3. Custom stream (no M3U account/group relation) -> should always be active
        active_streams_3 = self.channel_custom.get_active_streams()
        self.assertIn(self.stream_custom, active_streams_3)

    def test_channel_api_visibility(self):
        """ChannelViewSet should hide channels with no active streams when filtered by visibility_filter=active."""
        response = self.client.get("/api/channels/channels/?visibility_filter=active")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        channel_ids = [c["id"] for c in response.data]
        self.assertIn(self.channel_enabled.id, channel_ids)
        self.assertIn(self.channel_custom.id, channel_ids)
        self.assertNotIn(self.channel_disabled.id, channel_ids)

    def test_playlist_output_visibility(self):
        """generate_m3u should respect channel group visibility and skip channels with no active streams."""
        from django.http import QueryDict
        # Create a mock request object
        class DummyRequest:
            method = "GET"
            GET = QueryDict('')
            META = {}

        request = DummyRequest()
        response = generate_m3u(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        self.assertIn("Channel Enabled", content)
        self.assertIn("Channel Custom", content)
        self.assertNotIn("Channel Disabled", content)
