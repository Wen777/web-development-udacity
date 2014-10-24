#-*- coding: utf-8 -*-
import  webapp2, cgi
from google.appengine.ext import db
from jinja2 import Environment, PackageLoader, Template, FileSystemLoader
jinja_env = Environment(loader=FileSystemLoader('templates'), autoescape=True)

#Define a Table in db, named BlogModel
class BlogModel(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

#Define basic class, funtion
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
        subject = self.request.get("subject")
        content = self.request.get("content")

class BlogPage(Handler):
    """docstring for MainPage"""
    def queryPost(self):
        return db.GqlQuery('SELECT * FROM BlogModel ORDER BY created DESC limit 10')

    def get(self):
        posts = self.queryPost()
        self.render("blog.html", posts = posts)

class PostPage(Handler):
    """docstring for postPage"""
    def get(self, post_id):
        key = db.Key.from_path('BlogModel', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("blog_permalink.html", post = post)

class NewPost(Handler):
    """docstring for NewPost"""
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            a = BlogModel(parent = blog_key(),subject = subject, content = content)
            a.put()
            self.redirect('/blog/%s' % str(a.key().id()))
        else:
            self.render('newpost.html',error='invalid')
    def get(self):
        self.render("newpost.html")

app = webapp2.WSGIApplication([('/blog', BlogPage),
                                                          ('/blog/newpost', NewPost),
                                                          ('/blog/([0-9]+)', PostPage)
                                                         ], debug=True)