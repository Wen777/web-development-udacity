#-*- coding: utf-8 -*-
import  webapp2, cgi, hashlib
from sign import judge
import workdb
from string import split
from jinja2 import Environment, PackageLoader, Template, FileSystemLoader
jinja_env = Environment(loader=FileSystemLoader('templates'), autoescape=True)


#Define basic class, funtion
class Handler(webapp2.RequestHandler):
    """docstring for Handler
        template=? **params=? *a=? **kw=?
    """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params) #return Unicode object
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#Hash function
def hashVal(val):
    return ("%s|%s") % ( val, hashlib.sha256(val).hexdigest() )

#Cookie set, check
class cookie(object):
    """docstring for cookie"""
    def setCookie(self, cookieName, cookieVal):
        cookieName = str(cookieName)
        cookieVal = str(cookieVal)
        self.response.headers['Set-Cookie'] = "%s=%s; path=/;" %(cookieName, cookieVal)
    def checkCookie(self, DOM_cookie):
        val = DOM_cookie.split("|")[0]
        if DOM_cookie == hashVal(val):
            return True
        else:
            return False

#MainPage
class MainPage(Handler):
    """docstring for MainPage"""
    def get(self):
        self.render("mainpage.html")

#Sign In Page
class SignIn(Handler, cookie):
    """docstring for SignIn"""
    def get(self):
        self.render("signin.html")
    def post(self):
        signState = "signin"
        name = self.request.get("username")
        pw = self.request.get("password")
        params = dict(name=name, pw= pw, signState = signState)
        have_error, params = judge(**params)

        if have_error:
            self.render("signin.html", **params)
        else :
            self.setCookie("name", hashVal(name))
            self.redirect("/welcome")

#SignUp page
class SignUp(Handler, cookie):
    """docstring for SignUp"""
    def get(self):
        self.render("signup.html")
    def post(self):
        signState = "signup"
        name = self.request.get("username")
        pw = self.request.get("password")
        verifypw = self.request.get("verify")
        mail = self.request.get("email")
        params = dict(name=name, pw= pw, verifypw=verifypw, mail=mail, signState = signState)
        #print params
        #print have_error
        have_error, params = judge(**params)
        if have_error:
            #error_username = params.get("error_username","")
            #error_password=params.get('error_password',"")
            #error_verify=params.get('error_verify', "")
            #error_email=params.get('error_email', "")
            ##Here got some problems
            #self.render("/signup", error_username, error_password,error_verify,error_email)
            self.render("signup.html", **params)
        elif name and pw :
            if not mail:
                mail = None
            a = workdb.UserModel(parent = workdb.user_model_key(), username = name, userpw = hashVal(pw), usermail=mail)
            a.put()
             #   self.redirect('/blog/%s' % str(a.key().id()))
            self.setCookie("name", hashVal(name))
            self.redirect("/welcome")

""" Another system"""

#Set a key to each post
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

#Blog main page
class BlogPage(Handler):
    """docstring for MainPage"""
    def queryPost(self):
        return db.GqlQuery('SELECT * FROM BlogModel ORDER BY created DESC limit 10')

    def get(self):
        posts = self.queryPost()
        self.render("blog.html", posts = posts)
#post page
class PostPage(Handler):
    """docstring for postPage"""
    def get(self, post_id):
        ## WHY FOLLOWING CODE CAN WORK ???##
        key = db.Key.from_path('BlogModel', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("blog_permalink.html", post = post)
#New post page
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

class Welcome(Handler, cookie):
    def get(self):
        DOM_name = self.request.cookies.get("name")
        if self.checkCookie(DOM_name):

            self.render("welcome.html", name = DOM_name.split("|")[0])
        else:
            self.redirect("/signup")


app = webapp2.WSGIApplication([("/", MainPage),
                                                          ("/signup", SignUp),
                                                          ("/signin", SignIn),
                                                          ('/blog', BlogPage),
                                                          ('/blog/newpost', NewPost),
                                                          ('/blog/([0-9]+)', PostPage),
                                                          ("/welcome", Welcome)
                                                         ], debug=True)