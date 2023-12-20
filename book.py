import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    X+="<a href=books>全部圖書</a><br>"
    X+="<a href=search>根據書名關鍵字查詢圖書</a><br>"
    X+="<br><a href=spider>網路爬蟲擷取子青老師課程資訊</a><br><br>"
    X+="<a href=/searchQ>查詢開眼電影即將上映影片</a><br>"
    return X


@app.route("/books")
def books():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")
    docs = collection_ref.order_by("anniversary").get()     
    for doc in docs:
        bk = doc.to_dict()         
        Result += "書名： <a href=" +bk["url"] + ">" + bk["title"] + "</a><br>"
        Result += "作者：" + bk["author"] + "<br>"
        Result += str(bk["anniversary"]) + "週年紀念版" + "<br>"
        Result += "<img src=" + bk["cover"] + "></img><br><br>"    
    return Result

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keywork = request.form["keywork"]
        Result = "您輸入的關鍵字是：" + keywork
        
        db = firestore.client()
        collection_ref = db.collection("圖書精選")
        docs = collection_ref.order_by("anniversary").get()     
        for doc in docs:
            bk = doc.to_dict()
            if keywork in bk["title"]:         
                Result += "書名： <a href=" +bk["url"] + ">" + bk["title"] + "</a><br>"
                Result += "作者：" + bk["author"] + "<br>"
                Result += str(bk["anniversary"]) + "週年紀念版" + "<br>"
                Result += "<img src=" + bk["cover"] + "></img><br><br>"    
        return Result
    else:
        return render_template("searchbk.html")


@app.route("/searchQ", methods=["POST","GET"])
def searchQ():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("電影")
        docs = collection_ref.order_by("showDate").get()
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]: 
                info += "片名：" + doc.to_dict()["title"] + "<br>" 
                info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
                info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>" 
                info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"           
        return info
    else:  
        return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)