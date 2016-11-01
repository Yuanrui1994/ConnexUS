from google.appengine.api import users

import webapp2
import jinja2
import os

__author__='yuanrui'

JINJA_ENVIRONMENT=jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            url_linktext="logout"
            url=users.create_logout_url("/")
        else:
            url_linktext="Login"
            url=users.create_login_url("/management")
        template_values={
            'url':url,
            'url_linktext':url_linktext,
        }
        template=JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/',LoginPage),
], debug=True)




