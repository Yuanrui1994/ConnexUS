import os
import urllib

import webapp2
import jinja2

__author__="yuanrui"

JINJA_ENVIRONMENT=jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class ErrorPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/error',ErrorPage),
], debug=True)
