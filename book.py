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
    X+="<a href=searchb>根據書名關鍵字查詢圖書</a><br>"
    return X

@app.route("/books")
def books():
    info = ""
    url = "https://www.xbanxia.com/list/10_1.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box")

    for x in result:
        info += "<a href=" + x.find("a").get("href") + ">" + x.find("h4").text + "</a><br>"
        info += x.find("a").get("href") + "<br>"
        info +="<img src=https://www.xbanxia.com/" + x.find("img").get("src") + " width=200 height=300></img><br><br>"
    return info

@app.route("/searchQ", methods=["POST","GET"])
def searchQ():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("小說")
        docs = collection_ref.order_by("showDate").get()
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]: 
                info += "書名：" + doc.to_dict()["title"] + "<br>" 
                info += "作者：" + doc.to_dict()["author"] + "<br>"
                info += "類型：" + doc.to_dict()["showLength"] + "<br>" 
                info += "最近更新：" + doc.to_dict()["showDate"] + "<br>"
                info += "<img src=" + bk["cover"] + "></img><br><br>"           
        return info
    else:  
        return render_template("sraech.html")


if __name__ == "__main__":
    app.run(debug=True)
