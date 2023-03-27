from flask import Flask, jsonify, request
from urllib.request import urlopen
import json
import datetime
import logging
import sys


app = Flask(__name__)

url = "https://dev.ylytic.com/ylytic/test"

response = urlopen(url)

data_json = json.loads(response.read())


def sdb(df, dd, dt):
    at_from = datetime.datetime.strptime(df, '%d-%m-%Y')
    at_to = datetime.datetime.strptime(dt, '%d-%m-%Y')
    data_d = datetime.datetime.strptime(dd, '%d %b %Y')
    return at_from.date() <= data_d.date() <= at_to.date()


@app.route('/search')
def getCmtWithAuth():
    resp = {}
    data = []
    search_author = request.args.get('search_author')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')

    for i in range(0, len(data_json["comments"])):
        flag = sdb(at_from, data_json["comments"][i]["at"][5:16], at_to)
        if((search_author in data_json["comments"][i]["author"]) and (data_json["comments"][i]["like"] >= int(like_from)
                                                                      and data_json["comments"][i]["like"] <= int(like_to))
           and (data_json["comments"][i]["reply"] >= int(reply_from)
                and data_json["comments"][i]["reply"] <= int(reply_to))
           and search_text in (data_json["comments"][i]["text"])
           and flag):
            data.append(data_json["comments"][i])
    if(len(data) == 0):
        resp["status"] = "failed"
        resp["data"] = data
    else:
        resp["staus"] = "success"
        resp["data"] = data

    return resp


@app.route('/searchtwo')
def getAutho():
    respo = []
    search_author = request.args.get('search_author')
    print(len(data_json["comments"]))
    for i in range(0, len(data_json["comments"])):
        if(search_author.lower() in data_json["comments"][i]["author"].lower()):
            respo.append(data_json["comments"][i])
    resp1 = {}
    resp1[search_author] = respo

    return resp1


if __name__ == "__main__":
    app.run(debug=True)
