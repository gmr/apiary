"""
Apiary dashboard

"""

from apiary import web


class Distribution(web.AuthRequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('interface/pages/distribution.html')


class Distributions(web.AuthRequestHandler):

    @web.authenticated
    def get(self, *args, **kwargs):
        self.render('interface/pages/distributions.html')
