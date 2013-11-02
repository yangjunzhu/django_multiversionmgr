import os
from datetime import datetime
from xml.dom import minidom
from xml.etree.ElementTree import (ElementTree, Element, SubElement, tostring, )

from django.core.exceptions import ObjectDoesNotExist

from models import Version, FileInfo, CreateVersion
from public.createmd5code import getFileMD5Code

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

    def setTotal(self, value):
        self.changed = True
        self.version.totalfile = value
        self.version.save()

    def setCurrent(self, value):
        self.changed = True
        self.createversion.currentfile = value
        self.createversion.save()

    def setPercent(self, value):
        self.changed = True
        self.createversion.createpercent = value
        self.createversion.save()

    def createmd5Code(self, directory, files):
        total = len(files)
        self.setTotal(total)
        self.setCurrent('')
        self.setPercent(0)

        cur = 0
        for file in files:
            self.setCurrent(file.filepathname)
            fullname = os.path.join(directory, file.filepathname)
            file.md5code = getFileMD5Code(fullname)
            cur += 1
            self.setPercent((cur/total) * 100)

        self.setCurrent('')
        self.compltated(files)

    def createDeployFile(self, files):
        top = Element('MultiVersion')
        child = SubElement(top, 'Files')
        for f in files:
            file = SubElement(child, 'File')
            file.set('ID', str(f.id))
            file.set('Path', f.filepath)
            file.set('Name', f.filename)
            file.set('Code', f.md5code)

        text = prettify(top)
        name = self.root + self.version.path + 'deploy.xml'
        with open(name, 'wt') as xmlfile:
            xmlfile.write(text)
        self.version.md5code = getFileMD5Code(name)
        self.version.time = datetime.now()
        self.version.save()


    def compltated(self, files):
        deletes = []
        allfile = FileInfo.objects.filter(version=self.version)
        for all in allfile:
            bfind = False
            for file in files:
                if all.filepathname == file.filepathname:
                    bfind = True
                    break
            if bfind:
                if all.md5code != file.md5code:
                    all.md5code = file.md5code
                    all.save()
            else:
                deletes.append(all)

        for d in deletes:
            d.delete()

        adds = []
        allfile = FileInfo.objects.filter(version=self.version)
        for file in files:
            bfind = False
            for all in allfile:
                if all.filepathname == file.filepathname:
                    bfind = True
                    break
            if not bfind:
                FileInfo.objects.create(version = self.version,
                                        filepath = file.filepath,
                                        filename = file.filename,
                                        md5code = file.md5code)
        self.changed = False

        allfile = FileInfo.objects.filter(version=self.version)
        self.createDeployFile(allfile)





