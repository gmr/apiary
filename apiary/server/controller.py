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

    def log_request(self, handler):
        """Writes a completed HTTP request to the logs.

        By default writes to the python root logger.  To change
        this behavior either subclass Application and override this method,
        or pass a function in the application settings dictionary as
        'log_function'.
        """
        if handler.get_status() < 400:
            log_method = LOGGER.info
        elif handler.get_status() < 500:
            log_method = LOGGER.warning
        else:
            log_method = LOGGER.error
        request_time = 1000.0 * handler.request.request_time()
        log_method("%d %s %.2fms", handler.get_status(),
                   handler._request_summary(), request_time)

    def _application_settings(self):
        """Return a dictionary of settings that are valid for a
        tornado.web.Application and a dictionary of configuration values for
        apiary from the Application section of the config file.

        :return dict, dict: Tornado Settings, Apiary Configuration

        """
        # Create a dictionary to hold the two types of config values
        settings = dict(self._get_application_config())
        config = dict()

        # Assign any non-Tornado item to the config dict, removing from settings
        for key in settings.keys():
            if key not in TORNADO_SETTINGS:
                config[key] = settings[key]
                del settings[key]

        # Always disable xsrf_cookies by default
        settings['xsrf_cookies'] = False
        settings['log_function'] = self.log_request

        return settings, config

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
        settings, config = self._application_settings()

        # Create the web application
        self._application = web.Application(self._get_routes(), **settings)

        # Start the HTTP Server
        self._application.listen(**self._httpd_config)

        # If translations are provided, load them
        if 'locale_path' in settings:
            locale.load_translations(settings['locale_path'])

        # Assign the config to an apiary attribute of the application
        self._application.apiary_config = config

        # Create the database session
        self._application.database = self._new_db_session()

        LOGGER.info('Apiary %s HTTP service started on port %s',
                    apiary.__version__, self._httpd_config['port'])


def main():
    clihelper.setup('apiaryd', apiary.__doc__.strip(), apiary.__version__)
    clihelper.run(ApiaryController)
