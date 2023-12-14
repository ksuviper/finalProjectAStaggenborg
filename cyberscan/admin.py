from django.contrib import admin
from.models import Scan, ScanResult, Trace, TraceResult

# Register your models here.
admin.site.register(Scan)
admin.site.register(ScanResult)
admin.site.register(Trace)
admin.site.register(TraceResult)
