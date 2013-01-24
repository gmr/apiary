"""
Temporary setup file

"""
import logging
from sqlalchemy import create_engine
from sqlalchemy import orm
import os
import yaml

from apiary.mappers import Base
from apiary.mappers import architecture
from apiary.mappers import breed
from apiary.mappers import distribution
from apiary.mappers import profile
from apiary.mappers import session
from apiary.mappers import system
from apiary.mappers import nic


DEFAULTS_PATH = 'templates/defaults.yaml'
LOGGER = logging.getLogger(__name__)

def main(database_name):
    if not database_name:
        raise ValueError('Missing database_name')

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname) -10s %(message)s")

    defaults = dict()
    if os.path.exists('templates/defaults.yaml'):
        LOGGER.info('Loading defaults from %s', DEFAULTS_PATH)
        with open(DEFAULTS_PATH, 'r') as handle:
            defaults = yaml.load(handle)

    LOGGER.info('Creating database: %s', database_name)
    engine = create_engine('sqlite:///%s' % database_name, echo=False)

    Session = orm.sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    for arch in defaults.get('architectures'):
        LOGGER.info('Adding %s to available distribution architectures', arch)
        session.add(architecture.Architecture(arch))

    for value in defaults.get('breeds'):
        LOGGER.info('Adding %s to available distribution breeds', value)
        session.add(breed.Breed(value))

    d = distribution.Distribution(name='CentOS-6.3-x86_64',
                                  version='6.3',
                                  breed='redhat',
                                  architecture='x86_64',
                                  kernel='images/pxeboot/vmlinuz',
                                  initrd='images/pxeboot/initrd.img',
                                  kernel_options='ksdevice=bootif '
                                                 'printk.time=1')
    session.add(d)
    session.commit()

    p = profile.Profile(name='CentOS 6.3 x86-64', distribution=d.name)
    session.add(p)
    p2 = profile.Profile(name='CentOS 6.3 x86-64 Seamicro',
                         distribution=d.name,
                         parent = p.name,
                         kernel_options="nohardwareclock=true")
    session.add(p2)
    session.commit()


    LOGGER.info('Database created and defaults populated')

    with open('templates/apiary.yaml') as handle:
        config = yaml.load(handle.read())
    config['Application']['database']['file'] = database_name
    with open('etc/apiary.yaml', 'w') as handle:
        handle.write(yaml.dump(config, version=(1,2), allow_unicode=True,
                               default_flow_style=False, width=120))
    LOGGER.info('Default configuration written to etc/apiary.yaml')


if __name__ == '__main__':
    main(sys.argv[1] or '/etc/apiary/apiary.sqlite3')
