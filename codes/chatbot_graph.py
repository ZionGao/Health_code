#!/usr/bin/env python3
# coding: utf-8

from question_classifier import *
from question_parser import *
from answer_search import *
from prepare_data.similar import jaccard
from EntityUnity import *
import pandas as pd
import jieba
import json
from task_qa import TaskQA

'''问答类'''
class ChatBotGraph:
    def __init__(self, qa):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.qa = qa



    def chat_main(self, ques):
        answer = '您好，我是酒店问答小助手，希望可以帮到您！'
        if '订' in ques and '酒店' in ques: #是否有订   酒店
            self.qa.build()
        if self.qa.online:
            return self.qa.answer(ques)
        else:
            res_classify = self.classifier.classify(ques)
            print("ques class: ", res_classify)
            if not res_classify['args']:
                # return '抱歉，找不到该酒店哦😯'
                return self.postSizhi(ques)
            if not res_classify or not res_classify['question_types']:
                return '抱歉，小助手还在不断学习哦：：'
            res_sql = self.parser.parser_main(res_classify)
            final_answers = self.searcher.search_main(res_sql)
            if not final_answers:
                return answer
            else:
                return '\n'.join(final_answers)

    # 调取思知机器人
    def postSizhi(self, ques):
        url = "https://api.ownthink.com/bot"
        import requests
        import re
        data = {'spoken': ques, "appid": "xiaosi", "userid": "user"}
        response = requests.post(url, data=data)
        ans = response.content.decode('utf-8')
        json_str = re.sub('\'', '\"', ans)
        json_dict = json.loads(json_str)  # （注意：key值必须双引号）
        res = json_dict['data']['info']['text']
        return res.replace('小思','小助手')

    def load_hotel_name(self):
        df = pd.read_csv('./dict/base_dict.txt', sep=' ', names=['name', 'num', 'ner'])
        df = df[df['ner'].str.contains('h')]
        hotels = [list(jieba.cut(hotel)) for hotel in df.name.values]
        return hotels

    def match_hotel(self, hotels):
        seg_list = list(jieba.cut(question))
        match = []
        for hotel in hotels:
            if jaccard(seg_list, hotel) > 0.4:
                match.append(hotel)


if __name__ == '__main__':
    qa = TaskQA()
    handler = ChatBotGraph(qa)
    entityUnity = EntityUnity()

    while 1:
        question = input('请输入:')
        #实体统一
        question = entityUnity.main_extract(question)
        print('question:', question)
        answer = handler.chat_main(question)
        print('小助手:', answer)

