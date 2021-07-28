import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, setting):
        # self.db = db
        self.setting = setting
    def get(self):
        conn = self.setting['connection']
        cur = self.setting['cursor']
        print(conn)
        
        
# class StoryHandler(tornado.web.RequestHandler):
#     def initialize(self, setting):
#         # self.db = db
#         self.setting = setting

#     def get(self, story_id):
#         self.write("this is story %s" % story_id)

def main():

    set_ = {
        'connection' : '123',
        'cursor' : '34234'
    }
    app = make_app(set_)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

def make_app(setting):
    return tornado.web.Application([
        (r"/", MainHandler, dict(setting = setting)),
        # (r"/story/([0-9]+)", StoryHandler, )
    ])

if __name__ == "__main__":
    main()