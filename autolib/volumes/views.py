##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from volumes.models import Book, BookEditionGroup
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import HttpResponse

# Book related views

def book_detail(request, isbn):
	'''Gets information about a Book usage within the system.'''
	
	book = get_object_or_404(Book, isbn10=isbn)
	
	return render_to_response('books/book_detail.html', {
		'book': book,
	}, context_instance=RequestContext(request))

def book_list(request, page):
	'''Gets a list of all Books referenced throughout the system.'''
	
	books = []
	for edition_group in BookEditionGroup.objects.all():
		try:
			books.append(edition_group.editions.latest())
		except Book.DoesNotExist:
			edition_group.delete();
	
	# Set 10 books per page
	paginator = Paginator(books, 10)
	
	# Set the page to 1 if not specified
	page = 1 and page is None or page
	
	try:
		books_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		books_list = paginator.page(paginator.num_pages)
	
	return render_to_response('books/book_list.html', {
		'books': books_list,
	}, context_instance=RequestContext(request))

def add_book(request):
	
	return render_to_response('books/add_book.html', {})