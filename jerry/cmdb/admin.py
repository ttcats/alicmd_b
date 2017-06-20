from django.contrib import admin

# Register your models here.


from .models import *


class AssetAdmin(admin.ModelAdmin):
    list_display = ['hostname','ip']

class IDCAdmin(admin.ModelAdmin):
    list_display = ['name']

class AssetGroupAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(AssetGroup,AssetGroupAdmin)
admin.site.register(IDC,IDCAdmin)
admin.site.register(Asset,AssetAdmin)
