from django.contrib import admin
from .models import *


class DreamsAdmin(admin.ModelAdmin):
    search_fields= ['email','pub']
    list_display = ('email','id', 'name','pub')
    ordering =['-pub','email']

class ReplyAdmin(admin.ModelAdmin):
    
    list_display = ('dream','id','pub')
    ordering =['-pub']

class ShareAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'ip', 'pub')
    ordering =['-pub']

admin.site.register(Dreams, DreamsAdmin)
admin.site.register(Reply, ReplyAdmin)
