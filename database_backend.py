import random
import hashlib
import string
import uuid
from datetime import datetime

def create_password_random():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbol = string.punctuation

    #combine data
    all = lower + upper + num + symbol

    #use random
    temp = random.sample(all, 10)

    #create password
    password = "".join(temp)
    print("password:")
    print(password)
    
    return password

def hash_password(password: str) -> str:
    hash_method = hashlib.sha256()
    hash_method.update(password.encode('utf-8'))
    return hash_method.hexdigest()

def check_existed_student(cur, conn, user):
    try:
        # check
        query = """SELECT username
                    FROM users
                    WHERE username = %s """
        cur.execute(query,(user,))
        conn.commit()
                
        desc = cur.description
        column_names = [col[0] for col in desc]
        student_data = [dict(zip(column_names, row))  
                for row in cur.fetchall()]
        print(student_data)
        if student_data:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)

def generate_token(cur,conn,token, username):
    try:
        query = """
                INSERT INTO token(uuid, username, expired)
                VALUES (%s,%s,%s)
                """
        expire = datetime.now() + datetime.timedelta(days=10)
        expired_time = expire.strftime("%d/%m/%Y %H:%M:%S")
        cur.execute(query,(token,username,expired_time))
        conn.commit()
    except Exception as ex:
        print('Something went wrong in generate_token')
        print(ex)

def login(cur, conn, username, password):
    try:
        query = """SELECT username
                        FROM users
                        WHERE username = %s and pass = %s"""
        cur.execute(query,(username, hash_password(password)))
        conn.commit()
                
        desc = cur.description
        column_names = [col[0] for col in desc]
        student_data = [dict(zip(column_names, row))  
                for row in cur.fetchall()]
        print(student_data)
        if student_data:
            token = str(uuid.uuid4())
            print(token)
            generate_token(cur,conn,token,username)
            
            return token
        else:
            return False
       
    except Exception as ex:
        print("Something went wrong in login")
        print(ex)

def insert_new_student(cur, conn, user, holot, ten, email, sdt, nganhhoc):
    try:
        create_password = create_password_random()
        query_insert_student = """INSERT INTO users (username, holot, ten, email, sdt, pass, nganhhoc)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(query_insert_student,
                    (user,holot,ten,email,sdt,hash_password(create_password),nganhhoc))
        conn.commit()
        print('insert complete!')
        return True
    except Exception as ex:
        print(ex)
        return ex
