"""
Apiary dashboard

"""

from apiary import web


class System(web.AuthRequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('interface/pages/system.html')


class Systems(web.AuthRequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('interface/pages/systems.html')
