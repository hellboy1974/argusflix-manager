import logging
import time
from datetime import datetime
from django.utils import timezone
from celery import shared_task
from .models import StalkerPortalScan, StalkerPortalScanResult
from core.stalker_mac_gen import MacGenerator
from core.stalker import StalkerClient
from core.websockets import send_websocket_update

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def run_stalker_scan_task(self, scan_id):
    try:
        scan = StalkerPortalScan.objects.get(id=scan_id)
    except StalkerPortalScan.DoesNotExist:
        logger.error(f"Scan {scan_id} not found.")
        return

    scan.status = StalkerPortalScan.Status.RUNNING
    scan.worker_task_id = self.request.id
    scan.save()

    # Determine MACs to test
    macs = []
    if scan.scan_type == StalkerPortalScan.ScanType.RANDOM:
        prefix = scan.mac_prefix or '00:1A:79'
        count = scan.macs_to_test or 100
        macs = MacGenerator.generate_random(prefix, count)
    elif scan.scan_type == StalkerPortalScan.ScanType.SEQUENTIAL:
        macs = MacGenerator.generate_sequential(scan.mac_range_start, scan.mac_range_end)
    elif scan.scan_type == StalkerPortalScan.ScanType.IMPORT:
        macs = MacGenerator.parse_imported_macs(scan.imported_macs or "")

    scan.macs_to_test = len(macs)
    scan.save()

    send_websocket_update("stalker_scan_progress", {
        "scan_id": scan.id,
        "status": scan.status,
        "macs_to_test": scan.macs_to_test,
        "macs_tested": 0,
        "macs_found": 0,
    })

    rate_limit_seconds = scan.rate_limit / 1000.0 if scan.rate_limit else 0.33

    client = StalkerClient(scan.portal_url)

    for i, mac in enumerate(macs):
        # Check if cancelled
        scan.refresh_from_db()
        if scan.status == StalkerPortalScan.Status.CANCELLED:
            logger.info(f"Scan {scan.id} cancelled by user.")
            break

        client.mac_address = mac
        
        # Test MAC
        try:
            # First handshake
            token = client.handshake()
            if token:
                # Get profile
                profile = client.get_profile()
                if profile and profile.get('status') != 0:
                    # Found a working MAC!
                    StalkerPortalScanResult.objects.create(
                        scan=scan,
                        portal_url=scan.portal_url,
                        mac_address=mac,
                        status=StalkerPortalScanResult.Status.PENDING,
                        raw_profile=profile
                    )
                    scan.macs_found += 1
        except Exception as e:
            logger.debug(f"MAC {mac} failed: {e}")
            pass

        scan.macs_tested += 1
        
        # Update progress every 5 tests or on found
        if i % 5 == 0 or scan.macs_found > 0:
            scan.save()
            send_websocket_update("stalker_scan_progress", {
                "scan_id": scan.id,
                "status": scan.status,
                "macs_to_test": scan.macs_to_test,
                "macs_tested": scan.macs_tested,
                "macs_found": scan.macs_found,
            })

        # Rate Limiting
        time.sleep(rate_limit_seconds)

    if scan.status != StalkerPortalScan.Status.CANCELLED:
        scan.status = StalkerPortalScan.Status.COMPLETED
        scan.completed_at = timezone.now()
    
    scan.save()

    send_websocket_update("stalker_scan_progress", {
        "scan_id": scan.id,
        "status": scan.status,
        "macs_to_test": scan.macs_to_test,
        "macs_tested": scan.macs_tested,
        "macs_found": scan.macs_found,
    })
    
    logger.info(f"Scan {scan.id} finished. Tested: {scan.macs_tested}, Found: {scan.macs_found}")
