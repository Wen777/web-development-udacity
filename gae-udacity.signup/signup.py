#-*- coding: utf-8 -*-
import  webapp2, cgi, os
import re
from jinja2 import Environment, PackageLoader, Template, FileSystemLoader

"""Regular Expression"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)

class MainPage(webapp2.RequestHandler):
    """docstring for MainPage"""
    #env = Environment(loader=PackageLoader('main', 'templates/signup'))
    #template = env.get_template('main.html')
    def get(self):
        jinja_env = Environment(loader=FileSystemLoader('templates'))
        template = jinja_env.get_template('main.html')
        self.response.out.write(template.render())

class sign(webapp2.RequestHandler):
    #env = Environment(loader=PackageLoader('signup', 'templates/signup'))

    def get(self):
        jinja_env = Environment(loader=FileSystemLoader('templates/signup'))
        template = jinja_env.get_template('signup.html')
        self.response.out.write(template.render())

    def render(self, filename, **template_values):
        jinja_env = Environment(loader=FileSystemLoader('templates/signup'))
        template = jinja_env.get_template(filename)
        self.response.out.write(template.render(template_values))

    def post(self):
        jinja_env = Environment(loader=FileSystemLoader('templates/signup'))
        template = jinja_env.get_template('signup.html')
        #Get input from html
        name = self.request.get('username')
        password = self.request.get('password')
        veripassword =  self.request.get('verify')
        mail = self.request.get('email')
        params = dict(username = name, email = mail)
        #sent input from web page to judge
        #msg1, msg2, msg3, msg4 = self.judge(name, password, veripassword, mail, params)
        have_error, params = self.judge(name, password, veripassword, mail, **params)
        if have_error:
        #if (msg1 == '') and (msg2 == '') and (msg3 == '') and (msg4 == ''):
            #redirect a "Welcome page"
            # signinPage = Template('<p style="">Welcome, {{ name }}</p>')
            # self.response.out.write(signinPage.render(name = name))
            # Welcome.catch(self.post.name)
            #self.redirect('/welcome?name=' + cgi.escape(name, quote=True) )
            self.render('signup.html', **params)
        else :
        #elif msg1  or msg2 or msg3 or msg4:
            #re-render
            #self.response.out.write( template.render(msg1 = msg1, msg2 = msg2, msg3= msg3, msg4 = msg4) )
            self.redirect('welcome?name='+ str(name))
            #self.redirect('welcome?name='+ cgi.escape(name, quote=True))
    def judge(self, name, password, veripassword, mail, **params):
        have_error = False
        if not valid_username(name) :
            params['error_username'] = "That's not valid username"
            have_error = True

        if not valid_password(password) :
            params['error_password'] = "That's not valid password"
            have_error = True
        elif password != veripassword:
            params['error_verify'] = "That's not equivelent with password"
            have_error = True

        if not valid_email(mail) :
            params['error_email'] = "That's not a valid email"
            have_error = True

        return have_error, params
        # if name:
        #     #Correct
        #     msg1 = ""
        # else:
        #     msg1 = 'Can\'t stay empty '

        # if password:
        #     #Correct
        #     msg2 = ''
        # else :
        #     msg2 = 'Empty password'

        # if veripassword and veripassword != password:
        #     msg3 = 'Different with password'
        # elif  not(veripassword):
        #     msg3 = 'Empty'
        # else :
        #     #Correct
        #     msg3 = ''

        # if  mail:
        #     for each in mail:
        #         if  each == '@':
        #             msg4 = ''
        #             break
        #         else :
        #             msg4 = 'Invalid email address'
        # else:
        #     msg4 = ''

        # return msg1, msg2, msg3, msg4

class Welcome(webapp2.RequestHandler):
    """docstring for Welcome"""
    # def catch(self, name):
    #     self.Welcome.catch.name = name

    def get(self):
        jinja_env = Environment(loader=FileSystemLoader('templates/signup'))
        template = jinja_env.get_template('welcome.html')
        name = self.request.get('name')
        if valid_username(name) :
            self.response.out.write( template.render(name = name) )
        else :
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage), ('/signup', sign), ('/welcome', Welcome)], debug=True)