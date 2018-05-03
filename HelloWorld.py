# 引入tornado包中的ioloop和web类。该类是Tornado程序的基础
import tornado.ioloop
import tornado.web

#  实现一个web.RequestHandler子类，重载其中的get()函数，该函数负责相应定位到该RequestHandler的HTTP GET请求的处理。
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello world")

#  定义了make_app()函数，该函数返回一个web.Application对象。第一个参数用于定义Tonardo程序的路由映射。本例将对根URL的访问映射到了RequestHandler子类MainHandler中。
# 路由解析：路由字符串有两种：固定字串路径和参数字串路径。
# 1.固定字串路径
# Handlers = [
#   ("/", MainHandler),                 # 只匹配根路径
#   ("/entry", EntryHandler),           # 只匹配/entry
#   ("/entry/2018", Entry2018Handler),  # 只匹配/entry/2018
# ]
# 2.参数字串路径
# handlers = [
#   (r"/entry/([^/]+)", EntryHandler),   # 以/entry/开头的URL
# ]
# 3.带默认值得参数路径
# 2中的例子是无法匹配http://xx.xx.xx.xx/entry
# 需要修改方法URL路径和get()函数的定义：
# handlers = [
#   (r"/entry/([^/]*)", EntryHandler),
# ]
# class EntryHandler(tornado.web.RequestHandler):
#   def get(self, slug = 'default'):
#     entry = self.db.get("select * from entries where slug = %s", slug)
#     if not entry:
#       raise tornado.web.HTTPError(404)
#     self.render("entry.html", entry = entry)
# 首先用星号取代加号，然后为RequestHandler子类的get()函数的slug参数配置了默认值default
# 4.多参数路径
# 参数路径允许在一个URL模式中定义多个可变参数
# handlers = [
#   (r'/(\d{4})/(\d{2})/(\d{2})/([a-zA-Z\-0-9\.:,_]+)/?', DetailHandler)
# ]
# class DetailHandler(tornado.web.RequestHandler):
#   def get(self, year, month, day, slug):
#     self.write("%d-%d-%d %s"%(year, month, day, slug))
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
  ])

def main():
  app = make_app()
  # 用web.Application.listen()函数指定服务器监听的端口
  app.listen(8800)
  # 用tornado.ioloop.IOLoop.current().start()启动IOLoop，该函数将一直运行且不退出，用户处理完所有客户端的访问请求。
  tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()

# RequestHandler
# 1.接入点函数
# 需要子类继承并定义具体行为的函数在RequestHandler中被称为接入点函数（Entry Point）如get()函数
#   (1).RequestHandler.initialize()
#   该类实现RequestHanlder子类实例的初始化进程，可以为该函数传递参数，参数来源于配置URL映射时的定义，如
#   from tornado.web import RequestHandler
#   from tornado.web import Application
#   class ProfileHandler(RequestHandler):
#     def initialize(self, database):
#       self.database = database
    
#     def get(self):
#       pass

#     def post(self):
#       pass

#   app = Application([
#     (r'/account', ProfileHandler, dict(database="c:\\example.db")),
#   ])

