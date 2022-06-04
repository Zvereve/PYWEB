from django.contrib import admin

from .models import Note, Comment



@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'public', 'date_up', 'author', 'relevant', 'rating', )
    fields = (('author', 'relevant', 'title', 'public'), 'message', 'date_add', 'date_up', 'rating', )
    readonly_fields = ('date_add', 'date_up')
    search_fields = ['title']
    #
    # Фильтры справа
    list_filter = ('public', 'author', 'relevant', 'rating')


@admin.register(Comment)
class ComentAdmin(admin.ModelAdmin):

    list_display = ('author', 'note', 'comment', )
    fields = (('author', 'note'), 'comment',)

    #search_fields = ['title']
    #
    # Фильтры справа
    #list_filter = ('author', 'note_id')

