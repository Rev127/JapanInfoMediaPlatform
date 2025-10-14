from django.contrib import admin
from apps.user.models import Profile, Comment

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'date_joined']
    search_fields = ['username', 'email', 'first_name']
    list_filter = ['tracking_works', 'groups', 'user_permissions']
    filter_horizontal = ('tracking_works', 'groups', 'user_permissions')
    ordering = ("-date_joined",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'publication_unit', 'created_at']
    search_fields = ['user', 'publication_unit']
    ordering = ("-created_at",)