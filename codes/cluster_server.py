
from flask import Flask, render_template, request
from flask_cors import *
import json
from cluster import Text_Cluster

app = Flask(__name__)

CORS(app)

cluster = Text_Cluster()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_data()
    data = json.loads(data)
    #获取json的value为未回答数组
    questions = data['ques']
    result = cluster.run(questions)
    return result

def test(url, ques):
    import json
    data = json.dumps(dict(ques=ques))
    import requests
    response = requests.post(url, data=data)
    return response.content.decode()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, use_reloader=False)