#   (2).RequestHandler.prepare()、RequestHandler.on_finish()
#   prepare()方法用于调用请求处理（get、post等）方法之前的初始化处理。通常该方法做资源初始化操作
#   on_finish()用于请求处理结束后的一些清理工作。通常该方法可做清理对象占用的内存或者关闭数据库连接等工作。对于同步处理程序会在get()（等）后立即返回；对于异步处理程序，会在调用finish()后返回。
#   (3).HTTP Action处理函数
#   每个HTTP Action在RequestHandler中都以单独的函数进行处理
#   RequestHandler.get(*args, **kwargs)
#   RequestHandler.post(*args, **kwargs)
#   RequestHandler.head(*args, **kwargs)
#   RequestHandler.delete(*args, **kwargs)
#   RequestHandler.patch(*args, **kwargs)
#   RequestHandler.put(*args, **kwargs)
#   RequestHandler.options(*args, **kwargs)
# 2.输入捕获
#   旨在RequestHandler中用于获取客户端输入的工具函数和属性，比如获取URL查询字符串，Post提交参数等
#   (1).RequestHandler.get_argument(name)、RequestHandler.get_arguments(name) 都是返回给定参数的值。get_argument获得单个值；get_arguments针对参数存在多个值得情况下使用的，返回多个值得列表
#   用get_argument/get_arguments()方法获取的是URL查询字符串与Post提交参数的参数合集
#   (2).RequestHandler.get_query_argument(name)、RequestHandler.get_query_arguments(name) 仅从URL查询参数中获取参数值
#   (3).RequestHandler.get_body_argument(name)、RequestHandler.get_body_arguments(name) 仅从Post提交参数中获取参数值
#   (4).RequestHandler.get_cookie(name, default=None) 根据Cookie名称获取Cookie值
#   (5).RequestHandler.request 返回tornado.httputil.HTTPServerRequest对象实例的属性，通过该对象可以获取关于HTTP请求的一切信息，常用的对象属性
#   method--HTTP请求方法，如GET、POST等
#   uri--客户端请求的uri的完整内容
#   path--uri路径名，即不包括查询字符串
#   query--uri中的查询字符串
#   version--客户端发送请求时使用的HTTP版本，如HTTP/1.1
#   headers--以字典方式表达的HTTP headers
#   body--以字符串方式表达的HTTP消息体
#   remote_ip--客户端的IP地址
#   protocol--请求协议，比如HTTP、HTTPS
#   host--请求消息中的主机名
#   arguments--客户端提交的所有参数
#   files--以字典方式表达的客户端上传的文件，每个文件名对应一个HTTPFile
#   cookies--客户端提交的Cookies字典
#   (6).write_error 输出对错误页面使用的HTML
#   (7).on_connection_close 当客户端断开时被调用；应用程序可以检测这种情况，并中断后续处理，注意这不能保证一个关闭的连接及时被发现
#   (8).get_user_locale 返回Locale对象给当前用户使用
# 3.输出相应函数
#   指一组客户端生成处理结果的工具函数，开发者调用它们以控制URL的处理结果。
#   (1).RequestHandler.set_status(status_code, reason=None) 设置HTTP Response中的返回码。
#   (2).RequestHandler.set_header(name, value) 以键值对的方式设置HTTP Response中的HTTP头参数。使用该配置的Header值将覆盖之前配置的Header
#   (3).RequestHandler.add_header(name, value) 以键值对的方式设置HTTP Response中的HTTP头参数。不会覆盖之前配置的Header，即可以重复
#   (4).RequestHandler.write(chunk) 将给定的块作为HTTP Body发送给客户端一般情况下，本函数输出字符串给客户端。如果给定的块是一个字典，则会将这个块以JSON格式发送给客户端，同时将HTTP Header 中的Content_type设置为application/json
#   (5).RequestHandler.finish(chunk=None) 通知Tornado.Response的生成工作已完成，调用后，Tornado将向客户端发送HTTP Response。本方法适用于对RequestHandler的异步请求处理
#       注意：在同步或协程访问处理的函数中，无需调用finish()
#   (6).RequestHandler.render(template_name, **kwargs) 用给定的参数渲染模板，可以在本函数中传入模板文件名称和模板参数，如
#       import tornado.web
#       class MainHandler(tonardo.web.RequestHandler):
#         def get(self):
#           items = ["python", "C++", "Java"]
#           self.render("template.html", title="Tornado Templates", item=items)
#   (7).RequestHandler.redirect(url, permanent=False, status=None) 进行页面重定向。可以随时调用
#   (8).RequestHandler.clear() 清空所有在本次请求中之前写入的Header和Body内容
#   (9).RequestHandler.set_cookie(name, value)
#   (10).RequestHandler.clear_all_cookies(path="/", domain=None)
# 异步化及协程化
#   同步的方法处理用户的请求，即在RequestHandler的get()或post()等函数中完成所有处理，当退出get()、post()等函数后马上向客户端返回Response。
#   但在处理逻辑比较复杂或需要等待外部IO时，该机制容易造成阻塞服务器线程，并不适合大量客户端的高并发请求场景
#   有两种方式可改变同步的处理流程
#   1.异步化：针对RequestHandler的处理函数使用@tornado.web.asynchronous修饰器，将默认的同步机制改为异步机制
#   2.协程化：针对RequestHandler的处理函数使用@tornado.gen.coroutine修饰器，将默认的同步机制改为携程机制

