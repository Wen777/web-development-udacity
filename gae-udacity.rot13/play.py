#-*- coding: utf-8 -*-
import webapp2, cgi

form = """
<form action="" method="post">
    <label for="">
        ROT 13 :
        <br>
        <input type="text" name="text" value="%(text)s">
    </label>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    """docstring for Rot13"""
    def __init__(self, arg):
        pass

class Rot13(webapp2.RequestHandler):
    def write_form(self, out=""):
        self.response.out.write(form % {"text":out})

    def get(self):
        self.write_form()

    def post(self):
        #q = self.request.get('q')
        #self.response.out.write(q)
        #self.repsonse.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)
        user_out= self.request.get('text')
        if user_out:
            # user_out = self.write_form(out)
            #user_out = self.escapeHtml(user_out)
            user_out = self.changeCharacter(user_out)
            user_out = self.escapeHtml(user_out)
            self.response.out.write(form % {"text":user_out})

    def escapeHtml(self, esc):
        esc = cgi.escape(esc, True)
        return esc

    def changeCharacter(self, data):
        return_value = ''
        for test in data :
            if  test.isalpha() and test.isupper() :
                test = self.rotDict(test.lower())
                return_value = return_value + test.upper()
            elif  test.isalpha() and test.islower() :
                test = self.rotDict(test)
                return_value = return_value + test
            else:
                return_value = return_value + test
        if return_value:
            return return_value
        else:
            return data

    def rotDict(self, data):
        #build keys and values for dictionary
        Key = []
        Value = []
        for num in range(97,123):
            Value.append(num)
        for i in range (97,123):
            Key.append(str( unichr( i ) ))
        # set i
        i = 13
        # combine the lists into one dict
        rotdict = dict(zip(Key, Value))
        print rotdict
        # 檢驗
        if data in rotdict :
            if rotdict[data] + i < 123:
                search = rotdict[data] + i
                for Key, Value in rotdict.iteritems():
                    if Value == search:
                        return str( Key )
            else :
                search = rotdict[data] + i - 26
                for Key, Value in rotdict.iteritems():
                    if Value == search:
                        return str( Key )
        else :
            return data

app = webapp2.WSGIApplication([('/', MainPage), ('/rot13', Rot13)], debug=True)

# def main():
#     app.run()

# if __name__ == "__main__":
    # main()