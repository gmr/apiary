
from apiary.interface import auth
from apiary.interface import home

ROUTES = [(r"/", home.Home,),
          (r"/login", auth.Login),
          (r"/logout", auth.Logout)]
