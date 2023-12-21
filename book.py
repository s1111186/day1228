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
    X+="<a href=searchb>根據書名關鍵字查詢圖書</a><br>"
    return X

@app.route("/searchQ", methods=["POST","GET"])
def searchQ():
    if request.method == "POST":
        NovelTitle = request.form["NovelTitle"]
        info = ""
        db = firestore.client()     
        collection_ref = db.collection("小說")
        docs = collection_ref.order_by("showDate").get()
        for doc in docs:
            if NovelTitle in doc.to_dict()["title"]: 
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
