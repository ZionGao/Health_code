
from flask import Flask, render_template, request
from flask_cors import *
from chatbot_graph import ChatBotGraph
from EntityUnity import EntityUnity
import json
from task_qa import TaskQA

app = Flask(__name__)

CORS(app)

qa = TaskQA()
handler = ChatBotGraph(qa)
entityUnity = EntityUnity()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    question = request.args.get('msg')
    #实体统一
    question = entityUnity.main_extract(question)
    print('question:', question)
    answer = handler.chat_main(question)
    print('小助手:', answer)
    return answer

@app.route("/search", methods=["POST"])
def search():
    data = request.get_data()
    data = json.loads(data)
    question = data['ques']
    # 实体统一
    question = entityUnity.main_extract(question)
    print('question:', question)
    answer = handler.chat_main(question)
    print('小助手:', answer)
    return answer


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, use_reloader=False)






