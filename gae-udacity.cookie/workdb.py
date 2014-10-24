#-*- coding: utf-8 -*-
from google.appengine.ext import db

# Fu** ! wha's the function doing ?
"""
see following link (CS253 discuss form):  http://goo.gl/hhMBMb
The answer try to explaine how the "db.Key.from_path"  work.
We need a entity, but out of some unclear reason, we don't want the
 """
def user_model_key(name = "default"):
    return db.Key.from_path("Users", name)

#Define a Table in db, named BlogModel
class BlogModel(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class  UserModel(db.Model):
    username = db.StringProperty(required = True)
    userpw = db.StringProperty(required = True)
    usermail = db.EmailProperty()
    created = db.DateTimeProperty(auto_now_add = True)
