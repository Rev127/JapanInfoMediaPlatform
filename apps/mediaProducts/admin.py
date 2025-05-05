from django.contrib import admin
from  .models import Work, Characters, CharacterPublication, Author, Manga, Anime, Novel, Volumes, Seasons

# Register your models here.
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'link']
    search_fields = ['title', 'author']
    list_display_links = ['title', 'link']
    autocomplete_fields = ['author']
    list_filter = ['genre']
    filter_horizontal = ['genre']
    ordering = ('title',)

@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ('name',)

@admin.register(CharacterPublication)
class CharacterPublicationAdmin(admin.ModelAdmin):
    list_display = ['character', 'publication_type']
    search_fields = ['character']
    list_display_links = ['character']
    autocomplete_fields = ['character']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'work_years']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ('name',)

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'artist', 'publisher', 'work']
    search_fields = ['title', 'artist', 'publisher', 'work']
    list_display_links = ['title', 'link']
    ordering = ('title', 'artist', 'publisher', 'work',)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'director', 'studio', 'work']
    search_fields = ['title', 'director', 'studio', 'work']
    list_display_links = ['title', 'link']
    ordering = ('title', 'director', 'studio', 'work',)

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'illustrator', 'publisher', 'work']
    search_fields = ['title', 'illustrator', 'publisher', 'work']
    list_display_links = ['title', 'link']
    ordering = ('title', 'illustrator', 'publisher', 'work',)

@admin.register(Volumes)
class VolumesAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'status']
    search_fields = ['title', 'status']
    list_display_links = ['title', 'link']
    ordering = ('title', 'status',)

@admin.register(Seasons)
class SeasonsAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'status']
    search_fields = ['title', 'status']
    list_display_links = ['title', 'link']
    ordering = ('title', 'status',)


