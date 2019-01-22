from django.contrib import admin

from catalog.models import Author, Book, BookInstance, Genre, Language

# admin.site.register(Author)


class BooksInline(admin.StackedInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    list_filter = ('last_name', 'first_name', 'date_of_birth')
    fields = ('last_name', 'first_name', ('date_of_birth', 'date_of_death'))
    inlines = (BooksInline,)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
    inlines = (BooksInstanceInline,)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'imprint', 'book', 'due_back', 'status')
    list_filter = ('id', 'due_back', 'status')
    fieldsets = (
        (None, {
            'fields': ('id', 'book', 'imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
