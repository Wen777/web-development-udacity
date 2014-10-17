#-*- coding: utf-8 -*-
import  webapp2, cgi
import re
from jinja2 import Environment, PackageLoader, Template, FileSystemLoader
from google.appengine.ext import db
jinja_env = Environment(loader=FileSystemLoader('templates'), autoescape=True)

class Handler(webapp2.RequestHandler):
    """docstring for Handler
        template=? **params=? *a=? **kw=?
    """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

class MainPage(Handler):
    """docstring for MainPage"""
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html", title=title, art=art, error = error, arts = arts)
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        if title and art:
            a = Art(title = title, art = art)
            a.put()
            self.redirect("/")
    def get(self):
        self.render("front.html")
        #self.write("asciichan!")
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)