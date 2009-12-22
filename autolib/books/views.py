from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Book
# Book related views

def book_detail(request, isbn):
	return render_to_response('books/book_detail.html', {
		'book' : get_object_or_404(Book, isbn=isbn),
	}, context_instance=RequestContext(request))

def book_list(request):
	return render_to_response('books/book_list.html', {
		'books': Book.objects.all()
	}, context_instance=RequestContext(request))