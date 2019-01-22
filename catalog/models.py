import uuid
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter a book genre (eg. Science Fiction)')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=100, help_text='Enter a language for this book (eg. English)')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(
        max_length=100, help_text='Enter the first name of the author')
    last_name = models.CharField(
        max_length=100, help_text='Enter the last name of the author')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief decription of the book')
    imprint = models.CharField(max_length=200)
    isbn = models.CharField("ISBN", max_length=13)
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, help_text='Select a language for this book')

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'GENRE'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique id for this particular book across the whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'MAINTAINANCE'),
        ('O', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Book Availability')

    class Meta:
        ordering = ('due_back',)

    def __str__(self):
        return "%s %s" % (self.id, self.book.title)
