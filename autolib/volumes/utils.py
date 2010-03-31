##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from BeautifulSoup import BeautifulStoneSoup
from urllib2 import urlopen, HTTPError, URLError
import httplib
import re
from base import utils
from django.db.models import Q

from volumes.models import Book, BookEditionGroup
from tagging.models import Tag
from django.template.defaultfilters import slugify
from xml.sax.saxutils import unescape
import httplib

def get_editions(isbn):
	
	# Get on of the ISBN numbers and query google for all related editions
	if len(isbn) == 10 or len(isbn) == 13:
		url = 'http://books.google.com/books/feeds/volumes?q=editions:isbn' + isbn
	else:
		raise ValueError('Books must have either an ISBN10 or ISBN13 identifier')
	
	try:
		return BeautifulStoneSoup(urlopen(url).read())
	except (HTTPError, URLError, httplib.BadStatusLine, httplib.InvalidURL, ValueError, IOError):
		return None		

class BookDetail():
	"""
	Gets information regarding books using Google's books API
	"""
	
	THUMBNAIL_REL = 'http://schemas.google.com/books/2008/thumbnail'
	INFO_REL = 'http://schemas.google.com/books/2008/info'
	ANNOTATION_REL = 'http://schemas.google.com/books/2008/annotation'
	ALTERNATE_REL = 'alternate'
	SELF_REL = 'self'
	
	status = False
		
	def __init__(self, url):
# 		try:
		xml = unicode(urlopen(url).read(), errors='ignore')
		self.soup = BeautifulStoneSoup(xml)
# 		except (HTTPError, URLError, httplib.BadStatusLine, httplib.InvalidURL, ValueError, IOError):
# 			return None
		
		if self.soup is not None:
			
			self.status = True
			entry = self.soup
			
			author =  entry.find('dc:creator')
			self.author = unescape(author.string) if author is not None else None
			date = entry.find('dc:date')
			
			if date is not None:
				dateString = ''
				if re.match('^[0-9][0-9][0-9][0-9]$', date.string): dateString = date.string + '-01-01 00:00:00'
				elif re.match('^[0-9][0-9][0-9][0-9]-[0-9][0-9]$', date.string): dateString = date.string + '-01 00:00:00'
				elif re.match('^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$', date.string): dateString = date.string + ' 00:00:00'
				self.published = utils.parseDateTime(dateString)
			else:
				self.published = None
				
			description = entry.find('dc:description')
			self.description = unescape(description.string) if description is not None else None
			
			self.width = self.height = self.depth = self.pages = self.format = None
			
			try:
				for format in entry.findAll('dc:format'):
					if format.string.startswith('Dimensions'):
						dimensions = format.string.split(' ')[1]
						dimensions = dimensions.split('x')
						self.width = float(dimensions[0])
						self.height = float(dimensions[1])
						self.depth = float(dimensions[2])
					elif re.match('[0-9]', format.string):
						self.pages = int(format.string.split(' ')[0])
					else:
						self.format = unescape(format.string)
			except IndexError:
				# Some dimensions are not present
				pass
			
			
			
			identifiers = entry.findAll('dc:identifier')
			
			self.googleid = identifiers[0].string
			self.isbn10 = self.isbn13 = None
			for identifier in identifiers[1:]:
				if identifier.string.startswith('ISBN:'):
					isbn = identifier.string.lstrip('ISBN:')
					if len(isbn) == 10:
						self.isbn10 = isbn
					elif len(isbn) == 13:
						self.isbn13 = isbn
					else:
						# ERROR: It's an ISBN but is not 10 or 13 digits long
						pass
			
			language = entry.find('dc:language')
			self.language = language.string if language is not None else None
			publisher = entry.find('dc:publisher')
			self.publisher = unescape(publisher.string) if publisher is not None else None
			
			self.thumbnail_base = None
			self.thumbnail_huge = None
			self.thumbnail_small = None
			self.thumbnail_large = None
			
			# Thubnail
			for link in entry.findAll('link'):
				if link['rel'] == self.THUMBNAIL_REL:
					url = httplib.urlsplit(unescape(link['href']))
					self.thumbnail_base = url.scheme + '://' + url.netloc + url.path + '?id=' + self.googleid + '&printsec=frontcover&img=1&zoom='
					self.thumbnail_large = self.thumbnail_base + '1'
					self.thumbnail_small = self.thumbnail_base + '5'
					self.thumbnail_huge = self.thumbnail_base + '0'
			
			self.subjects = []
			for subject in entry.findAll('dc:subject'):
				self.subjects.append(unescape(subject.string))
			
			title = entry.find('dc:title')
			self.title = unescape(title.string) if title is not None else None
			
		else:
			self.status = False
	
	def get_details(self):
		if self.status:
			return {
				'title': self.title,
				'isbn10': self.isbn10,
				'isbn13': self.isbn13,
				'description': self.description,
				'publisher': self.publisher,
				'published': self.published,
				'author': self.author,
				'pages': self.pages,
				'format': self.format,
				'language': self.language,
				'width': self.width,
				'height': self.height,
				'depth': self.depth,
				'thumbnail_large': self.thumbnail_large,
				'thumbnail_small': self.thumbnail_small,
				'thumbnail_base': self.thumbnail_base,
				'thumbnail_huge': self.thumbnail_huge,
			}
		else:
			return None
	
	def get_book(self):
		if self.status:
			try:
				return Book.objects.get(Q(isbn10=self.isbn10) | Q(isbn13=self.isbn13))
			except Book.DoesNotExist:
				return None
		else:
			return None
	
	def convert_to_book(self, edition_group=None):
		"""
		Converts a BookDetail object into a Book object (from the database).
		 - If the book already exists it is retrieved from the database (unchanged)
		 - If the book does not exist it is created
		   - If an edition_group is specified it is set as the edition_group for the new book
		   - If an edition_group is not specified:
		     - Editions are retrieved from Google Books
		     - If any of those editions exist in the database, that Book's edition_group is used.
		"""
		
		# If this BookDetail has details
		if self.status:
			
			# Attempt to get the book from the database
			book = self.get_book()
			
			# If the book is in the database
			if book is not None:
				# possibly update information
				pass
				
			else:
				# Create a new book
				book = Book(**self.get_details())
				
				# If an edition_group was provided
				if edition_group is not None:
					# assign this new book that edition_group
					book.edition_group = edition_group
				else:
					# Get the editions (XML data) soup
					editionSoup = get_editions(self.isbn10) if self.isbn10 is not None else get_editions(self.isbn13)
					# Check each editions ISBN numbers
					for entry in editionSoup.findAll('entry'):
						# For each identifier
						for ident in entry.findAll('dc:identifier'):
							
							# If it is an ISBN identifier
							if ident.string.startswith('ISBN:'):
								# Get the actual ISBN
								isbn = ident.string.lstrip('ISBN:')
								
								try:
									# See if its the same book as the initial book, or if it is in the database.
									if len(isbn) == 10:
										if isbn == book.isbn10: continue
										existing_book = Book.objects.get(isbn10=isbn)
									elif len(isbn) == 13:
										if isbn == book.isbn13: continue
										existing_book = Book.objects.get(isbn13=isbn)
									
									# Assign the book we are trying to create the edition_group of this book
									book.edition_group = existing_book.edition_group
									book.save()
									
									# Add the subjects as tags to this book
									for subject in self.subjects:
										Tag.objects.add_tag(book, slugify(subject))
									
									return book
									
								except Book.DoesNotExist:
									# If not found try the next ISBN or the next Edition.
									continue
					
					# If no other editions were found in the database, its safe to create a new edition_group for this book
					edition_group = BookEditionGroup()
					edition_group.save()
					book.edition_group = edition_group
				
			# Save the book to the database
			book.save()
			
			# Add the subjects as tags to this book
			for subject in self.subjects:
				Tag.objects.add_tag(book, slugify(subject))
			
			return book
		else:
			return None

