#-*- coding: utf-8 -*-
import cgi, webapp2, urllib

form = """
<form action="" method="post">
    <label for="test">
        URL adapter <hr> <input type="text" name="test" value="%(test)s">
    </label>
    <label for="sub"> <input type="submit" name="sub"> </label>
</form>
"""

class twclJudge(webapp2.RequestHandler):
    """docstring for twclJudge"""

    def write_form(self):
        self.response.out.write(form % {"test": ""})

    def get(self):
        self.write_form()

    def post(self):
        URLS = self.request.get("test")
        msg = self.urlJudge(URLS)
        self.response.out.write(form % {"test": ""})
        self.response.out.write("<br>%s" % msg)

    def urlJudge(self, URLS):
        if URLS:
            URLS = cgi.escape(str(URLS))
            condition = urllib.urlopen(URLS)
        else:
            msg = "Error, try another url"
            return msg

        if condition.getcode() == 200:
            msg = "It's correct."
            return msg
        elif condition.getcode() == 404:
            msg = "404 error, try another url."
            return msg
        else:
            msg = "Error, try another url"
            return msg

app = webapp2.WSGIApplication([('/twclJudge', twclJudge)], debug=True)