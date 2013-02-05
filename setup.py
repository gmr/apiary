import os
import sys
from platform import python_version_tuple
from distutils.core import setup

base_path = '%s/apiary' % sys.prefix

data_files = dict()
data_paths = ['static', 'templates', 'etc']
for data_path in data_paths:
    for dir_path, dir_names, file_names in os.walk(data_path):
        install_path = '%s/%s' % (base_path, dir_path)
        if install_path not in data_files:
            data_files[install_path] = list()
        for file_name in file_names:
            data_files[install_path].append('%s/%s' % (dir_path, file_name))

with open('MANIFEST.in', 'w') as handle:
    for path in data_files:
        for filename in data_files[path]:
            handle.write('include %s\n' % filename)

console_scripts = ['apiary=apiary.tools.cli:main',
                   'apiaryd=apiary.server.daemon:main']

packages = ['apiary',
            'apiary.api',
            'apiary.mappers',
            'apiary.server',
            'apiary.tools']

install_requires = ['clihelper',
                    'lxml',
                    'msgpack-python',
                    'python-ldap',
                    'requests',
                    'sqlalchemy>=0.8',
                    'tornado']

tests_require = ['mock', 'nose']

if float('%s.%s' % python_version_tuple()[0:2]) < 2.7:
    install_requires.append('argparse')
    tests_require.append('unittest2')

setup(name='apiary',
      version='0.0.1',
      description=('Apiary is a modern data-center management tool that '
                   'includes provisioning, configuration management and '
                   'inventory control.'),
      url='https://github.com/gmr/apiary',
      packages=packages,
      author='Gavin M. Roy',
      author_email='gmr@meetme.com',
      license='BSD',
      install_requires=install_requires,
      tests_require=tests_require,
      entry_points={'console_scripts': console_scripts})
