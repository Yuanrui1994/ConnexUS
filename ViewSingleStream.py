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

class ViewSingleStream(webapp2.RequestHandler):
    def get(self):
        stream_name=self.request.get('stream_name')
        stream=Stream.query(Stream.name==stream_name).fetch(1)[0]
        user=users.get_current_user()
        stream.num_of_views+=1;
        stream.put()
        upload_url = blobstore.create_upload_url('/upload_photo?stream_name='+str(stream_name))
        template_values={
        'stream_name':stream_name,
        'upload_url':upload_url,
        'pictures':stream.pictures
        }
        template=JINJA_ENVIRONMENT.get_template('ViewSingle.html')
        self.response.write(template.render(template_values))
        
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            stream_name=self.request.get('stream_name')
            stream=Stream.query(Stream.name==stream_name).fetch(1)[0]
            upload = self.get_uploads()[0]
            picture = Picture(
                blob_key=upload.key(),
                date=datetime.datetime.now())
            picture.put()
            stream.pictures.append(picture)
            stream.num_of_pics+=1
            stream.put()
            self.redirect('/view?stream_name='+str(stream_name))
        except:
            self.error(500)
# [END upload_handler]
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
# [END download_handler]
class SubscribeHandler(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        stream_name=self.request.get('stream_name')
        stream=Stream.query(Stream.name==stream_name).fetch(1)[0]
        stream.subscribers.append(user.email())
        stream.put()
        self.redirect('/view?stream_name='+str(stream_name))




app = webapp2.WSGIApplication([
    ('/view', ViewSingleStream),
    ('/upload_photo', PhotoUploadHandler),
    ('/view_photo/([^/]+)?', ViewPhotoHandler),
    ('/subscribe',SubscribeHandler),
], debug=True)




