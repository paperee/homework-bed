# -*- coding: UTF-8 -*-

from flask import Flask,Response,request,redirect,render_template,session,send_file
from os import path,makedirs,walk,getcwd,remove
from time import strftime,localtime
from codecs import open
from json import dumps,loads
from random import choice,sample

def pull(arg,error=None):
    return request.args.get(arg,error)

def save(path_,mode,text):
    open(path_,mode,"UTF-8-sig").write(text)

def load(path_):
    return open(path_,"r","UTF-8-sig").read()

def test(list_):
    return "".join(list_).translate(table).isalnum()

def result(code,type_,text,arg={"head":"作者：PAPEREE(ee) 来自：DHQZ"}):
    return Response(dumps({"code":code,"type":type_,"text":text,**arg},ensure_ascii=False),mimetype="application/json")

table=str.maketrans("", "", ".-+=_/|~")
method=["POST","GET"]
config=loads(load("config.json").replace("'", '"'))

app=Flask(str(id("DHQZ")),static_folder="templates",static_url_path="/templates")
app.secret_key="".join(sample("NeverGonnaGiveYouUp",12))

@app.errorhandler(Exception)
def error(e):
    return redirect(f"https://1145.s3.ladydaily.com/{choice(['rock','cxk'])}.mp4")

@app.route("/")
def index():
    if request.args:
        return redirect(request.base_url)

    if "user" not in session:
        return render_template("login.html")

    user=session["user"]
    data=list()

    for root,dirs,files in walk(f"{getcwd()}/homework/{'/'.join(user)}"):
        for file in files:
            data.append(path.join(root,file).replace("\\","/").split("/")[-1].split("_",1)[-1])

    return render_template("index.html",user="".join(user),data=" ".join(data))

@app.route("/login",methods=method)
def login():
    form=list(request.form.values())

    if not all(form):
        return result(0,"login","小分队信息不完善")

    if not test(form):
        return result(0,"login","无效的小分队名称/密码")

    form[-2]+="小分队"
    user_="".join(form[:-1])
    pwd=config.get(user_)

    if pwd:
        if form[-1]!=pwd:
            return result(0,"login","密码错误")

    else:
        config[user_]=form[-1]
        save("config.json","w",str(config))

    session["user"]=form[:-1]
    return result(1,"login","注册/登陆成功",{"user":user_})

@app.route("/leave",methods=method)
def leave():
    session.pop("user")
    return redirect("/")

@app.route("/upload",methods=method)
def upload():
    if "user" not in session:
        return result(0,"upload","无效的登陆状态")

    files=request.files.getlist("files[]",None)
    files_=list()

    if not files:
        return result(0,"upload","你传了个寂寞")

    if int(request.content_length)>1*1024*1024:
        return result(0,"upload","无效的文件大小")

    if not test([i.filename for i in files]):
        return result(0,"upload","无效的文件名称")

    ip=request.headers.get("X-Forwarded-For",request.remote_addr)
    user=session["user"]
    time=strftime("%Y.%m.%d %H:%M:%S",localtime())

    path_=f"homework/{'/'.join(user)}"
    makedirs(path_,exist_ok=True)

    for file in files:
        file.save(f"{path_}/{''.join(user)}_{file.filename}")
        files_.append(file.filename)

    return result(1,"upload","文件上传成功",{"files":files_,"time":time})

@app.route("/delete",methods=method)
def delete():
    if "user" not in session:
        return result(0,"delete","无效的登陆状态")

    filename=pull("filename")

    if not filename:
        return result(0,"delete","请输入文件名称")

    user=session["user"]
    path_=f"homework/{'/'.join(user)}/{''.join(user)}_{filename}"
    time=strftime("%Y.%m.%d %H:%M:%S",localtime())

    if not path.isfile(path_):
        return result(0,"delete","无效的文件路径")

    remove(path_)
    return result(1,"delete","文件删除成功",{"file":filename,"time":time})

@app.route("/download/<path:filename>",methods=method)
def download(filename):
    if "user" not in session:
        return result(0,"download","无效的登陆状态")

    user=session["user"]
    path_=f"homework/{'/'.join(user)}/{''.join(user)}_{filename}"

    if not path.isfile(path_):
        return result(0,"download","无效的文件路径")

    try:
        return send_file(path_,as_attachment=True,attachment_filename=filename)

    except:
        return send_file(path_,as_attachment=True,download_name=filename)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=1919,debug=True,threaded=True)
