from django.contrib import admin
from  .models import Work, Characters, CharacterWork, Author, Manga, Anime, Novel, Volumes, Seasons, MangaVolumes, NovelVolumes, AnimeSeasons

# Register your models here.
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'link']
    search_fields = ['title', 'author']
    list_display_links = ['title', 'link']
    autocomplete_fields = ['author']
    list_filter = ['genre']
    filter_horizontal = ['genre']
    ordering = ('title', 'genre',)

@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    search_fields = ['name']
    list_display_links = ['name', 'link']
    ordering = ('name',)

@admin.register(CharacterWork)
class CharacterWorkAdmin(admin.ModelAdmin):
    list_display = ['character', 'work']
    search_fields = ['character', 'work']
    list_display_links = ['character', 'work']
    autocomplete_fields = ['character', 'work']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'work_years']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ('name',)

class MangaVolumesInline(admin.TabularInline):
    model = MangaVolumes
    extra = 0
    autocomplete_fields = ['publication_unit']

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'artist']
    search_fields = ['title', 'artist']
    list_display_links = ['title', 'link']
    ordering = ('title', 'artist',)
    inlines = [MangaVolumesInline]

class AnimeSeasonsInline(admin.TabularInline):
    model = AnimeSeasons
    extra = 0
    autocomplete_fields = ['publication_unit']

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'director', 'studio']
    search_fields = ['title']
    list_display_links = ['title', 'link']
    ordering = ('title', 'director', 'studio',)
    inlines = [AnimeSeasonsInline]

class NovelVolumesInline(admin.TabularInline):
    model = NovelVolumes
    extra = 0
    autocomplete_fields = ['publication_unit']

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'illustrator', 'publisher']
    search_fields = ['title', 'illustrator', 'publisher']
    list_display_links = ['title', 'link']
    ordering = ('title', 'illustrator', 'publisher',)
    inlines = [NovelVolumesInline]

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


