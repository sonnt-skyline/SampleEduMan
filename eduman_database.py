def check_student(cur,username):
    sql = """SELECT SinhVien.MaSV, SinhVien.Maso, SinhVien.Holot,SinhVien.Ten,Lop.Tenlop,NganhHoc.TenNganh,NganhHoc.MaNG
                        FROM SinhVien
                        INNER JOIN Lop On SinhVien.MaL = Lop.MaL
                        RIGHT JOIN NganhHoc On Lop.MaNG = NganhHoc.MaNG 
                        WHERE Maso = ? """
               
    cur.execute(sql,(username,))
    #load data
    desc = cur.description
    column_names = [col[0] for col in desc]
    student_data = [dict(zip(column_names, row))  
            for row in cur.fetchall()]
    print(student_data)
    if student_data:
        reply = {
            "flag" : True,
            "nganh" : student_data[0]['MaNG'],
            "holot" : student_data[0]['Holot'],
            "ten" : student_data[0]['Ten']
        }
        return reply
    else: 
        reply = {
            "flag" : False
        }
        return reply