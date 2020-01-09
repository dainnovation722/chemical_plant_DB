from flask import Flask, render_template, request
from models.models import FeatureContent, User
from models.database import db_session
from datetime import datetime
#ログイン処理の実装に必要なモジュール
from flask import session, redirect, url_for
from app import key
from hashlib import sha256

app = Flask(__name__)
app.secret_key = key.SECRET_KEY
@app.route("/")
def hello_world():
    return "Hello World!"

'''
/indexにアクセスしたユーザに対してsession情報がある場合index.htmlを表示、
session情報がない場合はログインページ(/top?status=logout)にリダイレクト
'''
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_feature = FeatureContent.query.all()
        return render_template("index.html", name=name, all_feature=all_feature)
    else:
        return redirect(url_for("top", status="logout"))

@app.route("/add", methods=["post"])
def add():
    feature = request.form["feature"]
    details = request.form["details"]
    content = FeatureContent(feature, details, datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/update", methods=["post"])
def update():
    content = FeatureContent.query.filter_by(id=request.form["update"]).first()
    content.feature = request.form["feature"]
    content.details = request.form["details"]
    db_session.commit()
    return redirect(url_for("index"))

'''
request.form.getlist("delete")でidのリストで受け取ってから、
そのリストに対してfor文を回して１件ずつ削除
'''
@app.route("/delete", methods=["post"]) 
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = FeatureContent.query.filter_by(id=id).first() 
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/login", methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top", status="wrong_password"))
    else:
        return redirect(url_for("top", status="user_notfound"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top", status="logout"))

@app.route("/register", methods=["post"])
def register():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        #passwordをDBにベタ書き保存するとセキュリティ上よろしくないためハッシュ化
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)

@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)

if __name__=="__main__":
    app.run(debug=True)