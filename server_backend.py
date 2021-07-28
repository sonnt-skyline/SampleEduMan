from requests.models import Response
from tornado.httputil import ResponseStartLine
import tornado.ioloop
import tornado.web
import requests
import json
import signal
import tornado.options
import logging
import psycopg2
# from tornado_cors import CorsMixin

from database_backend import check_existed_student, insert_new_student,login
from common import get_config





class MainHandler(tornado.web.RequestHandler):
     # Value for the Access-Control-Allow-Origin header.
    # Default: None (no header).
    CORS_ORIGIN = '*'
    
    # Value for the Access-Control-Allow-Headers header.
    # Default: None (no header).
    CORS_HEADERS = 'Content-Type'
    
    # Value for the Access-Control-Allow-Methods header.
    # Default: Methods defined in handler class.
    # None means no header.
    CORS_METHODS = 'POST'

    # Value for the Access-Control-Allow-Credentials header.
    # Default: None (no header).
    # None means no header.
    CORS_CREDENTIALS = True
    
    # Value for the Access-Control-Max-Age header.
    # Default: 86400.
    # None means no header.
    CORS_MAX_AGE = 21600

    # Value for the Access-Control-Expose-Headers header.
    # Default: None
    CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages'
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def initialize(self, config):
        # self.db = db
        self.config = config

    def get(self):
        # try:
        #     res = self.request.body
        #     request_body = json.loads(res)
        #     check_username = request_body['username']
        #     check_hoten = request_body['hoten']
        #     check_email = request_body['email']
        #     check_sdt = request_body['sdt']
        #     query = """SELECT username,hoten,email,sdt 
        #                 FROM t_user 
        #                 WHERE username = ? and hoten = ? and email = ? and sdt = ?"""
        #     cur.execute(query,(check_username,check_hoten,check_email,check_sdt,))
                       
        #     desc = cur.description
        #     column_names = [col[0] for col in desc]
        #     student_data = [dict(zip(column_names, row))  
        #             for row in cur.fetchall()]
        #     if not student_data:
        #         response=requests.get("http://localhost:9998",
        #                         headers={"Authorization":"123456"},
        #                         data=json.dumps(request_body))
        #         json_response = response.json()
            
        # except Exception as ex:
        #     print(ex)
        # finally:
        #     cur.close()
        #     conn.close()
        self.write("Hello, world")



    def post(self):
        try:
            res = self.request.body
            request_body = json.loads(res)
            print(request_body)
            
            username = request_body['username'] #mssv
            email = request_body['email']
            sdt = request_body['phone']

            conn = self.config['connection']
            cur = self.config['cursor']
            student_exist = check_existed_student(cur, conn, username)
            if student_exist:
                reply = {
                    "status": "existed"
                }
                self.write(reply)
            else:
                response = requests.post("http://localhost:9998/sv",
                                headers = {"Authorization":"123456"},
                                data = json.dumps(request_body))
                
                json_response = response.json()
                print(json_response)
                nganh_hoc = json_response['nganh']
                ho_lot = json_response['holot']
                ten = json_response['ten']
                insert_success = insert_new_student(cur, conn, username, ho_lot, ten, email, sdt, nganh_hoc)
                reply = {"status": "completed"} if insert_success else {"status" : "Not Completed"}

                self.write(reply)
        except Exception as ex:
            print("Something went wrong in register MainHandler!!")
            print(ex)

class LoginStudentHandler(tornado.web.RequestHandler):

    CORS_ORIGIN = '*'
    
    # Value for the Access-Control-Allow-Headers header.
    # Default: None (no header).
    CORS_HEADERS = 'Content-Type'
    
    # Value for the Access-Control-Allow-Methods header.
    # Default: Methods defined in handler class.
    # None means no header.
    CORS_METHODS = 'POST'

    # Value for the Access-Control-Allow-Credentials header.
    # Default: None (no header).
    # None means no header.
    CORS_CREDENTIALS = True
    
    # Value for the Access-Control-Max-Age header.
    # Default: 86400.
    # None means no header.
    CORS_MAX_AGE = 21600

    # Value for the Access-Control-Expose-Headers header.
    # Default: None
    CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages'
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def initialize(self, config):
        # self.db = db
        self.config = config

    def get(self):
        self.write('Hello World')
    def post(self):
        try:
            res = self.request.body
            request_body = json.loads(res)
            print(type(res))
            print(request_body)

            username = request_body['username']
            password = request_body['password']
            conn = self.config['connection']
            cur = self.config['cursor']

            login_status = login(cur,conn,username,password)
            print(login_status)
            reply = { "status" : "Login Success", "access_token" : login_status } if login_status else {"status": "Login Failed"}
            self.set_header("Authorization", login_status)
            self.write(reply)
            
                    
        except Exception as ex:
            print('Something went wrong in LoginStudentHandler') 
            print(ex)
        

class TeacherHandler(tornado.web.RequestHandler):
    def get():
        pass
    def post():
        pass

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class MyApplication(tornado.web.Application):
    is_closing = False

    def initialize(self, config):
            self.config = config

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
                        
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')        


def make_app(config: dict):
    return MyApplication([
        (r"/sv/login",LoginStudentHandler, dict(config=config)),
        (r"/sv", MainHandler, dict(config=config)),
        (r"/gv", TeacherHandler),
        (r"/qli",AdminHandler),
    ],
    dict(config=config))


def main():
    postgres = get_config('db_config.json').get('postgres')

    host = postgres.get('host')
    database = postgres.get('database')
    username = postgres.get('username')
    password = postgres.get('password')
    port = postgres.get('port')

    conn = psycopg2.connect(
        host = host,
        database = database,
        user = username,
        password = password,
        port = port
    )
    cur = conn.cursor()
    connect_db = {
        'connection' : conn,
        'cursor' : cur
    }
    port=8889
    application = make_app(connect_db)

    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, application.signal_handler)
    application.listen(port)
    print(f'App listening port={port}')   
    tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()