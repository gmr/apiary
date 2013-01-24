__author__ = 'gmr'

from apiary.api import architecture
from apiary.api import breed
from apiary.api import distribution
from apiary.api import system

from apiary import UUID_RE

ROUTES = [("/api/architecture", architecture.Architecture),
          ("/api/architecture/(?P<name>[\w_\-]*)", architecture.Architecture),
          ("/api/architectures", architecture.Architectures),
          ("/api/breed", breed.Breed),
          ("/api/breed/(?P<name>[\w_\-]*)", breed.Breed),
          ("/api/breeds", breed.Breeds),
          ("/api/distribution", distribution.Distribution),
          ("/api/distribution/%s" % UUID_RE, distribution.Distribution),
          ("/api/distributions", distribution.Distributions),
          ("/api/system", system.System),
          ("/api/system/%s" % UUID_RE, system.System),
          ("/api/systems", system.Systems)]
