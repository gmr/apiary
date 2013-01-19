"""
Apiary dashboard

"""

from apiary import web


class Home(web.InterfaceRequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('interface/pages/home.html')
