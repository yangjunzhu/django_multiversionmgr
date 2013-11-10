#coding=utf-8
import os
import time
import socket
from ftplib import FTP
from xml.etree import ElementTree

from public.createmd5code import getfilemd5code
from multiversion.models import FileInfo


class LoadFileHandle:
    def __init__(self, f):
        self.len = 0
        self.file = f

    def handle(self, data):
        self.file.write(data)
        self.len += len(data)
        print self.len


class MYFTP:
    def __init__(self, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.port = port
        self.ftp = FTP()
        self.file_list = []
        # self.ftp.set_debuglevel(2)

    def __del__(self):
        self.ftp.close()
        # self.ftp.set_debuglevel(0)

    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print u'开始连接到 %s' % self.hostaddr
            ftp.connect(self.hostaddr, self.port)
            print u'成功连接到 %s' % self.hostaddr
            print u'开始登录到 %s' % self.hostaddr
            ftp.login(self.username, self.password)
            print u'成功登录到 %s' % self.hostaddr
            debug_print(ftp.getwelcome())
        except Exception:
            print u'连接或登录失败'
        try:
            ftp.cwd(self.remotedir)
        except Exception:
            print u'切换目录失败'

    def is_same_size(self, localfile, remotefile):
        try:
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        debug_print('localfile_size:%d  remotefile_size:%d' % (localfile_size, remotefile_size), )
        if remotefile_size == localfile_size:
            return 1
        else:
            return 0

    def download_file(self, localfile, remotefile):
        if self.is_same_size(localfile, remotefile):
            debug_print(u'%s 文件大小相同，无需下载' % localfile)
            return
        else:
            debug_print(u'>>>>>>>>>>>>下载文件 %s ... ...' % localfile)
            #return
        #file_handler = open(localfile, 'wb')
        #self.ftp.retrbinary(u'RETR %s'%(remotefile), file_handler.write)
        file_handler = open(localfile, 'wb')
        f = LoadFileHandle(file_handler)
        self.ftp.retrbinary(u'RETR %s' % remotefile, f.handle)
        file_handler.close()

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print(u'目录%s不存在，继续...' % remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print(u'切换至目录 %s' % self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        #print(remotenames)
        #return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            if filetype == 'd':
                self.download_files(local, filename)
            elif filetype == '-':
                self.download_file(local, filename)
        self.ftp.cwd('..')
        debug_print(u'返回上层目录 %s' % self.ftp.pwd())

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
            debug_print(u'跳过[相等]: %s' % localfile)
            return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' % remotefile, file_handler)
        file_handler.close()
        debug_print(u'已传送: %s' % localfile)

    def upload_files(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):
            return
        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print(u'目录已存在 %s' % item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')

    def get_file_list(self, line):
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_filename(self, line):
        pos = line.rfind(':')
        while line[pos] != ' ':
            pos += 1
        while line[pos] == ' ':
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

    def downloadfile(self, name, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print(u'目录%s不存在，继续...' % remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print(u'切换至目录 %s' % self.ftp.pwd())

        localfile = os.path.join(localdir, name)
        print localfile
        with open(localfile, 'wb') as f1:
            f = LoadFileHandle(f1)
            self.ftp.retrbinary(u'RETR %s' % name, f.handle)

    def __getattr__(self, attr):
        return getattr(self.ftp, attr)

    def downloadversion(self, md5code, localdir='./', remotedir='./'):
        deployfile = localdir + 'deploy.xml'
        code = getfilemd5code(deployfile)
        if code != md5code:
            self.downloadfile('deploy.xml', localdir, remotedir)

        files = []
        with open(deployfile, 'rt') as file:
            tree = ElementTree.parse(file)
        for node in tree.iter(r'File'):
            f = FileInfo()
            f.id = node.attrib.get('ID')
            f.filepath = node.attrib.get('Path')
            f.filename = node.attrib.get('Name')
            f.md5code = node.attrib.get('Code')
            files.append(f)

        downloads = []
        for f in files:
            code = getfilemd5code(localdir + f.filepathname)
            if code != f.md5code:
                downloads.append(f)

        for f in downloads:
            self.downloadfile(f.filename, localdir + f.filepath, remotedir + f.filepath)


def debug_print(s):
    print s


def test():
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    # 配置如下变量
    hostaddr = '192.168.1.2' # ftp地址
    username = '' # 用户名
    password = '' # 密码
    port = 21   # 端口号
    rootdir_local = 'E:/testftp' # 本地目录
    rootdir_remote = '/test'          # 远程目录

    f = MYFTP(hostaddr, username, password, rootdir_remote, port)
    f.login()
    #f.download_files(rootdir_local, rootdir_remote)
    f.downloadversion('ba7ae44652e75159cb9861ff1b3d1e7c', 'E:/testftp/test/1.00/', '/test/1.00/')
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    logstr = u"%s 成功执行了备份\n" % datenow
    debug_print(logstr)


if __name__ == '__main__':
    test()
