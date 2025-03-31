from django.contrib import admin
from apps.user.models import Profile, Comment

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'date_joined']
    search_fields = ['username', 'email', 'first_name']
    ordering = ("-date_joined",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'publication_unit', 'created_at']
    search_fields = ['profile', 'publication_unit']
    ordering = ("-created_at",)