from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Book
from voting.models import Vote
# Book related views

def book_detail(request, isbn):
	'''Gets information about a Book usage within the system.'''
	
	book = get_object_or_404(Book, isbn10=isbn)
	score = Vote.objects.get_score(book)
	try:
		vote = Vote.objects.get(user=request.user, object_id=book.pk)
	except Vote.DoesNotExist:
		vote = None
	
	return render_to_response('books/book_detail.html', {
		'book': book,
		'score': score,
		'vote': vote,
	}, context_instance=RequestContext(request))

def book_list(request):
	'''Gets a list of all Books referenced throughout the system.'''
	
	return render_to_response('books/book_list.html', {
		'books': Book.objects.all()
	}, context_instance=RequestContext(request))

def add_book(request):
	
	return render_to_response('books/add_book.html', {})