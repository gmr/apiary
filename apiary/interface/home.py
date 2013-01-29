"""
Apiary dashboard

"""

from apiary import web


class Home(web.AuthRequestHandler):

    def get(self, *args, **kwargs):
        self.render('interface/pages/home.html')
