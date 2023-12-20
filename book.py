import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime

import requests
from bs4 import BeautifulSoup


@app.route("/")
def index():
    X+="<a href=books>全部圖書</a><br>"
    X+="<a href=search>根據書名關鍵字查詢圖書</a><br>"
    return X

@app.route("/books")
def spider():
    info = ""
    url = "https://www.xbanxia.com/list/10_1.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box")

    for x in result:
        info += "<a href=" + x.find("a").get("href") + ">" + x.find("h4").text + "</a><br>"
        info += x.find("p").text + "<br>"
        info += x.find("a").get("href") + "<br>"
        info +="<img src=https://www.xbanxia.com/" + x.find("img").get("src") + " width=200 height=300></img><br><br>"
    return info

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
        return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
