import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django_multiversionmgr.settings import FTP_ROOT
        from multiversion.createversion import CreateVersion
        from multiversion.models import Software, Version
        from multiversion.createobserver import CreateObserver

        version = None
        softwarepath = ''
        versionpath = ''
        if len(args) > 1:
            softwarepath = sys.argv[0]
            versionpath = sys.argv[1]
            version = Version.objects.filter(software__softwarepath = softwarepath, versionpath = versionpath)
        else:
            sw = Software.objects.all()[0]
            softwarepath = sw.softwarepath
            version = Version.objects.filter(software_id = sw.id)[0]
            versionpath = version.versionpath

        fullpath = os.path.join(FTP_ROOT, softwarepath, versionpath)
        create = CreateVersion(fullpath)
        create.setObserver(CreateObserver(FTP_ROOT, version))
        create.create()
        for file in create.files:
            print file.filepath + '/' + file.filename + ":" + file.md5code
        return 0
