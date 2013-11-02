from os.path import join

from django.db import models

from public.multicastthreaded import startMulticastThread

class FtpInfo(models.Model):
    '''FTP服务器信息'''
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    ip = models.IPAddressField('IP地址')
    port = models.PositiveSmallIntegerField('端口', default=21)
    anonymous = models.BooleanField('匿名', default=True)
    user = models.CharField('用户名', max_length=50, blank=True, null=True)
    password = models.CharField('密码', max_length=50, blank=True, null=True)

    def __unicode__(self):
        if self.descript:
            return self.descript
        return ":".join(self.ip, self.port)

class ServiceInfo(models.Model):
    '''务器网络信息'''
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    sendip = models.IPAddressField('发送组播地址')
    sendport = models.PositiveSmallIntegerField('发送端口', default=5000)
    revip = models.IPAddressField('接收组播地址')
    revport = models.PositiveSmallIntegerField('接收端口', default=5001)
    ttl = models.PositiveSmallIntegerField('TTL', default=1)

    def __unicode__(self):
        if self.descript:
            return self.descript
        return ":".join(self.sendip, self.sendport)

class Node(models.Model):
    '''节点信息'''
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    ip = models.IPAddressField('IP地址')
    lasttime = models.DateTimeField('最新时间', auto_now=True)

    def __unicode__(self):
        if self.descript:
            return self.descript
        return self.ip

class NodeGroup(models.Model):
    '''节点管理组'''
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    nodes = models.ManyToManyField(Node, verbose_name='节点')

    def __unicode__(self):
        if self.descript:
            return self.descript
        return self.ip

class Software(models.Model):
    '''软件信息'''
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    softwarepath = models.CharField('软件目录', max_length=100)

    def __unicode__(self):
        if self.descript:
            return self.descript
        return self.softwarepath

class Version(models.Model):
    '''版本信息'''
    software = models.ForeignKey(Software, verbose_name='软件')
    descript = models.CharField('描述', max_length=100, blank=True, null=True)
    versionpath = models.CharField('版本目录', max_length=100)
    totalfile = models.IntegerField('文件个数', default=0, editable = False)
    md5code = models.CharField('校验码', max_length=64, editable = False)
    createtime = models.DateTimeField('打包时间', auto_now=True)

    def __unicode__(self):
        if self.descript:
            return self.descript
        return self.versionpath

    def _path(self):
        return join(self.software.softwarepath, self.versionpath)

    path = property(_path)

class FileInfo(models.Model):
    '''文件信息'''
    version = models.ForeignKey(Version, verbose_name='版本')
    filepath = models.CharField('文件目录', max_length=100, blank=True, null=True)
    filename = models.CharField('文件名称', max_length=40)
    md5code = models.CharField('校验码', max_length=64, editable = False)

    def __unicode__(self):
        return self.filename

    def _filepathname(self):
        return join(self.filepath, self.filename)

    def _filefullpathname(self):
        return join(self.version.path, self.filepathname)

    filepathname = property(_filepathname)
    filefullpathname = property(_filefullpathname)

class VersionManager(models.Manager):
    '''版本信息管理器'''
    def __init__(self):
        super(VersionManager, self).__init__()

    def startService(self, *args):
        service = ServiceInfo.objects.all()[0]
        startMulticastThread(service.revip, service.revport, service.ttl)

class VersionMgr(models.Model):
    '''版本管理信息'''
    node = models.ForeignKey(Node, verbose_name='节点')
    version = models.ForeignKey(Version, verbose_name='版本')
    deploypercent = models.DecimalField('部署百分比',max_digits=5, decimal_places=2, default=0, editable = False)
    currentfile = models.ForeignKey(FileInfo, verbose_name='当前下载文件', blank=True, null=True, editable = False)
    filepercent = models.DecimalField('文件下载百分比',max_digits=5, decimal_places=2, default=0, editable = False)
    nodecode = models.CharField('节点校验码', max_length=64, blank=True, null=True, editable = False)
    nodestatus = models.SmallIntegerField('节点校验结果', default=0, editable = False)
    time = models.DateTimeField('部署时间', null=True, editable = False)

    def __unicode__(self):
        return self.node.__unicode__() + '::' + self.version.__unicode__()

    def _status(self):
        if 0 != self.nodestatus:
            return self.nodestatus
        if self.nodecode != self.version.md5code:
            return -3
        return 0

    objects = VersionManager()
    status = property(_status)

class CreateVersion(models.Model):
    '''生成版本信息'''
    version = models.ForeignKey(Version, verbose_name='版本')
    currentfile = models.CharField('当前文件', max_length=200, blank=True, null=True, editable = False)
    createpercent = models.DecimalField('生成百分比',max_digits=5, decimal_places=2, default=0, editable = False)

    def __unicode__(self):
        return self.version.__unicode__()

class ErrorVersionFile(models.Model):
    '''错误版本文件信息'''
    node = models.ForeignKey(Node, verbose_name='节点')
    file = models.ForeignKey(FileInfo, verbose_name='文件')
    time = models.DateTimeField('时间', auto_now=True)

    def __unicode__(self):
        return self.file

class ErrorMessage(models.Model):
    '''错误信息'''
    node = models.ForeignKey(Node, verbose_name='节点')
    version = models.ForeignKey(Version, verbose_name='版本')
    time = models.DateTimeField('时间', auto_now=True)
    message = models.CharField('信息', max_length=200)

    def __unicode__(self):
        return self.message
