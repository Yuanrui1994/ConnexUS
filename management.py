import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import blobstore
from CreateStream import Stream
from CreateStream import Picture
import webapp2
import jinja2

__author__='yuanrui'

JINJA_ENVIRONMENT=jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class ManagementPage(webapp2.RequestHandler):
    def get(self):
  		user=users.get_current_user()
  		owned_streams=[]
  		subscribed_streams=[]
  		owned_streams=Stream.query(Stream.owner==user).fetch()
  		all_streams=Stream.query().fetch()
  		for stream in all_streams:
  			if (user.email() in stream.subscribers):
  				subscribed_streams.append(stream)

  		template_values={
  			'owned_streams':owned_streams,
  			'subscribed_streams':subscribed_streams
  		}
  		template=JINJA_ENVIRONMENT.get_template('management.html')
  		self.response.write(template.render(template_values))

class ManagementHandler(webapp2.RequestHandler):
  	def post(self):
  		user=users.get_current_user()
  		if self.request.get('delete'):
  			owned_streams=Stream.query(Stream.owner==user).fetch()
  			for stream in owned_streams:
  				tmp='delete'+str(stream.key.id())
  				if self.request.get(tmp):
  					stream.key.delete()
  		if self.request.get('unsubscribe'):
  			all_streams=Stream.query().fetch()
  			for stream in all_streams:
  				tmp='unsubscribe'+str(stream.key.id())
  				if self.request.get(tmp):
  					stream.subscribers.remove(user.email())
  					stream.put()
  		self.redirect('/management')

application = webapp2.WSGIApplication([
	('/managementhandler', ManagementHandler),
    ('/management',ManagementPage),
], debug=True)