class Adapter(object):
	"""
	An interface for other adapters
	"""
	
	def __init__(self, isbn):
		raise NotImplementedError
	
	def get_title(self):
		raise NotImplementedError
	
	def get_isbn10(self):
		raise NotImplementedError
	
	def get_isbn13(self):
		raise NotImplementedError
	
	def get_description(self):
		raise NotImplementedError
	
	def get_publisher(self):
		raise NotImplementedError
	
	def get_published(self):
		raise NotImplementedError
	
	def get_author(self):
		raise NotImplementedError
	
	def get_pages(self):
		raise NotImplementedError
	
	def get_dimensions(self):
		raise NotImplementedError
	
	def get_width(self):
		raise NotImplementedError
		
	def get_height(self):
		raise NotImplementedError
	
	def get_depth(self):
		raise NotImplementedError
	
	def get_format(self):
		raise NotImplementedError
	
	def get_custom_id(self):
		raise NotImplementedError
	
	def get_language(self):
		raise NotImplementedError
	
	def get_subjects(self):
		raise NotImplementedError
	
	def does_exist(self):
		raise NotImplementedError
	
	def get_details(self):
		if self.does_exist():
			return dict({
				'title': self.get_title(),
				'isbn10': self.get_isbn10(),
				'isbn13': self.get_isbn13(),
				'description': self.get_description(),
				'publisher': self.get_publisher(),
				'published': self.get_published(),
				'author': self.get_author(),
				'pages': self.get_pages(),
				'format': self.get_format(),
				'language': self.get_language(),
			}.items() + self.get_dimensions().items())
		else:
			return None
			

from BeautifulSoup import BeautifulStoneSoup
from urllib import urlopen
import re
from base import utils

class GoogleAdapter(Adapter):
	"""
	Gets information regarding books using Google's books API
	"""
		
	def __init__(self, isbn):
		url = 'http://books.google.com/books/feeds/volumes?q=isbn:' + isbn
		searchFeed = BeautifulStoneSoup(urlopen(url).read())
		
		if searchFeed.entry is not None:
			self.status = True
			
			volumeURL = searchFeed.entry.id.string
			self.soup = BeautifulStoneSoup(urlopen(volumeURL).read())
			
			entry = self.soup.entry
			
			author =  entry.find('dc:creator')
			self.author = author.string if author is not None else None
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
			self.description = description.string if description is not None else None
			
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
					self.format = format.string
			
			identifiers = entry.findAll('dc:identifier')
			
			self.googleid = identifiers[0].string
			self.isbn10 = ''
			self.isbn13 = ''
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
			self.publisher = publisher.string if publisher is not None else None
			
			self.subjects = []
			for subject in entry.findAll('dc:subject'):
				self.subjects.append(subject.string)
			
			title = entry.find('dc:title')
			self.title = title.string if title is not None else None
		else:
			self.status = False
	
	def get_title(self):
		return self.title
		
	def get_isbn10(self):
		return self.isbn10
	
	def get_isbn13(self):
		return self.isbn13
	
	def get_description(self):
		return self.description
	
	def get_publisher(self):
		return self.publisher
	
	def get_published(self):
		return self.published
	
	def get_author(self):
		return self.author
	
	def get_pages(self):
		return self.pages
	
	def get_dimensions(self):
		return {'width': self.width, 'height': self.height, 'depth': self.depth}
	
	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height
	
	def get_depth(self):
		return self.depth
	
	def get_format(self):
		return self.format
	
	def get_custom_id(self):
		return self.googleid
	
	def get_language(self):
		return self.language
	
	def get_subjects(self):
		return self.subjects
	
	def does_exist(self):
		return self.status