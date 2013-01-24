from apiary.interface import auth
from apiary.interface import distribution
from apiary.interface import home
from apiary.interface import system

from apiary import UUID_RE

ROUTES = [(r"/", home.Home,),
          (r"/login", auth.Login),
          (r"/logout", auth.Logout),
          (r"/settings/distribution/%s" % UUID_RE, distribution.Distribution),
          (r"/settings/distributions", distribution.Distributions),
          (r"/system/%s" % UUID_RE, system.System),
          (r"/systems", system.Systems)]
