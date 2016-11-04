from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

import webapp2
import jinja2
import os
import urllib
import datetime

from CreateStream import Picture
from CreateStream import Stream

JINJA_ENVIRONMENT=jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class TrendPage(webapp2.RequestHandler):
    def get(self):
    	streams=Stream.query().order(-Stream.num_of_views).fetch(3)
    	template_values={
            'streams':streams,
        }
        template=JINJA_ENVIRONMENT.get_template('trend.html')
        self.response.write(template.render(template_values))
	
application = webapp2.WSGIApplication([
    ('/trend', TrendPage),
], debug=True)