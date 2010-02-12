from django.contrib import admin

from libraries.models import Collection
from base.models import Config, Update
from books.models import Book, BookProfile

admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(BookProfile)
admin.site.register(Config)
admin.site.register(Update)
