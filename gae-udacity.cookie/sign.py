import re
from google.appengine.ext import db
import workdb

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

#Hash function
def hashVal(val):
    return ("%s|%s") % ( val, hashlib.sha256(val).hexdigest() )
#query user name
def queryUserAccount():
    return db.GqlQuery('SELECT * FROM UserModel ORDER BY created DESC')

def judge(**params):
    have_error = False

    if not valid_username(params['name']) :
        params['error_username'] = "That's not valid username"
        have_error = True

    if not valid_password(params['pw']) :
        params['error_password'] = "That's not valid password"
        have_error = True

    if params.get("signState", "invalid") == "signin":
        # If True, must be signin, check db
        #Two methods to make user account querried. One is db.Gql, another is db.get
        queryVal = queryUserAccount()
        #print queryVal
        #print type(queryVal)
        for query in queryVal:
            print query.username
            if query.username == params['name'] and query.userpw.split("|")[0] == params['pw']:
                print "ok"
                break
            elif query.username != params['name'] and query.userpw != params['pw']:
                params['error_message'] = "That's not valid username or password"
                have_error = True
        #Second way, failure way !!!!
        #queryVal = db.Key.from_path("UserModel", str(params['name']),parent=workdb.user_model_key())

    elif params.get("signState", "invalid") == "signup":
        # If True, must be signup, check db
        if params['pw'] != params['verifypw']:
            params['error_verify'] = "That's not equivelent with password"
            have_error = True

        if params['mail']:
            if not valid_email(params['mail']) :
                params['error_email'] = "That's not a valid email"
                have_error = True

    return have_error, params