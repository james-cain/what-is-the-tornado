import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
# local module
from handlers.patterns import url_patterns
from restful_api.resource_handlers import ResourceHandlers
from restful.rest import RestService
from handlers.static_file_handler_impl import AuthenticationStaticFileHandler

define('port', default=8080, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "web/react-cain/build"),
            static_path=os.path.join(os.path.dirname(__file__), "web/react-cain/build"),
            debug=True,
            login_url='/login',
            cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
        )
        super(Application, self).__init__(url_patterns, **settings)

def GetRestfulApp():
    settings = dict(
        #template_path=os.path.join(os.path.dirname(__file__), "web/react-cain/build"),
        #static_path=os.path.join(os.path.dirname(__file__), "web/react-cain/build"),
        login_url='/login',
        cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
#        xsrf_cookies=True,
    )
    return RestService(ResourceHandlers, handlers=url_patterns, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(GetRestfulApp())
    http_server.listen(options.port)

    # use wechatpy to do this work.
    #wxShedule = WxShedule()
    #3wxShedule.excute()
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
