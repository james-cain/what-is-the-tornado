import tornado.ioloop
import tornado.web

#  实现一个web.RequestHandler子类，重载其中的get()函数，该函数负责相应定位到该RequestHandler的HTTP GET请求的处理。
class MainHandler(tonardo.web.RequestHandler):
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
def make_app():
  return tornardo.web.Application([
    (r"/", MainHandler),
  ])

def main():
  app = make_app()
  # 用web.Application.listen()函数指定服务器监听的端口
  app.listen(8888)
  # 用tornado.ioloop.IOLoop.current().start()启动IOLoop，该函数将一直运行且不退出，用户处理完所有客户端的访问请求。
  tornardo.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()