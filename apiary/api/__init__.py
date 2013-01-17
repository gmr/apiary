__author__ = 'gmr'

from apiary.api import distribution

UUID_ID = "(?P<id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"

ROUTES = [("/api/distribution", distribution.Distribution),
          ("/api/distribution/%s" % UUID_ID, distribution.Distribution),
          ("/api/distributions", distribution.Distributions)]
