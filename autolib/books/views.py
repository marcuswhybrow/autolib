# Book related views

def book(request, isbn):
	return render_to_response('books/book_detail.html', {
		'book' : get_object_or_404(Book, isbn=isbn),
	}, context_instance=RequestContext(request))