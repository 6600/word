import json
import pymysql
import requests
import datetime
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

appListObj = {
  "wx82979d12f4b4f98e": "7428b006ae60de7a1bbdf3bc1060fcad"
}

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

@app.route("/getUserInfo")
def getUserInfo():
  global appListObj
  appid = request.args.get("appid")
  # print(request.args.get("code"))
  response = requests.request("GET", "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + appid + "&secret=" + appListObj[appid] +"&code=" + request.args.get("code") + "&grant_type=authorization_code", headers={}, data={})
  data = response.json()
  if ('access_token' not in data):
    return response.json()
  response2 = requests.request("GET", "https://api.weixin.qq.com/sns/userinfo?access_token=" + data['access_token'] + "&openid=" + data['openid'] + "&lang=zh_CN", headers={}, data={})
  userInfo = response2.json()
  connection = pymysql.connect(host=config["server"], port=config["port"], user=config["user"], password=config["password"], db=config["name"], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
  with connection.cursor() as cursor:
      # 执行sql语句，进行查询
      sql = "select * from `user` where openid='" + userInfo['openid'] + "'"
      # print(sql)
      cursor.execute(sql)
      # 获取查询结果
      result = cursor.fetchone()
      connection.commit()
      if (not result):
        sql = "INSERT INTO `user` ( openid, jointime, value) VALUES ( '%s', '%s', '%s')" % (userInfo['openid'], str(datetime.datetime.now()), '')
        # print(sql)
        cursor.execute(sql)
        connection.commit()
      connection.close()
  print(userInfo)
  return userInfo


app.run(host='0.0.0.0', port=8100, debug=True)