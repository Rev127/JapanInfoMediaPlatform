from django.contrib import admin
from infoPlatformMainApp.models import ServerNews, WorkNews

# Register your models here.
@admin.register(ServerNews)
class ServerNewsAdmin(admin.ModelAdmin):
    list_display = ['news_type', 'created_at']
    search_fields = ['news_type']
    ordering = ("-created_at", 'news_type')

@admin.register(WorkNews)
class WorkNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_at']
    search_fields = ['title', 'content']
    ordering = ("-created_at", 'title',)