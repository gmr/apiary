__author__ = 'gmr'

from apiary.api import architecture
from apiary.api import breed
from apiary.api import distribution

UUID_ID = "(?P<id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"

ROUTES = [("/api/architecture", architecture.Architecture),
          ("/api/architecture/(?P<name>[\w_\-]*)", architecture.Architecture),
          ("/api/architectures", architecture.Architectures),
          ("/api/breed", breed.Breed),
          ("/api/breed/(?P<name>[\w_\-]*)", breed.Breed),
          ("/api/breeds", breed.Breeds),
          ("/api/distribution", distribution.Distribution),
          ("/api/distribution/%s" % UUID_ID, distribution.Distribution),
          ("/api/distributions", distribution.Distributions)]
