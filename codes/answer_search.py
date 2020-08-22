#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Date: 18-10-5

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            # "http://localhost:7474/db/data"  # py2neo 2.0.8写法
            host="127.0.0.1",  # py2neo 3写法
            user="neo4j",
            password="123456"
        )
        self.num_limit = 30

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'hotel_address':
            desc = [i['m.地址'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的地址是: {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'hotel_phone':
            desc = [i['m.电话'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的电话是: {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'hotel_subway':
            desc = [i['m.地铁'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))

        elif question_type == 'hotel_airport':
            desc = [i['m.机场'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))

        elif question_type == 'hotel_train_station':
            desc = [i['m.火车站'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))

        elif question_type == 'hotel_surrounding_scenic_spots':
            desc = [i['m.周边景区'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))

        elif question_type == 'hotel_surrounding_traffic':
            desc = [i['m.周边交通'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))

        elif question_type == 'hotel_shopping_mall_supermarket':
            desc = [i['m.商场超市'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # wifi
        elif question_type == 'hotel_have_wifi':
            desc = [i['m.wifi'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 早餐
        elif question_type == 'hotel_breadfast':
            desc = [i['m.早餐'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 停车场
        elif question_type == 'hotel_parking':
            desc = [i['m.停车房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 餐厅
        elif question_type == 'hotel_dining_hall':
            desc = [i['m.餐厅'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 无烟房
        elif question_type == 'hotel_no_smoking_room':
            desc = [i['m.无烟房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 健身房
        elif question_type == 'hotel_gym':
            desc = [i['m.健身房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 棋牌室
        elif question_type == 'hotel_chess_room':
            desc = [i['m.棋牌室'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 残疾人设施
        elif question_type == 'hotel_disabled_facilities':
            desc = [i['m.残疾人设施'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 会议室
        elif question_type == 'hotel_meeting_room':
            desc = [i['m.会议室'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 温泉
        elif question_type == 'hotel_spa':
            desc = [i['m.温泉'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 交通站
        elif question_type == 'hotel_traffic_station':
            desc = [i['m.交通站'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 热水
        elif question_type == 'hotel_hot_water':
            desc = [i['m.热水'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 商务中心
        elif question_type == 'hotel_business_center':
            desc = [i['m.商务中心'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 电梯
        elif question_type == 'hotel_elevator':
            desc = [i['m.电梯'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 泳池
        elif question_type == 'hotel_swimming_pool':
            desc = [i['m.泳池'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # SPA
        elif question_type == 'hotel_SPA':
            desc = [i['m.SPA'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 烫衣服务
        elif question_type == 'hotel_ironing_service':
            desc = [i['m.烫衣服务'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 自助办理入住
        elif question_type == 'hotel_self_checkin':
            desc = [i['m.自助办理入住'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 装修时间
        elif question_type == 'hotel_renovation_time':
            desc = [i['m.装修时间'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 亲子房
        elif question_type == 'hotel_family_room':
            desc = [i['m.亲子房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 净化房
        elif question_type == 'hotel_clean_room':
            desc = [i['m.净化房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 商务房
        elif question_type == 'hotel_business_room':
            desc = [i['m.商务房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 智能房
        elif question_type == 'hotel_smart_room':
            desc = [i['m.智能房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 行政房
        elif question_type == 'hotel_executive_suite':
            desc = [i['m.行政房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))
        # 套房
        elif question_type == 'hotel_suite':
            desc = [i['m.套房'] for i in answers]
            final_answer = '{0}'.format('；'.join(desc))


        elif question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            print(answers)
            print(desc)
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_getway':
            desc = [i['m.get_way'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的传播方式为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的并发症包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_can_eat':
            desc = [answers[0]['m.can_eat']]
            print(answers)
            print(desc)
            subject = answers[0]['m.name']
            print(subject)
            if desc:
                final_answer = '{0}可以吃/喝：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = '{0}推荐{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        print("final_answer: ",final_answer)
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
