from django.core.management.base import BaseCommand
from public.ftpmgr import test


class Command(BaseCommand):
    def handle(self, *args, **options):
        #from django_multiversionmgr.settings import FTP_ROOT
        #from multiversionmgr.createversion import CreateVersion
        #from multiversionmgr.models import Software, Version
        #from multiversionmgr.createobserver import CreateObserver

        #version = None
        #softwarepath = ''
        #versionpath = ''
        #if len(args) > 1:
        #    softwarepath = sys.argv[0]
        #    versionpath = sys.argv[1]
        #    version = Version.objects.filter(software__softwarepath = softwarepath, versionpath = versionpath)
        #else:
        #    sw = Software.objects.all()[0]
        #    softwarepath = sw.softwarepath
        #    version = Version.objects.filter(software_id = sw.id)[0]
        #    versionpath = version.versionpath

        #fullpath = os.path.join(FTP_ROOT, softwarepath, versionpath)
        #create = CreateVersion(fullpath)
        #create.setObserver(CreateObserver(FTP_ROOT, version))
        #create.create()
        #for file in create.files:
        #    print file.filepath + '/' + file.filename + ":" + file.md5code
        test()
        return 0
