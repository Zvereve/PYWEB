from django.contrib import admin

from .models import Note, Comment



@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'public', 'date_up', 'author', )
    fields = (('title', 'public'), 'message', 'date_add', 'date_up')
    readonly_fields = ('date_add', 'date_up')
    search_fields = ['title']
    #
    # Фильтры справа
    list_filter = ('public', 'id')


@admin.register(Comment)
class ComentAdmin(admin.ModelAdmin):

    list_display = ('author', 'comment', 'note_id', 'rating', )
    #fields = (('title', 'public'), 'message', 'date_add', 'date_up')

    #search_fields = ['title']
    #
    # Фильтры справа
    list_filter = ('author', 'note_id')

