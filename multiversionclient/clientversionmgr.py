#coding=utf-8
import socket
import os
from datetime import datetime, time

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from public.createmd5code import getfilemd5code
from public.watchdir import WatchDir

from multiversion.models import *


class ClientVersionMgr(object):
    """管理本地软件版本"""

    def __init__(self):
        self.rootpath = ''
        self.node = None
        self.version = None
        self.watch = None

        try:
            hostname, aliases, addresses = socket.gethostbyname_ex(socket.gethostname())
            for address in addresses:
                try:
                    self.node = Node.objects.get(ip=address)
                    break
                except MultipleObjectsReturned:
                    print "have MultipleObjectsReturned."
                except ObjectDoesNotExist:
                    print "Either the entry or blog doesn't exist."

            if not self.node:
                print "self.node = None"
        except socket.error as msg:
            print 'ERROR:', msg

    def setrootpath(self, path):
        """设置本地软件版本根目录"""
        self.rootpath = path

    def setversionid(self, versionid):
        """设置本地软件版本ID"""
        try:
            self.version = Version.objects.get(versionid)
        except MultipleObjectsReturned:
            print "self.version have MultipleObjectsReturned (id = %d)." % (versionid,)
        except ObjectDoesNotExist:
            print "self.version doesn't exist (id = %d)." % (versionid,)

    def startwatch(self):
        """开始监视本地部署文件"""
        self.watch = WatchDir(self.rootpath, self)
        self.watch.start()

    def stopwatch(self):
        """停止监视本地部署文件"""
        if self.watch:
            self.watch.stop()

    def createfilestatus(self, f):
        """生成文件部署状态
        @param f:
        """
        if not f:
            return

        filename = os.path.join(self.rootpath, f.filepathname)
        code = getfilemd5code(filename)
        if code == f.md5code:
            ErrorVersionFile.objects.filter(node_id=self.node.id, file_id=f.id).delete()
        else:
            obj, created = ErrorVersionFile.objects.get_or_create(node_id=self.node.id, file_id=f.id)
            obj.time = datetime.now()

    def changefile(self, filenmae):
        """本地文件状态发生变化
        @param filenmae:
        """
        self.changefiles([filenmae])

    def changefiles(self, files):
        """本地多个文件状态发生变化
        @param files:
        """
        for filename in files:
            try:
                f = FileInfo.objects.get(filepathname=filename)
                self.createfilestatus(f)
            except MultipleObjectsReturned:
                print "have MultipleObjectsReturned."
            except ObjectDoesNotExist:
                print "Either the entry or blog doesn't exist."

    def changedir(self, path):
        """本地文件目录状态发生变化
        @param path:
        """
        self.changedirs([path])

    def changedirs(self, dirs):
        """本地多个文件目录状态发生变化
        @param dirs:
        """
        for d in dirs:
            try:
                #file = FileInfo.objects.get(filepathname = pathname)
                #self.CreateFileStatus(file)
                pass
            except MultipleObjectsReturned:
                print "have MultipleObjectsReturned."
            except ObjectDoesNotExist:
                print "Either the entry or blog doesn't exist."


if __name__ == "__main__":
    mgr = ClientVersionMgr()
    mgr.setrootpath('./')
    mgr.setrootpath(r'E:\testftp\test\1.00')
    mgr.setversionid(1)
    mgr.startwatch()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mgr.stopwatch()
