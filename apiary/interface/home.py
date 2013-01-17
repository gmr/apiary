"""
File Description

"""

from tornado import web


class Home(web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('interface/base.html')
