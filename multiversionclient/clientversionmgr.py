import socket
import os
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from public.createmd5code import getFileMD5Code
from public.watchdir import WatchDir

from multiversion.models import FileInfo, Version, Node

class ClientVersionMgr(object):
    '''管理本地软件版本'''
    def __init__(self):
        self.rootPath = ''
        self.node = None
        self.version = None
        self.watch = None

        try:
            hostname, aliases, addresses = socket.gethostbyname_ex(socket.gethostname())
            for address in addresses:
                try:
                    self.node = Node.objects.get(ip = address)
                    break
                except MultipleObjectsReturned:
                    print "have MultipleObjectsReturned."
                except ObjectDoesNotExist:
                    print "Either the entry or blog doesn't exist."

            if not self.node:
                print "self.node = None"
        except socket.error as msg:
            print 'ERROR:', msg

    def setRootPath(self, path):
        '''设置本地软件版本根目录'''
        self.rootPath = path

    def setVersionID(self, id):
        '''设置本地软件版本ID'''
        try:
            self.version = Version.objects.get(id)
        except MultipleObjectsReturned:
            print "self.version have MultipleObjectsReturned (id = %d)." %(id,)
        except ObjectDoesNotExist:
            print "self.version doesn't exist (id = %d)." % (id,)

    def startWatch(self):
        '''开始监视本地部署文件'''
        self.watch = WatchDir(self.rootPath, self)
        self.watch.start()

    def stopWatch(self):
        '''停止监视本地部署文件'''
        if self.watch:
            self.watch.stop()

    def CreateFileStatus(self, file):
        '''生成文件部署状态'''
        if not file:
            return

        filename = os.path.join(self.rootPath, file.filepathname)
        code = getFileMD5Code(filename)
        if code == file.md5code:
            ErrorVersionFile.objects.filter(node_id = self.node.id, file_id = file.id).delete()
        else:
            obj, created = ErrorVersionFile.objects.get_or_create(node_id = self.node.id, file_id = file.id)
            obj.time = datetime.now()

    def changeFile(self, filenmae):
        '''本地文件状态发生变化'''
        self.changeFiles([filenmae])

    def changeFiles(self, files):
        '''本地多个文件状态发生变化'''
        for filename in files:
            try:
                file = FileInfo.objects.get(filepathname = filename)
                self.CreateFileStatus(file)
            except MultipleObjectsReturned:
                print "have MultipleObjectsReturned."
            except ObjectDoesNotExist:
                print "Either the entry or blog doesn't exist."

    def changeDir(self, path):
        '''本地文件目录状态发生变化'''
        self.changeDirs([path])

    def changeDirs(self, dirs):
        '''本地多个文件目录状态发生变化'''
        for dir in dirs:
            try:
                #file = FileInfo.objects.get(filepathname = pathname)
                #self.CreateFileStatus(file)
                pass
            except MultipleObjectsReturned:
                print "have MultipleObjectsReturned."
            except ObjectDoesNotExist:
                print "Either the entry or blog doesn't exist."


if __name__ == "__main__":
    mgr = ClientVersionMgr('./')
    mgr.setRootPath(r'E:\testftp\test\1.00')
    mgr.setVersionID(1)
    mgr.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mgr.stop()


