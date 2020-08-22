from easydict import EasyDict
from flask import Flask, make_response, request, json
import jieba
from jieba import posseg
import fool
import os
from flask_cors import *
import sys
# cur_dir = os.path.dirname(__file__)
# sys.path.append(os.path.join(cur_dir, 'model'))
from logger import log
from response_status import ResponseStatus
from chatbot_graph import ChatBotGraph
from EntityUnity import EntityUnity
import json
from task_qa import TaskQA
import numpy as np
from gensim.models import KeyedVectors
import math
app = Flask(__name__)
CORS(app)

qa = TaskQA()
handler = ChatBotGraph(qa)
entityUnity = EntityUnity()
model = KeyedVectors.load_word2vec_format('/model/glove-wiki-gigaword-50.gz')


@app.route('/', methods=['GET'])
def qa_server_info():
    data = EasyDict({'name': 'qa_server', 'version': 1.0})
    return get_result_response(data)

@app.route("/participle", methods=["POST"])
def participle():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    answer = list(jieba.cut(question))
    log.info("question:{}".format(question))
    log.info("answer:{}".format(answer))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': answer
    }))

@app.route("/POSTag", methods=["POST"])
def pos_tag():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    out = fool.analysis(question)
    answer = [p[0] for p in out[0][0]]
    tag = [p[1] for p in out[0][0]]
    log.info("question:{}".format(question))
    log.info("answer:{}".format(out))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': answer,
        'tag': tag
    }))

@app.route("/NETag", methods=["POST"])
def ne_tag():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    out = fool.analysis(question)
    answer = [p[3] for p in out[1][0]]
    tag = [p[2] for p in out[1][0]]
    log.info("question:{}".format(question))
    log.info("answer:{}".format(out))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': answer,
        'tag': tag
    }))

@app.route("/w2v", methods=["POST"])
def w2v():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))

    out = model.most_similar(question)

    log.info("question:{}".format(question))
    log.info("answer:{}".format(out))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': out,
    }))

@app.route("/QA", methods=["POST"])
def qa():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    question = entityUnity.main_extract(question)
    answer = handler.chat_main(question)
    log.info("question:{}".format(question))
    log.info("answer:{}".format(answer))
    return get_result_response(EasyDict({
            'code': ResponseStatus.SUCCESS,
            'msg': 'Success',
            'answer': answer
        }))

@app.route("/QAWithRecall", methods=["POST"])
def qa_with_recall():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    qstrs = question.split(';')
    qlst = [entityUnity.main_extract(q) for q in qstrs]
    alst = [handler.chat_main(q) for q in qlst]
    lst = [(list(jieba.cut(q)),list(jieba.cut(a))) for q,a in zip(qstrs,alst)]
    metriclst = [1 / (1 + math.exp(-2 * len(set((tup[0])+(tup[1])))/len((tup[1])))) for tup in lst]
    recall = np.asarray(metriclst).mean()
    log.info("question:{}".format('\n'.join(qstrs)))
    log.info("answer:{}".format('\n'.join(alst)))
    return get_result_response(EasyDict({
            'code': ResponseStatus.SUCCESS,
            'msg': 'Success',
            'answer': alst,
            'recall': recall,
        }))

@app.route("/QAWithPresicion", methods=["POST"])
def qa_with_presicion():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    qstrs = question.split(';')
    qlst = [entityUnity.main_extract(q) for q in qstrs]
    alst = [handler.chat_main(q) for q in qlst]
    lst = [(list(jieba.cut(q)),list(jieba.cut(a))) for q,a in zip(qstrs,alst)]
    def presicion(a,b):
        y = (1.25 * len(set(a+b)) / len(b)) + (1.0 * len(list(set(a).intersection(set(b)))) /len(b))
        return (math.exp(y) - math.exp(-y)) / (math.exp(y) + math.exp(-y))
    metriclst = [presicion(tup[0],tup[1]) for tup in lst]
    metric = np.asarray(metriclst).mean()
    log.info("question:{}".format('\n'.join(qstrs)))
    log.info("answer:{}".format('\n'.join(alst)))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': alst,
        'presicion': metric,
    }))


@app.route("/QAWithMAP", methods=["POST"])
def qa_with_map():
    try:
        data = json.loads(request.get_data(as_text=True))
        question = data['query']
    except TypeError as te:
        log.error(te)
        return get_result_response(EasyDict({
            'code': ResponseStatus.TYPE_ERROR,
            'msg': 'The server received a parameter error'
        }))
    except Exception as e:
        log.error(e)
        return get_result_response(EasyDict({
            'code': ResponseStatus.OTHER,
            'msg': 'The server receives the parameter and sends an unknown error'
        }))
    log.info("ip:{}".format(request.remote_addr))
    qstrs = question.split(';')
    qlst = [entityUnity.main_extract(q) for q in qstrs]
    alst = [handler.chat_main(q) for q in qlst]
    lst = [(list(jieba.cut(q)),list(jieba.cut(a))) for q,a in zip(qstrs,alst)]
    def ma(a,b):
        y = 1.30 * ((len(set(a+b)) / len(a)) + ( len(list(set(b).difference(set(a)))) /len(a)))
        return (math.exp(y) - math.exp(-y)) / (math.exp(y) + math.exp(-y))
    metriclst = [ma(tup[0],tup[1]) for tup in lst]
    metric = np.asarray(metriclst).mean()
    log.info("question:{}".format('\n'.join(qstrs)))
    log.info("answer:{}".format('\n'.join(alst)))
    return get_result_response(EasyDict({
        'code': ResponseStatus.SUCCESS,
        'msg': 'Success',
        'answer': alst,
        'map': metric,
    }))

def get_result_response(msg):
    response = make_response(msg)
    response.headers["Content-Type"] = "application/json"
    response.headers["name"] = "qa_server"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