#   异步化例子
#   import tornado.web
#   import tornado.httpclient
#   class MainHandler(tornado.web.RequestHandler):
#     # 当get()函数返回时，对该HTTP访问的请求尚未完成，所以Tornado无法发送HTTP Response给客户端。
#     # 只有当在随后的on_response()中的finish()函数被调用时，Tornado才知道本次处理已完成，可以发送Response给客户端
#     @tonardo.web.asynchronous
#     def get(self):
#       http = tornado.httpclient.AsyncHTTPClient()
#       http.fetch("http://www.baidu.com", callback=self.on_response)

#     def on_response(self, response):
#       if response.error: raise tornado.web.HTTPError(500)
#       self.write(response.body)
#       self.finish()
  
#   协程化例子：(结合了同步处理和异步处理的优点，使得代码清晰易懂，又能适应海量的客户端的高并发请求)
#   import tornado.web
#   import tornado.httpclient
#   class MainHandler(tornado.web.RequestHandler):
#     # 协程关键技术点
#     # 1.用tornado.gen.coroutine装饰MainHandler的get()、post()等处理函数
#     # 2.使用异步对象处理耗时操作，比如本例的AsyncHTTPClient
#     # 3.调用yield关键字获取异步对象的处理函数
#     @tornado.gen.coroutine
#     def get(self):
#       http = tornado.httpclient.AsyncHTTPClient()
#       response = yield http.fetch("http://www.baidu.com")
#       self.write(response.body)
# 用户身份验证框架
# 1.安全Cookie机制
#   在Tornado中使用RequestHandler.get_cookies()、RequestHandler.set_cookie()可以方便地对Cookie进行读写
#   在实际应用中，Cookie经常用户保存Session信息
#   因为Cookie总是被保存在客户端，所以如何保证其不被篡改是服务器程序必须解决的问题。Tornado提供了Cookie信息加密的机制，使得客户端无法随意解析和修改Cookie的键值
#   例子：
#   import tornado.web
#   import tornado.ioloop
#   session_id = 1
#   class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#       global session_id
#       if not self.get_secure_cookie("session"):
#         self.set_secure_cookie("session", str(session_id))
#         session_id = session_id + 1
#         self.write("Your session got a new session")
#       else:
#         self.write("Your session was set!")

#   application = tornado.web.Application([
#     ('r"/", MainHandler'),
#   ], cookie_secret = "SECRET_DONT_LEAK")

#   def main():
#     application.listen(8888)
#     tornado.ioloop.IOLoop.current().start()

#   if __name__ == "__main__":
#     main()
#   注意：cookie_secret参数值是Cookie的加密秘钥，需要做好保护工作，不能泄露
# 2.用户身份认证
#   RequestHandler类中有一个current_user属性用于保存当前请求的用户名。默认值为None，在get()、post()等处理函数中可以随时读取该属性以获取当前的用户名。
#   RequestHandler.current_user是一个只读属性，需要重载RequestHandler.get_current_user()函数以设置该属性值
#   例子：

#   import tornado.web
#   import tornado.ioloop
#   import uuid

#   dict_sessions = {}

#   class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#       session_id = self.get_secure_cookie("session_id")
#       return dict_sessions.get(session_id)

#   class MainHandler(BaseHandler):
#     # 需要身份认证才能访问的处理器
#     @tornado.web.authenticated
#     def get(self):
#       name = tornado.escape.xhtml_escape(self.current_user)
#       self.write("Hello," + name)

#   class LoginHandler(BaseHandler):
#     def get(self):
#       self.write('<html><body>'
#                   '<form action="/login" method="post">'
#                     'Name: <input type="text" name="name">'
#                     '<input type="submit" value="Sign in">'
#                   '</form>'
#                 '</html></body>')
    
