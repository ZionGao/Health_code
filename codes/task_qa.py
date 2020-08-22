import random
import json
import requests
import re


class TaskQA(object):
    def __init__(self):
        self.name = {"loc": "地点", "time": "入住日期"}
        self.online = False

    def build(self):
        self.slots = {"loc": '', "time": ''}
        self.online = True

    def tex_ner(self, text):

        obj = {"str": text}
        req_str = json.dumps(obj).encode()

        url = "https://texsmart.qq.com/api"
        r = requests.post(url, data=req_str)
        r.encoding = "utf-8"
        res = json.loads(r.content)
        return res['entity_list']

    def parser_tex(self, text, slots, target_slot=None):
        result = self.tex_ner(text)
        if target_slot is None:
            for i in result:
                if i['tag'].startswith('time'):
                    time = '{0[0]}年{0[1]}月{0[2]}日'.format(i['meaning']['value'])
                    slots['time'] = time
                if i['tag'].startswith('loc') and i['str'] != '酒店':
                    slots['loc'] += i['str']
        else:
            slot_data = [x for x in result if x['tag'].startswith(target_slot)]
            if len(slot_data) == 0:
                return slots, 0
            else:
                slot_data = slot_data[0]
                if target_slot == 'time':
                    time = '{0[0]}年{0[1]}月{0[2]}日'.format(slot_data['meaning']['value'])
                    slots['time'] = time
                elif target_slot == 'loc' and slot_data['str'] != '酒店':
                    slots['loc'] += slot_data['str']

        return slots, 1

    def answer(self, text):
        self.slots, _ = self.parser_tex(text, self.slots)

        items = list(self.slots.items())

        for k, v in items:
            if v == '':
                return "客服：请问%s是？\n" % (self.name[k])
        # print('为您推荐{loc}，{time}入住的房间'.format(**slots))
        self.online = False
        return '为您推荐{loc}，{time}入住的酒店'.format(**self.slots)


if __name__ == '__main__':
    qa = TaskQA()
    question = input('请输入:')
    qa.answer(question)