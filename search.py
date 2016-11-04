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

class SearchPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render())

class SearchResultPage(webapp2.RequestHandler):
    def post(self):
    	keyword=self.request.get('keyword')
    	streams=Stream.query().fetch()
    	searched_streams=[]
    	for stream in streams:
    		if keyword in stream.tags:
    			searched_streams.append(stream)
    	results_num=len(searched_streams)
    	template_values={
    	   'results_num':results_num,
    	   'keyword':keyword,
    	   'streams':searched_streams,
    	}
    	template=JINJA_ENVIRONMENT.get_template('SearchResult.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	('/search',SearchPage),
    ('/searchresult',SearchResultPage),
], debug=True)


