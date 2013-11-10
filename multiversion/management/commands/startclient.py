import time
from django.core.management.base import BaseCommand

from multiversionclient.clientversionmgr import ClientVersionMgr


class Command(BaseCommand):
    def handle(self, *args, **options):
        mgr = ClientVersionMgr()
        mgr.setrootpath(r'E:\testftp\test\1.00')
        mgr.setversionid(1)
        mgr.startwatch()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            mgr.stopwatch()
        return 0
