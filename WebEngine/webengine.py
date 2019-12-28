from tornado import ioloop, web
import os

class WebServer:
    """Creates the webserver used as the control interface for dummyRDM
    """

    class MainHandler(web.RequestHandler):
        def get(self):
            self.render("templates/index.html")

    def make_app(self):
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        return web.Application([
            (r"/", WebServer.MainHandler),
        ], **settings)
    
    def run(self):
        app = WebServer.make_app(self)
        app.listen(8080)
        print("Webserver running on port 8080")
        ioloop.IOLoop.current().start()