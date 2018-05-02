import tornado
from base import BaseHandler

class AuthenticationStaticFileHandler(tornado.web.StaticFileHandler):
    def get(self, path, include_body=True):
        #if not self.get_secure_cookie(BaseHandler.secure_username):
        #    raise tornado.web.HTTPError(403)
        #    #self.set_default_headers()
        #    #self.redirect(self.get_login_url())
        #    return
        self.get(path, include_body)
