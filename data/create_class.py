'''
Author: flwfdd
Date: 2021-07-31 10:37:08
LastEditTime: 2021-07-31 10:40:02
Description: 
_(:з」∠)_
'''
import json
import os

def read_json(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.loads(f.read())

def save_json(path,dic):
    with open(path,"w",encoding="utf-8") as f:
        f.write(json.dumps(dic,ensure_ascii=False))

dic=read_json("./class_list.json")
for i in dic:
    for j in dic[i]:
        if os.path.exists("./"+j+".json")==False:
            os.system("copy {} {}".format("template.json",j+".json"))
        mdic=read_json("./"+j+".json")
        mdic['class_name']=j
        save_json("./"+j+".json",mdic)
