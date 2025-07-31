'''
Author: flwfdd
Date: 2021-07-29 12:15:47
LastEditTime: 2021-07-29 18:24:40
Description: 
_(:з」∠)_
'''
from flask_cors import CORS
from flask import Flask,request,abort
import json
import time
import threading

app = Flask(__name__)
CORS(app,resources=r"/*")

def read_json(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.loads(f.read())

def save_json(path,dic):
    with open(path,"w",encoding="utf-8") as f:
        f.write(json.dumps(dic,ensure_ascii=False))

def user_input(dic):
    path="./data/"+dic['class_name']+".json"
    data=read_json(path)
    for (ind,i) in enumerate(data['list']):
        if i[0]==dic['name']:
            data['list'].pop(ind)
            break
    data['list'].append([dic['name'],dic['city'],dic['university']])
    if dic['city'] not in data['location']:
        data['location'][dic['city']]=location[dic['city']]
    if dic['university_type']==True: #大陆大学
        if dic['university'] not in data['location']:
            data['location'][dic['university']]=location[dic['university']]
    else: #其他大学
        data['location'][dic['university']]=dic['location']
    save_json(path,data)
    return {"status":"ok"}

def admin_delete(dic):
    if dic['password']!='sukisu233' and dic['password']!=read_json("./data/password.json")[dic['class_name']]:
        return {"status":"error"}
    path="./data/"+dic['class_name']+".json"
    data=read_json(path)
    l=[]
    for i in data['list']:
        if i[0] not in dic['delete_list']:
            l.append(i)
    data['list']=l
    save_json(path,data)
    return {"status":"ok"}

def merge():
    dic=read_json("./data/class_list.json")
    for i in dic:
        out=read_json("./data/template.json")
        out['class_name']=i
        for j in dic[i]:
            mdic=read_json("./data/"+j+".json")
            pre_name=j.replace(i,"")+" "
            for k in mdic['list']: k[0]=pre_name+k[0]
            out['list']+=mdic['list']
            out['location'].update(mdic['location'])
        save_json("./data/"+i+".json",out)

def merge_thread():
    while True:
        merge()
        time.sleep(60)

@app.route("/")
def say_hello():
    return file_route("index.html")
    #return "hello SF-ND!"

#api
@app.route('/api',methods=['GET','POST'])
def api():
    ips=read_json("./ban.json")
    if request.remote_addr in ips: return {"status":"err"}
    args=request.values
    with open("./log.txt","a",encoding="utf-8") as f: f.write(request.remote_addr+" "+args['type']+" "+args["data"]+"\n")
    if args['type']=='user_input': return user_input(json.loads(args['data']))
    if args['type']=='admin_delete': return admin_delete(json.loads(args['data']))

#show.html
@app.route("/show.html")
def show_html():
    args=request.values
    with open("./html/show.html","r",encoding="utf-8") as f:
        s=f.read()
    with open("./data/"+args['class_name']+".json","r",encoding="utf-8") as f:
        s=s.replace("{/*data*/ }",f.read())
    return s

#admin.html
@app.route("/admin.html")
def admin_html():
    args=request.values
    with open("./html/admin.html","r",encoding="utf-8") as f:
        s=f.read()
    with open("./data/"+args['class_name']+".json","r",encoding="utf-8") as f:
        s=s.replace("{/*data*/ }",f.read())
    return s

#文件服务器
@app.route("/<path>")
def file_route(path):
    try:
        with open("./html/"+path,"r",encoding="utf-8") as f:
            return f.read()
    except:
        abort(404)

#初始化
location=read_json("./data/location.json")

threading.Thread(target=merge_thread).start()

app.run(host="0.0.0.0",port=5707)
