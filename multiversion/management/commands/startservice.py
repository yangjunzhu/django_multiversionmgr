from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from multiversionmgr.models import VersionMgr
        return VersionMgr.objects.startservice(*args)
