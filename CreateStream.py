import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import blobstore
from google.appengine.api import mail

import webapp2
import jinja2

__author__='yuanrui'

class Picture(ndb.Model):
	blob_key=ndb.BlobKeyProperty()
	date=ndb.DateTimeProperty(auto_now_add=True)
	
class Stream(ndb.Model):
	name=ndb.StringProperty()
	owner=ndb.UserProperty()
	tags=ndb.StringProperty(repeated=True)
	subscribers=ndb.StringProperty(repeated=True)
	pictures=ndb.StructuredProperty(Picture,repeated=True)
	cover_url=ndb.StringProperty()
	creation_time=ndb.DateTimeProperty(auto_now_add=True)
	last_new_date=ndb.DateTimeProperty(auto_now_add=True)
	num_of_pics=ndb.IntegerProperty()
	num_of_views=ndb.IntegerProperty()


JINJA_ENVIRONMENT=jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class CreateStreamPage(webapp2.RequestHandler):
    def get(self):
        template=JINJA_ENVIRONMENT.get_template('CreateStream.html')
        self.response.write(template.render())

class CreateStream(webapp2.RequestHandler):
	def post(self):
		stream_name=self.request.get('name')
		streams=Stream.query(Stream.name==stream_name).fetch()
		if len(streams)>0:
			self.redirect('/error')
			return
		else:
			new_stream=Stream()
			new_stream.name=stream_name
			new_stream.owner=users.get_current_user()
			new_stream.tags=self.request.get('tags').split(',')
			new_stream.subscribers=self.request.get('subscribers').split(',')
			new_stream.cover_url=self.request.get('cover_url')
			new_stream.num_of_views=0
			new_stream.num_of_pics=0
			new_stream.put()
			to_addrs=self.request.get('subscriber').split(',')
			email_sender=users.get_current_user().email()
			email_subject=users.get_current_user().nickname()+"shares a new stream with you"
			email_message=self.request.get('message')
			for email_receiver in to_addrs:
				if mail.is_email_valid(email_receiver):
					mail.send_mail(sender=email_sender,to=email_receiver,subject=email_subject,body=email_message)
			self.redirect('/management')
application = webapp2.WSGIApplication([
	('/sign',CreateStream),
    ('/createstream',CreateStreamPage),
], debug=True)

			

	