#     def post(self):
#       if len(self.get_argument("name"))<3:
#         self.redirect("/login")
#       session_id = str(uuid.uuid1())
#       dict_sessions[session_id] = self.get_argument("name")
#       self.set_secure_cookie("session_id", session_id)
#       self.redirect("/")
  
#   application = tornado.web.Application([
#     (r"/", MainHandler),
#     (r"/login", LoginHandler),
#   ], cookie_secret = "SECRET_DONT_LEAK", login_url: "/login")

#   def main():
#     application.listen(8888)
#     tornado.ioloop.IOLoop.current().start()

#   if __name__ = "__main__":
#     main()
#   商用的用户身份认证还要完善更多的内容，比如加入密码验证机制、管理登录超时、将用户信息保存到数据库等
# 3.防止跨站攻击（Cross-site request forgery, CSRF 或 XSRF）
#   通过CSRF，攻击者可以冒用用户的身份，在用户不知情的情况下执行恶意操作
#   攻击过程：
#   第一步，用户首先访问存在CSRF漏洞的网站Sites1，成功登陆并获取到了Cookie。此后，所有该用户对site1的访问均会携带Site1的Cookie，因此被Site1认为是有效操作
#   第二步，此时用户又访问了带有攻击行为的站点Site2，Site2的返回页面中带有一个访问Site1进行恶意操作的链接，但被伪装成了合法内容
#   第三步，用户点击恶意链接，在不知情的情况下向Site1站点发送了请求，恶意站点的目的达到。

#   用Tornado防范CSRF攻击
#     要求每个请求包括一个参数值作为令牌来匹配存储在Cookie中的对应值
#     Tornado应用可以通过一个Cookie头和一个隐藏的HTML表单元素向页面提供令牌。这样，当一个合法页面的表单 被提交时，它将包括表单值和已存储的Cookie。如果两者匹配，则Tornado应用认定请求有效

#     开启Tornado的CSRF防范功能需要两个步骤
#     步骤一，在实例化tornado.web.Application时传入xsrf_cookies = True 参数，即
#     application = tornado.web.Application([
#       (r'/', MainHandler),
#       (r'/purchase', PurchaseHandler),
#     ], cookie_secret = "DONT_LEAK_SECRET", xsrf_cookies = True)
#     或者
#     settings = {
#       "cookie_secret": "DONT_LEAK_SECRET",
#       "xsrf_cookies": True
#     }
#     application = tornado.web.Application([
#       (r'/', MainHandler),
#       (r'/purchase', PurchaseHandler),
#     ], **settings)
#     步骤二，在每个具有HTML表单的模板文件中，为所有表单添加xsrf_form_html()函数标签，如
#     <form aciton="/login" method="post">
#       {% module xsrf_form_html() %}
#       <input type="text" name="message" />
#       <input type="submit" value="Post" />
#     </form>
# 调试模式
#   1.自动加载
#   通过向Application实例传入参数debug=True，可以将程序以调试模式启动。如
#   def make_app():
#     return tornado.web.Application([

#     ], debug = True)
#   便利之处：
#     (1).自动加载：对项目中的任何*.py源文件的修改将自动重启并加载修改后的代码文件
#     (2).错误追溯：当RequestHandler处理用户访问出现异常时，系统的错误信息调用栈将被推送到浏览器中，使得调试者可以马上查找错误的根源
#     (3).禁用模板缓存
#   2.Ctrl+C 退出机制
#   默认情况下，Tornado的IOLoop不会相应Linux控制台的Ctrl+C命令，导致程序无法便捷的退出运行
#   def main():
#     app = make_app()
#     app.listen(8888)
#     try:
#       tornado.ioloop.IOLoop.current().start()
#     except KeyboardInterrupt:
#       tornado.ioloop.IOLoop.current().stop()

#     print "Program exit!"
#   这样在控制台发送了Ctrl+C请求后，程序可有机会回收系统的其他资源并退出执行
#   注意：在Window平台中，产生KeyboardInterrupt中断的方式是Ctrl+Pause
# 静态文件
#   1.配置静态文件URL路径与服务器本地路径的关联关系
#     Tornado提供了两种方式进行配置静态文件URL与服务器本地路径的关联关系
#     (1)static目录配置
#     在tornado.web.Application的构造函数中可以传入static_path参数，用于配置对URL路径http://mysite.com/static 中文件的本地路径，如
#     def make_app():
#       return tornado.web.Application([

