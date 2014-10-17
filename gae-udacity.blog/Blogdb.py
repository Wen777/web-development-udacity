#-*- coding: utf-8 -*-
from google.appengine.ext import db

class BlogModel(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)