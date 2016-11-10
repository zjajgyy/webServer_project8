import sqlite3
import os
from flask import Flask, request, Response
import consul
import json


app = Flask(__name__)

DB_FILE_PATH = 'sqlite.db'
SHOW_SQL = True 
create_table_sql = "CREATE TABLE user(id integer primary key,username varchar(20) UNIQUE,password varchar(15) NOT NULL)"
query_sql = "select * from  user"
insert_sql = "INSERT INTO user values(?,?)"


def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        return conn


def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()


def create_table(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        try:
            cu.execute(sql)
            conn.commit()
            close_all(conn, cu)
            return True
        except:
            return False
    else:
        return False


def drop_table(conn, table_name):
    sql = 'DROP TABLE IF EXISTS ' + table_name
    if table_name is not None and table_name != '':
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        close_all(conn, cu)
        return True
    else:
        return False


def close_all(conn, cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if conn is not None:
            conn.close()


def insert_data(conn, sql, data):
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            cu.execute(sql,(data[0],data[1]))
            conn.commit()
            close_all(conn, cu)
            return True
    else:
        return False


def query_data(conn,sql):
    cu = get_cursor(conn)
    cu.execute(sql)
    r = cu.fetchall()
    list_for_return = []
    if len(r) > 0:
        for e in r:
            users = e
            list_for_return.append(users)
    close_all(conn, cu)
    return list_for_return





@app.route("/register_service", methods=['POST'])
def register():
    conn = get_conn(DB_FILE_PATH)
    email = request.form.get("username")
    password = request.form.get("password")
 
    if (insert_data(conn, insert_sql, [email, password])):
        return Response(json.dumps("YES"))
        #return "YES"
    else:
        #return "None"
        return Response(json.dumps("None"))

@app.route("/login_service", methods=['POST'])
def login():
    conn = get_conn(DB_FILE_PATH)
    email = request.form.get("username")
    password = request.form.get("password")
    print(email)
    data_password = query_data(conn, "SELECT password from user where username='" + email + "'")
    for i in data_password:
        if (password==i[0]):
            #return "OK"
            return Response(json.dumps("OK"))
    #return " Not"
    return Response(json.dumps("Not"))

@app.route("/judgeEmail_service", methods=['POST'])
def judgeEmail():
    conn = get_conn(DB_FILE_PATH)
    email = request.form.get("username")
    password = request.form.get("password")
    data_password = query_data(conn, "SELECT * from user where username='" + email + "'")
    if (data_password==[]):
        #return "None"
        return Response(json.dumps("None"))
    else:
        #return "YES"
        return Response(json.dumps("YES"))


def register(host_consul, port_consul):
    c = consul.Consul(host="192.168.1.1", port=8500)
    c.agent.service.register(name="consul_database", service_id="consul_database", address=host_consul, port=port_consul)

def deregister(service_id):
    c = consul.Consul()
    c.agent.service.deregister(service_id)

if __name__ == '__main__':
    register("192.168.1.1", 8083)
    app.run(host='0.0.0.0', port=8083)

