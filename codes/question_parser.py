#!/usr/bin/env python3
# coding: utf-8

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            #地址
            if question_type == 'hotel_address':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            #电话
            elif question_type == 'hotel_phone':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 地铁
            elif question_type == 'hotel_subway':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 机场
            elif question_type == 'hotel_airport':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 火车站
            elif question_type == 'hotel_train_station':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 周边景区
            elif question_type == 'hotel_surrounding_scenic_spots':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 周边交通
            elif question_type == 'hotel_surrounding_traffic':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 商场超市
            elif question_type == 'hotel_shopping_mall_supermarket':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # wifi
            elif question_type == 'hotel_have_wifi':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 早餐
            elif question_type == 'hotel_breadfast':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 停车场
            elif question_type == 'hotel_parking':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 餐厅
            elif question_type == 'hotel_dining_hall':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 无烟房
            elif question_type == 'hotel_no_smoking_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 健身房
            elif question_type == 'hotel_gym':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 棋牌室
            elif question_type == 'hotel_chess_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 残疾人设施
            elif question_type == 'hotel_disabled_facilities':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 会议室
            elif question_type == 'hotel_meeting_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 温泉
            elif question_type == 'hotel_spa':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 交通站
            elif question_type == 'hotel_traffic_station':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 24小时热水
            elif question_type == 'hotel_hot_water':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 商务中心
            elif question_type == 'hotel_business_center':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 电梯
            elif question_type == 'hotel_elevator':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 泳池
            elif question_type == 'hotel_swimming_pool':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # SPA
            elif question_type == 'hotel_SPA':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 烫衣服务
            elif question_type == 'hotel_ironing_service':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 自助办理入住
            elif question_type == 'hotel_self_checkin':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 装修时间
            elif question_type == 'hotel_renovation_time':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 亲子房
            elif question_type == 'hotel_family_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 净化房
            elif question_type == 'hotel_clean_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 商务房
            elif question_type == 'hotel_business_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 智能房
            elif question_type == 'hotel_smart_room':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 行政房
            elif question_type == 'hotel_executive_suite':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))
            # 套房
            elif question_type == 'hotel_suite':
                sql = self.sql_transfer(question_type, entity_dict.get('hotel'))


            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_can_eat':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_getway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        #查看酒店电话
        if question_type == 'hotel_phone':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.电话".format(i) for i in entities]

        #查看酒店地址
        elif question_type == 'hotel_address':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.地址".format(i) for i in entities]
        # 地铁
        elif question_type == 'hotel_subway':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.地铁".format(i) for i in entities]
        # 机场
        elif question_type == 'hotel_airport':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.机场".format(i) for i in entities]
        # 火车站
        elif question_type == 'hotel_train_station':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.火车站".format(i) for i in entities]
        # 周边景区
        elif question_type == 'hotel_surrounding_scenic_spots':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.周边景区".format(i) for i in entities]
        # 周边交通
        elif question_type == 'hotel_surrounding_traffic':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.周边交通".format(i) for i in entities]
        # 商场超市
        elif question_type == 'hotel_shopping_mall_supermarket':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.商场超市".format(i) for i in entities]
        # wifi
        elif question_type == 'hotel_have_wifi':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.wifi".format(i) for i in entities]
        # 早餐
        elif question_type == 'hotel_breadfast':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.早餐".format(i) for i in entities]
        # 停车场
        elif question_type == 'hotel_parking':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.停车场".format(i) for i in entities]
        # 餐厅
        elif question_type == 'hotel_dining_hall':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.餐厅".format(i) for i in entities]
        # 无烟房
        elif question_type == 'hotel_no_smoking_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.无烟房".format(i) for i in entities]
        # 健身房
        elif question_type == 'hotel_gym':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.健身房".format(i) for i in entities]
        # 棋牌室
        elif question_type == 'hotel_chess_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.棋牌室".format(i) for i in entities]
        # 残疾人设施
        elif question_type == 'hotel_disabled_facilities':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.残疾人设施".format(i) for i in entities]
        # 会议室
        elif question_type == 'hotel_meeting_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.会议室".format(i) for i in entities]
        # 温泉
        elif question_type == 'hotel_spa':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.温泉".format(i) for i in entities]
        # 交通站
        elif question_type == 'hotel_traffic_station':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.交通站".format(i) for i in entities]
        # 24小时热水
        elif question_type == 'hotel_hot_water':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.热水".format(i) for i in entities]
        # 商务中心
        elif question_type == 'hotel_business_center':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.商务中心".format(i) for i in entities]
        # 电梯
        elif question_type == 'hotel_elevator':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.电梯".format(i) for i in entities]
        # 泳池
        elif question_type == 'hotel_swimming_pool':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.泳池".format(i) for i in entities]
        # SPA
        elif question_type == 'hotel_SPA':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.SPA".format(i) for i in entities]
        # 烫衣服务
        elif question_type == 'hotel_ironing_service':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.烫衣服务".format(i) for i in entities]
        # 自助办理入住
        elif question_type == 'hotel_self_checkin':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.自助办理入住".format(i) for i in entities]
        # 装修时间
        elif question_type == 'hotel_renovation_time':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.装修时间".format(i) for i in entities]
        # 亲子房
        elif question_type == 'hotel_family_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.亲子房".format(i) for i in entities]
        # 净化房
        elif question_type == 'hotel_clean_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.净化房".format(i) for i in entities]
        # 商务房
        elif question_type == 'hotel_business_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.商务房".format(i) for i in entities]
        # 智能房
        elif question_type == 'hotel_smart_room':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.智能房".format(i) for i in entities]
        # 行政房
        elif question_type == 'hotel_executive_suite':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.行政房".format(i) for i in entities]
        # 套房
        elif question_type == 'hotel_suite':
            sql = ["MATCH (m:Hotel) where m.name = '{0}' return m.name, m.套房".format(i) for i in entities]


        # 查询疾病的原因
        elif question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病传染性
        elif question_type == 'disease_getway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.get_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病是否可以吃某种食物：
        elif question_type == 'disease_can_eat':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.can_eat".format(i) for i in entities]

        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        print(sql)
        return sql



if __name__ == '__main__':

    from question_classifier import *

    handler = QuestionPaser()
    QChandler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = QChandler.classify(question)
        print(data)
        sqls = handler.parser_main(data)
        print(sqls)