from django.contrib import admin

from autolib.libraries.models import Collection
from autolib.books.models import Book

admin.site.register(Collection)
admin.site.register(Book)
