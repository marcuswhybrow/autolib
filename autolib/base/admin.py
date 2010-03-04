from django.contrib import admin

from libraries.models import Collection
from base.models import Config, Update
from books.models import Book, BookProfile, BookEditionGroup

class SoftDeleteAdmin(admin.ModelAdmin):
	
	def queryset(self, request):
		# Use the objects manager (which hides Soft Deleted objects) in the admin interface
		return self.model.objects

# Register models to be included in the admin, specifing any which are soft deletable with the special queryset
admin.site.register(Collection, SoftDeleteAdmin)
admin.site.register(Book)
admin.site.register(BookEditionGroup)
admin.site.register(BookProfile, SoftDeleteAdmin)
admin.site.register(Config)
admin.site.register(Update)