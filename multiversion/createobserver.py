import os
from datetime import datetime
from xml.dom import minidom
from xml.etree.ElementTree import (Element, SubElement, tostring, )

from django.core.exceptions import ObjectDoesNotExist

from models import FileInfo, CreateVersion
from public.createmd5code import getfilemd5code


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class CreateObserver:
    def __init__(self, root, version):
        self.root = root
        self.changed = False
        self.version = version
        self.current = ""
        self.percent = 0
        try:
            self.createversion = CreateVersion.objects.get(version=version)
        except ObjectDoesNotExist:
            self.createversion = CreateVersion.objects.create(version=version)

    def settotal(self, value):
        self.changed = True
        self.version.totalfile = value
        self.version.save()

    def setcurrent(self, value):
        self.changed = True
        self.createversion.currentfile = value
        self.createversion.save()

    def setpercent(self, value):
        self.changed = True
        self.createversion.createpercent = value
        self.createversion.save()

    def createmd5code(self, directory, files):
        total = len(files)
        self.settotal(total)
        self.setcurrent('')
        self.setpercent(0)

        cur = 0
        for f in files:
            self.setcurrent(f.filepathname)
            fullname = os.path.join(directory, f.filepathname)
            f.md5code = getfilemd5code(fullname)
            cur += 1
            self.setpercent((cur/total) * 100)

        self.setcurrent('')
        self.compltated(files)

    def createdeployfile(self, files):
        top = Element('MultiVersion')
        child = SubElement(top, 'Files')
        for f in files:
            fileelemnet = SubElement(child, 'File')
            fileelemnet.set('ID', str(f.id))
            fileelemnet.set('Path', f.filepath)
            fileelemnet.set('Name', f.filename)
            fileelemnet.set('Code', f.md5code)

        text = prettify(top)
        name = self.root + self.version.path + 'deploy.xml'
        with open(name, 'wt') as xmlfile:
            xmlfile.write(text)
        self.version.md5code = getfilemd5code(name)
        self.version.time = datetime.now()
        self.version.save()

    def compltated(self, files):
        deletes = []
        allfile = FileInfo.objects.filter(version=self.version)
        for f in allfile:
            find = False
            for f1 in files:
                if f.filepathname == f1.filepathname:
                    find = True
                    break
            if find:
                if f.md5code != f1.md5code:
                    f.md5code = f1.md5code
                    f.save()
            else:
                deletes.append(f)

        for d in deletes:
            d.delete()

        allfile = FileInfo.objects.filter(version=self.version)
        for f1 in files:
            find = False
            for f in allfile:
                if f.filepathname == f1.filepathname:
                    find = True
                    break
            if not find:
                FileInfo.objects.create(version=self.version,
                                        filepath=f1.filepath,
                                        filename=f1.filename,
                                        md5code=f1.md5code)
        self.changed = False

        allfile = FileInfo.objects.filter(version=self.version)
        self.createdeployfile(allfile)
