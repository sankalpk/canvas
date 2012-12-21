import webapp2
import jinja2
import os
from google.appengine.ext import db
from google.appengine.api import mail

#Main pages are home, about, events, resources


#Jinja templating setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

#Functions
users=['divya','columbia','upenn','jhu','jefferson','bostoncollege','mgh','northeastern']
def valid_username(username):
  return username.lower() in users

def valid_password(password):
  return password=="oohlala"

#HANDLERS
class GenericHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Home(GenericHandler):
  def get(self):
      self.render('home.html')

class About(GenericHandler):
  def get(self):
      self.render('about.html')

class Events(GenericHandler):
  def get(self):
    self.render('events.html')

class Resources(GenericHandler):
  def get(self):
    self.render('resources.html')
class LogoutHandler(GenericHandler):
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    self.redirect('/manuscript')

class AdminView(GenericHandler):
  def get(self):
    userCookie = self.request.cookies.get('user_id')
    if(userCookie[-4:]=="0123" and userCookie[:-4]=="divya"):
      logins= db.GqlQuery("SELECT * FROM UserLogin ORDER BY created DESC")
      self.render("admin.html",logins=logins)
    else:
      self.redirect('/manuscript')

class Signup(GenericHandler):
    def post(self):
        user_address = self.request.get("email_address")

        #if not mail.is_email_valid(user_address):
            # prompt user to enter a valid address
            # You entered an invalid email address.
        #else:
        sender_address = "sankalp221@gmail.com"
        subject = "New Dlist signup"
        body = """
        Someone has just signed up to the dlist. Please add:%s
        """ % user_address

        mail.send_mail(sender_address, "sankalp@cmuspeech.com", subject, body)
        self.render("signup.html",email=user_address)
class DebateTeam(GenericHandler):
  def get(self):
    self.render('debateteam.html')

app = webapp2.WSGIApplication([('/', Home),('/about',About),('/events',Events),('/logout',LogoutHandler),('/resources',Resources), ('/signup',Signup),('/debateteam',DebateTeam)],
                              debug=True)

class UserLogin(db.Model):
  username = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add = True)