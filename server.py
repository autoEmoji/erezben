__package__ = "typeIt"

import tornado.ioloop
import tornado.web
import json
import os
import predictor
from platform import system

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("main.html")
        self.render("main.html")

class sheetsHandler(tornado.web.RequestHandler):
    def get(self):
        print("sheets handler")
        self.redirect("https://docs.google.com/presentation/d/1FsLbbtWLhHNGdk60ctadGCanPxKEDlF2wC4mKFuo3Ck/present?slide=id.p")

class searchHandler(tornado.web.RequestHandler):
    def post(self):
        print("search handler")
        body = bytes.decode(self.request.body)
        body = json.loads(body)
        msg = body["msg"]
        timestamp = body["time"]
        uid = body["id"]
        if msg != "":
            try:
                test_result = predictor.test_result(msg, timestamp, uid)
                print(test_result)
                result = {"result":[test_result]}
                result = json.dumps(result)
            except KeyError:
                self.set_status(404)
                result = "no such user id"
        else:
            self.set_status(404)
            result = json.dumps("empy message")
        self.finish(result)
        print('sent result')

class resultHandler(tornado.web.RequestHandler):
    def post(self):
        print("result handler")
        msg = self.get_argument("msg")
        label = self.get_argument("label")

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


def make_app():
    print("make_app")
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", searchHandler),
        (r"/result", resultHandler),
        (r"/sheets", sheetsHandler),
    ], **settings)


if __name__ == "__main__":
    if system() in ["Windows", "Darwin"]:
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
