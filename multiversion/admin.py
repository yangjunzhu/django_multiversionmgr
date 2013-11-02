from django.contrib import admin

from models import *

class FtpInfoAdmin(admin.ModelAdmin):
    model=FtpInfo
    list_display = ('descript', 'ip', 'port', 'anonymous', 'user', 'password')

class ServiceInfoAdmin(admin.ModelAdmin):
    model=ServiceInfo
    list_display = ('descript', 'sendip', 'sendport', 'revip', 'revport')
class NodeAdmin(admin.ModelAdmin):
    model=Node
    list_display = ('descript', 'ip', 'lasttime')

class NodeGroupAdmin(admin.ModelAdmin):
    model=NodeGroup
    list_display = ('descript')

class SoftwareAdmin(admin.ModelAdmin):
    model=Software
    list_display = ('descript', 'softwarepath')

class VersionAdmin(admin.ModelAdmin):
    model=Version
    list_display = ('software', 'descript', 'versionpath', 'totalfile', 'md5code', 'createtime', 'path')

class FileInfoAdmin(admin.ModelAdmin):
    model=FileInfo
    list_display = ('version', 'filepath', 'filename', 'md5code', 'filepathname', 'filefullpathname')

class VersionMgrAdmin(admin.ModelAdmin):
    model=VersionMgr
    list_display = ('node', 'version', 'deploypercent', 'currentfile', 'filepercent', 'nodecode',
                    'nodestatus', 'time', 'status')

class CreateVersionAdmin(admin.ModelAdmin):
    model=CreateVersion
    list_display = ('version', 'currentfile', 'createpercent')

admin.site.register(FtpInfo, FtpInfoAdmin)
admin.site.register(ServiceInfo, ServiceInfoAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeGroup)#, NodeGroupAdmin)
admin.site.register(Software, SoftwareAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(FileInfo, FileInfoAdmin)
admin.site.register(VersionMgr, VersionMgrAdmin)
admin.site.register(CreateVersion, CreateVersionAdmin)
