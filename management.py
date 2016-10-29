import os
import urllib

import webapp2
import jinja2

JINJA_ENVIRONMENT=jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class ManagementPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('management.html')
        self.response.write(template.render())


application = webapp2.WSGIApplication([
    ('/management',ManagementPage),
], debug=True)