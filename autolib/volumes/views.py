from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from volumes.models import Book, BookEditionGroup
# Book related views

def book_detail(request, isbn):
	'''Gets information about a Book usage within the system.'''
	
	book = get_object_or_404(Book, isbn10=isbn)
	
	return render_to_response('books/book_detail.html', {
		'book': book,
	}, context_instance=RequestContext(request))

def book_list(request):
	'''Gets a list of all Books referenced throughout the system.'''
	
	books = []
	for edition_group in BookEditionGroup.objects.all():
		books.append(edition_group.editions.latest())
	
	return render_to_response('books/book_list.html', {
		'books': books,
	}, context_instance=RequestContext(request))

def add_book(request):
	
	return render_to_response('books/add_book.html', {})