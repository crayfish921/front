import webapp2
from google.appengine.ext import ndb
import labApp
import endpoints


class Glavnaya(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('lab.html').read())

class Scoreboard(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('scores.html').read())
                             
app = webapp2.WSGIApplication([
    ('/', Glavnaya),
    ('/scoreboard', Scoreboard),
],debug = True)

APPLICATION = endpoints.api_server([labApp.Labyrinth])