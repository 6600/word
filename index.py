import json
import pymysql
from urllib import parse
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin

config = {
  "server": "bj-cynosdbmysql-grp-kqvvbnw0.sql.tencentcdb.com",
  "port": 28556,
  "user": "root",
  "password": "CjMom&xcaq3iPixQ",
  "name": "word"
}

app = Flask(__name__, static_folder='file')
cors = CORS(app)

# 连接数据库
def connectDB():
  return pymysql.connect(host=config["server"], port=config["port"], user=config["user"], password=config["password"], db=config["name"], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

@app.route("/getData")
def getData():
    connection = connectDB()
    with connection.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = "select * from `word`"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        return json.dumps(result)


app.run(host='0.0.0.0', port=8100, debug=True)