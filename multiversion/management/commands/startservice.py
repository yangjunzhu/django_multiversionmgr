import os
import sys
import logging

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from multiversionmgr.models import VersionMgr
        return VersionMgr.objects.startService(*args)