#       ], static_path = "C:\\www\\\static")
#     通常这些静态文件的目录与网站的代码文件有某种相对关联关系，可以通过下面这样的方式将该参数设置为相对路径：
#     import os
#     def make_app():
#       return tornado.web.Application([

#       ], static_path = os.path.join(os.path.dirname(__file__), "static"))
#     (2)StaticFileHandler配置
#     如果除了http://mysite.com/static 目录还有其他存放静态文件的URL，则可以用RequestHandler的子类StaticFileHandler进行配置，如
#     def make_app():
#       return tornado.web.Application([
#         (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': 'assets/css'}),
#         # 以下除了映射外，还配置了default_filename参数，即当用户访问了http://mysite.com/js 目录本身时，将返回template/index.html文件
#         (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': 'assets/js', 'default_filename': 'template/index.html'}),
#       ], static_path = 'c:\\www\\static')
#   2.优化静态文件访问
#     优化静态文件访问的目的在于减少静态文件的重复传送，提高网络及服务器的利用率，通过在模板文件中用static_url方法修饰静态文件链接可以达到这个目的，如
#     <div>
#       <img src="{{ static_url('images/logo.png') }}" />
#     </div>
#     此时会将图像链接设置为后面带上hash值，用于缓存。
# websocket
#   原理：在客户端与服务器之间建立TCP持久链接，从而使得当服务器有消息需要推送给客户端时能够进行即时通信。
#   其HTTP Request包为：
#     GET /stock_info/?encoding=text HTTP/1.1
#     Host: echo.websocket.org
#     Origin: http://websocket.org
#     Cookie: __token=ubcxx13
#     # 以下是websocket建立链路的核心，告诉Web服务器：客户端希望建立一个WebSocket连接，客户端使用的WebSocket版本是13，秘钥是uRovscZjNo1/umbTt5uKmw==
#     Connection: Upgrade
#     Sec-WebSocket-key: uRovscZjNo1/umbTt5uKmw==
#     Upgrade: websocket
#     Sec-WebSocket-Version: 13
#   服务器在收到该Request后，如果同意建立WebSocket连接则返回Response，如下
#     HTTP/1.1 101 WebSocket Protocol Handshake
#     Date: Fri, 10 Feb 2012 17:38:18 GMT
#     Connection: Upgrade ------
#     Server: Kaazing Gateway
#     Upgrade: WebSocket ------
#     Access-Control-Allow-Origin: http://websocket.org
#     Access-Control-Allow-Credentials: true
#     Sec-WebSocket-Accept: rLHCkw/SKs09GAH/ZSFhBATDKrU= ------
#     Access-Control-Allow-Headers: content-type
#     ------是与WebSocket相关的Header信息
#     其中Sec_WebSocket-Accept是将客户端发送的Sec-WebSocket-Key加密后产生的数据，以让客户端确认服务器能够正常工作
#   Tornado定义了tornado.websocket.WebSocketHandler类用于处理WebSocket链接的请求，应用开发者应该继承该类实现其中的open()、on_message()、on_close()函数
#     自动调用的三个函数
#     (1)WebSocketHandler.open() 在一个新的WebSocket链接建立时，Tornado框架会调用此函数。一样可以在get()、post()等函数中一样用get_argument()函数获取客户端提交的参数，以及用get_secure_cookie/set_secure_cookie操作Cookie等
#     (2)WebSocketHandler.on_message(message) 建立WebSocket连接后，当收到来自客户端的消息时，Tornado框架会调用本函数，通过解析收到的消息作出相应的处理
#     (3)WebSocketHandler.on_close() 当WebSocket连接被关闭时，Tornado框架会调用本函数。可以通过访问self.close_code和self.close_reason查询关闭的原因
#     开发者主动操作WebSocket的两个函数
#     (4)WebSocketHandler.write_message(message, binary=False) 用于向与本链接相对应的客户端写消息
#     (5)WebSocketHandler.close(code=None, reason=None) 主动关闭WebSocket连接。其中的code和reason用于告诉客户端连接被关闭的原因。参数code必须是一个数值，reason是一个字符串
#   例子
#   import tornado.ioloop
#   import tornado.web
#   import tornado.websocket
#   from tornado.options import define, options, parse_command_line

