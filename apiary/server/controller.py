"""
Apiary Services Daemon Controller

"""
import clihelper
from tornado import ioloop
import logging
from tornado import locale
from sqlalchemy import orm
import sqlalchemy
from tornado import web

import apiary
from apiary import api
from apiary import interface

LOGGER = logging.getLogger(__name__)
SQLITE_DEFAULT_FILE = 'data/apiary.sqlite3'
TORNADO_SETTINGS = ['debug', 'gzip', 'log_function', 'ui_modules', 'ui_methods',
                    'cookie_secret', 'login_url', 'autoescape',
                    'template_path', 'template_loader', 'static_path',
                    'static_url_prefix', 'static_handler_class',
                    'static_handler_args']


class ApiaryController(clihelper.Controller):

    HTTP_PORT = 8000

    def run(self):
        """The core method for starting the application. Will setup logging,
        toggle the runtime state flag, block on loop, then call shutdown.

        """
        LOGGER.debug('Process running')
        self._setup()
        self._set_state(self._STATE_RUNNING)
        try:
            self._ioloop.start()
        except KeyboardInterrupt:
            LOGGER.debug('Caught CTRL-C, shutting down')
        if self.is_running:
            self._shutdown()

    @property
    def _application_settings(self):
        """Return a dictionary of settings that are valid for a
        tornado.web.Application from the configuration file Application
        settings.

        :rtype: dict

        """
        config = dict(self._get_application_config())
        for key in config.keys():
            if key not in TORNADO_SETTINGS:
                del config[key]
        config['xsrf_cookies'] = False
        return config

    def _get_routes(self):
        """Return the routes from the API and Interface packages

        :rtype: list

        """
        return tuple(api.ROUTES + interface.ROUTES)

    @property
    def _httpd_config(self):
        """Return a dictionary that will be used as kwargs for a new instance
        of a HTTPServer.

        :rtype: dict

        """
        config = self._get_config('httpd')
        return {'port': config.get('port', self.HTTP_PORT),
                'no_keep_alive': config.get('no_keep_alive', False),
                'xheaders': config.get('xheaders', False),
                'ssl_options': config.get('ssl_options', None)}

    def _new_db_session(self):
        """Return a new SQLAlchemy session

        :rtype: sqlalchemy.orm.session.Session

        """
        Session = orm.sessionmaker(bind=self._sqlalchemy_engine)
        LOGGER.debug('Returning a new SQLAlchemy session')
        return Session()

    def _setup(self):
        """This method is called when the cli.run() method is invoked."""
        self._ioloop = ioloop.IOLoop.instance()
        self._start_httpd()

    def _shutdown(self):
        self._set_state(self._STATE_SHUTTING_DOWN)
        self._ioloop.stop()

    @property
    def _sqlalchemy_engine(self):
        """Return an instance of a SQLAlchemy engine that is determined by the
        configuration.

        :rtype: sqlalchemy.engine.Engine
        :raises: ValueError

        """
        config = self._get_config('database')
        backend = config.get('backend', 'sqlite')
        if backend == 'sqlite':
            db_file = config.get('file', SQLITE_DEFAULT_FILE)
            LOGGER.debug('Creating new sqlite engine: %s', db_file)
            return sqlalchemy.create_engine('sqlite:///%s' % db_file)
        raise ValueError('Unsupported SQLAlchemy backend: %s', backend)

    def _start_httpd(self):
        """Start the Tornado web application, creating the HTTPD server and
        passing in configuration as settings to the web Application

        """
        self._application = web.Application(self._get_routes(),
                                            **self._application_settings)
        self._application.listen(**self._httpd_config)
        config = self._get_application_config()
        if 'locale_path' in config:
            locale.load_translations(config['locale_path'])
        self._application.database = self._new_db_session()
        LOGGER.info('Apiary %s HTTP service started on port %s',
                    apiary.__version__, self._httpd_config['port'])

def main():
    clihelper.setup('apiaryd', apiary.__doc__.strip(), apiary.__version__)
    clihelper.run(ApiaryController)
