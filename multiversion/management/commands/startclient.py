from django.core.management.base import BaseCommand

from multiversionclient.clientversionmgr import ClientVersionMgr

class Command(BaseCommand):
    def handle(self, *args, **options):
        mgr = ClientVersionMgr()
        mgr.setRootPath(r'E:\testftp\test\1.00')
        mgr.setVersionID(1)
        mgr.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            mgr.stop()
        return 0
