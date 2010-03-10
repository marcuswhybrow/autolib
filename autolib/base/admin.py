from django.contrib import admin

from libraries.models import Collection
from base.models import Config, Update
from volumes.models import Book, BookProfile, BookEditionGroup, Note

# Register models to be included in the admin
admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(BookEditionGroup)
admin.site.register(BookProfile)
admin.site.register(Note)
admin.site.register(Config)
admin.site.register(Update)