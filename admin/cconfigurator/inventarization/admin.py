from django.contrib import admin
from .models import *

admin.site.register(UplinkStat)
admin.site.register(Border)
admin.site.register(SiteLatency)
admin.site.register(Site)
admin.site.register(Node)
admin.site.register(NodeLatency)
admin.site.register(NodeIp)
admin.site.register(Service)
