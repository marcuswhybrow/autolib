from django.contrib import admin

from libraries.models import Collection
from base.models import Config
from books.models import Book

admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(Config)