def update_all_editions(book):
	"""
	Ensures all other editions of the same book are in the database and that all editions are associated with the same edition_group.
	"""
	
	# Get the editions soup for this book
	soup = get_editions(book.isbn10) if book.isbn10 else get_editions(book.isbn13)
	
	# Create a list for the resultant book details URLs
	books = []
	
	# For each edition
	for entry in soup.findAll('entry'):
		# Check all identifiers
		for ident in entry.findAll('dc:identifier'):
			# If its an ISBN identifier
			if ident.string.startswith('ISBN:'):
				# Get the actual ISBN
				isbn = ident.string.lstrip('ISBN:')
				
				try:
					# See if its the same book as the initial book, or if it is in the database.
					if len(isbn) == 10:
						if isbn == book.isbn10: continue
						book.edition_group.editions.get(isbn10=isbn)
					elif len(isbn) == 13:
						if isbn == book.isbn13: continue
						book.edition_group.editions.get(isbn13=isbn)
				except Book.DoesNotExist:
					# If not found, add it to the database and to the inital books edition_group
					BookDetail(entry.id.string).convert_to_book(book.edition_group)

def get_book_detail(isbn):
	"""
	Gets al details from google books about regarding a specific ISBN, making them assessable through a BooKDetail object.
	"""
	
	# If the ISBN number is the correct length
	if len(isbn) == 10 or len(isbn) == 13:
		
		# Query Google
		queryUrl = 'http://books.google.com/books/feeds/volumes?q=isbn:' + isbn
		try:
			querySoup = BeautifulStoneSoup(urlopen(queryUrl).read())
		except (HTTPError, URLError, httplib.BadStatusLine, httplib.InvalidURL, ValueError, IOError):
			return None
		
		# If an entry was found
		if querySoup.entry is not None:
			
			# Find the url for the full details of the book
			volumeUrl = querySoup.entry.id.string
			# Return a BookDetail object containign those detials
			return BookDetail(volumeUrl)
			
		else:
			raise Exception('ISBN not found using Google Books')
	else:
		raise Exception('An ISBN must be 10 or 13 digits long')


import threading

class UpdateEditions(threading.Thread):
	"""
	A thread which calls the update_all_editions() utility function on a specific book.
	Books are added within a view, we do not want the make the user wait for all editions to be updated
	when they only care about their single book. We use a thread to execute this process non-sequentially.
	"""
	
	def __init__(self, book):
		"""
		Specifies the book on which to update the editions
		"""
		
		super(UpdateEditions, self).__init__()
		self.book = book
	
	def run(self):
		"""
		Updates the editions for a specific book.
		"""
		update_all_editions(self.book)
