from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from  .models import Work, Characters, CharacterPublication, Author, Manga, Anime, Novel, Volumes, Seasons

# Register your models here.
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_genre']
    search_fields = ['title', 'author']
    list_display_links = ['title']
    autocomplete_fields = ['author']
    list_filter = ['genre']
    filter_horizontal = ['genre']
    ordering = ('title',)

    def get_genre(self, obj):
        return ", ".join([genre.get_name() for genre in obj.get_genres()])
    get_genre.short_description='Жанри'

class CharacterPublicationInline(admin.TabularInline):
    model = CharacterPublication
    extra = 0
    verbose_name = 'Опис песонажа в залежності від публікації'
    verbose_name_plural = 'Опис песонажа'

    def save_new(self, form, commit=True):
        # Отримуємо дані з форми
        character = form.cleaned_data.get('character')
        publication_type = form.cleaned_data.get('publication_type')

        # Перевіряємо, чи існує вже такий запис
        if CharacterPublication.objects.filter(character=character, publication_type=publication_type).exists():
            raise ValidationError(f"CharacterPublication with type '{publication_type}' already exists for this character.")

        return super().save_new(form, commit)

@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_display_links = ['name']
    inlines = [CharacterPublicationInline]
    ordering = ('name',)

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
    list_filter = ['publication_unit']
    filter_horizontal = ['publication_unit']
    ordering = ('title', 'artist', 'publisher', 'work',)

    # Аналогічно для ManyToManyField:
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "publication_unit":
            used = Manga.objects.all().values_list("publication_unit__id", flat=True)

            obj_id = request.resolver_match.kwargs.get('object_id')
            current_units = []
            if obj_id:
                try:
                    manga_obj = Manga.objects.get(pk=obj_id)
                    current_units = list(manga_obj.publication_unit.values_list("id", flat=True))
                except Manga.DoesNotExist:
                    pass

            kwargs["queryset"] = Volumes.objects.filter(
                Q(id__in=current_units) | ~Q(id__in=used)
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'director', 'studio', 'work']
    search_fields = ['title', 'director', 'studio', 'work']
    list_display_links = ['title', 'link']
    list_filter = ['publication_unit']
    filter_horizontal = ['publication_unit']
    ordering = ('title', 'director', 'studio', 'work',)

    # Аналогічно для ManyToManyField:
    from django.db.models import Q

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "publication_unit":
            used = Anime.objects.all().values_list("publication_unit__id", flat=True)

            obj_id = request.resolver_match.kwargs.get('object_id')
            current_units = []
            if obj_id:
                try:
                    anime_obj = Anime.objects.get(pk=obj_id)
                    current_units = list(anime_obj.publication_unit.values_list("id", flat=True))
                except Anime.DoesNotExist:
                    pass

            kwargs["queryset"] = Seasons.objects.filter(
                Q(id__in=current_units) | ~Q(id__in=used)
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'illustrator', 'publisher', 'work']
    search_fields = ['title', 'illustrator', 'publisher', 'work']
    list_display_links = ['title', 'link']
    list_filter = ['publication_unit']
    filter_horizontal = ['publication_unit']
    ordering = ('title', 'illustrator', 'publisher', 'work',)

    # Аналогічно для ManyToManyField:
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "publication_unit":
            used = Novel.objects.all().values_list("publication_unit__id", flat=True)

            obj_id = request.resolver_match.kwargs.get('object_id')
            current_units = []
            if obj_id:
                try:
                    novel_obj = Novel.objects.get(pk=obj_id)
                    current_units = list(novel_obj.publication_unit.values_list("id", flat=True))
                except Novel.DoesNotExist:
                    pass

            kwargs["queryset"] = Volumes.objects.filter(
                Q(id__in=current_units) | ~Q(id__in=used)
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Volumes)
class VolumesAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'status']
    search_fields = ['title', 'status']
    list_display_links = ['title', 'link']
    list_filter = ['active_characters']
    filter_horizontal = ['active_characters']
    ordering = ('title', 'status',)

@admin.register(Seasons)
class SeasonsAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'status']
    search_fields = ['title', 'status']
    list_display_links = ['title', 'link']
    list_filter = ['active_characters']
    filter_horizontal = ['active_characters']
    ordering = ('title', 'status',)