#   define("port", default=8888, help="run on the given port", type=int)
#   # 定义了全局变量字典client，用于保存所有与服务器建立WebSocket链接的客户端信息。
#   # 字典的键是客户端id，值是一个由id与相应的WebSocketHandler实例构成的元组（Tuple）
#   clients = dict() # 客户端Session字典
#   # 一个普通的页面处理器，用于向客户端渲染主页index.html
#   class IndexHandler(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     def get(self):
#       self.render("index.html")
#   # 核心处理器。
#   # 继承自tornado.websocket.WebSokectHandler。
#   # 其中的open()函数将所有客户端链接保存到clients字典中
#   #      on_message()用于显示客户端发来的消息
#   #      on_close()用于将已经关闭的WebSocket链接从clients字典中移除
#   class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
#     def open(self, *args):
#       self.id = self.get_argument("id")
#       self.stream.set_nodelay(True)
#       clients[self.id] = {"id": self.id, "object": self} # 保存Session到clients字典中

#     def on_message(self, message):
#       print "Client %s received a message: %s" % (self.id, message)

#     def on_close(self):
#       if self.id in clients:
#         del clients[self.id]
#         print "Client %s is closed" % (self.id)

#     def check_origin(self, origin):
#       return True

#   app = tornado.web.Application([
#     (r'/', IndexHandler),
#     (r'/websocket', MyWebSocketHandler),
#   ])

#   import threading
#   import time

#   # 启动单独的线程运行此函数，每隔1秒向所有的客户端推送当前时间
#   def sendTime():
#     import datetime
#     while True:
#       for key in clients.keys():
#         msg = str(datetime.datatime.now())
#         clients[key]["object"].write_message(msg)
#         print "write to client %s: %s" % (key, msg)
#       time.sleep(1)

#   if __name__ = '__main__':
#     threading.Thread(target=sendTime).start() # 启动推送时间线程
#     parse_command_line()
#     app.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()

# 客户端：
#   在js中通过 var socket = new WebSocket(url); 来初始化WebSocket对象
#   在代码中只需给WebSocket构造函数传入服务器的URL地址，如http://mysite.com/point,可以为该对象的如下时间指定处理函数以响应他们
#   (1)WebSocket.onopen: 在WebSocket链接建立时
#   (2)WebSocket.onmessage: 发生在收到了来自服务器的消息时
#   (3)WebSocket.onerror: 发生在通信过程中有任何错误时
#   (4)WebSocket.onclose: 发生在与服务器的链接关闭时
#   除了以上，还可以通过WebSocket对象的两个方法主动操作
#   (5)WebSocket.send(data): 向服务器发送信息
#   (6)WebSocket.close(): 主动关闭现在链接
# 客户端WebSocket例子：
#   <body>
#     <a href="jacascript:WebSocketTest()">Run WebSocket</a>
#     <div id="messages"></div>
#   </body>

#   <script>
#     var messageContainer = document.getElementById("messages");
#     function WebSocketTest() {
#       if ("WebSocket" in window) {
#         messageContainer.innerHTML = "WebSocket is supported by your Browser!";
#         var ws = new WebSocket("ws://localhost:8888/websocket?Id=12345");
#         ws.onopen = function() {
#           ws.send("Message to send");
#         };
#         ws.onmessage = function(evt) {
#           var received_msg = evt.data;
#           messageContainer.innerHTML += "<br/>Message is received:" + received_msg;
#         };
#         ws.onclose = function() {
#           messageContainer.innerHTML += "<br/>Connection is closed...";
#         };
#       } else {
#         messageContainer.innerHTML = "WebSocket NOT supported by your Browser!";
#       }
#     }
#   </script>