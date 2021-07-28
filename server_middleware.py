import tornado.ioloop
import tornado.web
import json
import pyodbc
import tornado.options
import signal
import logging

from pprint import pprint
from eduman_database import check_student
from common import get_config

mysql = get_config('db_config.json').get('mysql')
server = mysql.get('server')
database = mysql.get('database')
username = mysql.get('username')
password = mysql.get('password')
       
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'
            %(server, database, username, password))
cur = conn.cursor()

class MainHandler(tornado.web.RequestHandler):

    def initialize(self, config):
        # self.db = db
        self.config = config
    
    def get(self):
    #     try:
    #         code = self.request.header.get("Authorization","")
    #         if code == "123456":
    #             conn = self.open_connection()
    #             cur = conn.cursor()
    #             query = """SELECT username,hoten,email,sdt
    #                         FROM t_user 
    #                         WHERE username = ? and hoten = ? and email = ? and sdt = ?"""
    #             cur.execute("SELECT MaSV,Dienthoai,Email,Ngaysinh1 FROM SinhVien WHERE MaSV={code}")

    #             #check data
    #             desc = cur.description
    #             column_names = [col[0] for col in desc]
    #             student_data = [dict(zip(column_names, row))  
    #                     for row in cur.fetchall()]
    #             data = {student_data}

    #             self.write(data)
                
    #     except Exception as ex:
    #         print(ex)
    #     finally:
    #         cur.close()
    #         conn.close()
        self.write("Hello World")
    def post(self):
        try:
            code = self.request.headers.get("Authorization", "")
            if code == "123456":
                res = self.request.body
                print(res)
                request_body = json.loads(res)
                username = request_body['username']
                #open cursor connect
                conn = self.config['connection']
                cur = self.config['cursor']

                check_students = check_student(cur, username)
                print(check_students)
                # data = {
                #     'MaSV:' : student_data[0]['MaSV'],
                #     'Hoten' : student_data[0]['Ten'],
                #     'Tenlop': student_data[0]['Tenlop'],
                #     'Tennganh': student_data[0]['Tennganh'],
                #     'MonHoc': []
                # }
                # print(student_data)
                
                # for index in student_data:
                #     data['MonHoc'].append({
                #         'IDMonhoc': index['MaMH'],
                #         'Tenmon': index['Tenmon'],
                #         'Hocky':index['Hocky']
                #     })
                    
                self.write(check_students)
            else:
                self.set_header("Content-Type", 'application/json')
                reply = {
                    "status": "error",
                    "reason": "Unauthorizated"
                }
                self.write(reply)
        except Exception as ex: 
            print("something went wrong")
            print(ex)
        # finally:
        #     cur.close()
        #     conn.close()


# def make_app():
#     return tornado.web.Application([
#         (r"/", MainHandler),
#     ])

class TeacherHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class MyApplication(tornado.web.Application):
    is_closing = False

    def initialize(self, config):
            # self.db = db
            self.config = config

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
            
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')
            conn = self.config['connection']
            cur = self.config['cursor']
            cur.close()
            conn.close()


def make_app(config: dict):
    return MyApplication([
        (r"/sv", MainHandler, dict(config=config)),
        (r"/gv", TeacherHandler),
        (r"/qli", AdminHandler),
    ])

def main():
    mysql = get_config('db_config.json').get('mysql')
    server = mysql.get('server')
    database = mysql.get('database')
    username = mysql.get('username')
    password = mysql.get('password')
        
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'
                %(server, database, username, password))
    cur = conn.cursor()

    connect_cursor = {
        'connection' : conn,
        'cursor' : cur
    }

    port = 9998
    application = make_app(connect_cursor)

    print(f'App listening port={port}')
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, application.signal_handler)
    application.listen(port)
    tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
