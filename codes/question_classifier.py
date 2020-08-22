#!/usr/bin/env python3
# coding: utf-8

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.hotel_path = os.path.join(cur_dir, 'dict/hotel.txt')

        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.producer_path = os.path.join(cur_dir, 'dict/producer.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        # 加载特征词
        self.hotel_wds = [i.strip() for i in open(self.hotel_path, encoding='utf-8') if i.strip()]

        self.disease_wds= [i.strip() for i in open(self.disease_path,encoding='utf-8') if i.strip()]
        self.department_wds= [i.strip() for i in open(self.department_path,encoding='utf-8') if i.strip()]
        self.check_wds= [i.strip() for i in open(self.check_path,encoding='utf-8') if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path,encoding='utf-8') if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path,encoding='utf-8') if i.strip()]
        self.producer_wds= [i.strip() for i in open(self.producer_path,encoding='utf-8') if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path,encoding='utf-8') if i.strip()]

        self.region_words = set(self.hotel_wds + self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding='utf-8') if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        #电话
        self.phone_qwds = ['电话','联系','手机号','座机','客服','前台','号码']
        #地址
        self.address_qwds = ['地址', '在哪儿','哪里','位置']
        # 机场
        self.airport = ['机场']
        #地铁
        self.subway = ['地铁','公交','几号线']
        # 火车站
        self.train_station = ['火车']
        # 周边景区
        self.surrounding_scenic_spots = ['周边景区','好玩的','旅游','景点']
        # 周边交通
        self.surrounding_traffic = ['周边交通','交通','怎么去']
        # 商场超市
        self.shopping_mall_supermarket = ['商场','超市']
        # wifi
        self.have_wifi = ['wifi','无线','网络']
        # 早餐
        self.breadfast  = ['早餐','早饭']
        # 停车场
        self.parking  = ['停车','泊车']
        # 餐厅
        self.dining_hall = ['餐厅','吃饭']
        # 无烟房
        self.no_smoking_room = ['无烟房']
        # 健身房
        self.gym = ['健身','跑步']
        # 棋牌室
        self.chess_room = ['棋牌室','打牌']
        # 残疾人设施
        self.disabled_facilities = ['残疾人设施','残疾人']
        # 会议室
        self.meeting_room = ['会议','开会']
        # 温泉
        self.spa = ['温泉','洗浴']
        # 交通站
        self.traffic_station = ['交通站']
        # 热水
        self.hot_water = ['热水','洗澡']
        # 商务中心
        self.business_center = ['商务中心']
        # 电梯
        self.elevator = ['电梯','爬楼梯']
        # 泳池
        self.swimming_pool = ['泳池','游泳']
        # SPA
        self.SPA = ['SPA','水疗']
        # 烫衣服务
        self.ironing_service = ['烫衣','熨烫']
        # 自助办理入住
        self.self_checkin = ['自助办理','自己办']
        # 装修时间
        self.renovation_time = ['装修','装潢']
        # 亲子房
        self.family_room = ['亲子']
        # 净化房
        self.clean_room = ['净化']
        # 商务房
        self.business_room = ['商务房']
        # 智能房
        self.smart_room = ['智能房']
        # 行政房
        self.executive_suite = ['行政房']
        # 套房
        self.suite = ['套房','套间']


        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '会引起']
        self.cause_qwds = ['原因','成因', '病因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现', '引起','有关']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['吃','药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不','日常','护理']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.getway_qwds = ['传染']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要','可以治']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            if 'diseases_dict' in globals():    # 判断是否是首次提问，若首次提问，则diseases_dict无值
                medical_dict = diseases_dict
            else:
                return {}
        print("medical_dict : ", medical_dict)
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        question_types = []

        # 电话
        if self.check_words(self.phone_qwds, question) and ('hotel' in types):
            question_type = 'hotel_phone'
            question_types.append(question_type)
        # 地址
        if self.check_words(self.address_qwds, question) and ('hotel' in types):
            question_type = 'hotel_address'
            question_types.append(question_type)
        # 地铁
        if self.check_words(self.subway, question) and ('hotel' in types):
            question_type = 'hotel_subway'
            question_types.append(question_type)

        # 机场
        if self.check_words(self.airport, question) and ('hotel' in types):
            question_type = 'hotel_airport'
            question_types.append(question_type)
        # 火车站
        if self.check_words(self.train_station, question) and ('hotel' in types):
            question_type = 'hotel_train_station'
            question_types.append(question_type)
        # 周边景区
        if self.check_words(self.surrounding_scenic_spots, question) and ('hotel' in types):
            question_type = 'hotel_surrounding_scenic_spots'
            question_types.append(question_type)
        # 周边交通
        if self.check_words(self.surrounding_traffic, question) and ('hotel' in types):
            question_type = 'hotel_surrounding_traffic'
            question_types.append(question_type)
        # 商场超市
        if self.check_words(self.shopping_mall_supermarket, question) and ('hotel' in types):
            question_type = 'hotel_shopping_mall_supermarket'
            question_types.append(question_type)
        # wifi
        if self.check_words(self.have_wifi, question) and ('hotel' in types):
            question_type = 'hotel_have_wifi'
            question_types.append(question_type)
        # 早餐
        if self.check_words(self.breadfast, question) and ('hotel' in types):
            question_type = 'hotel_breadfast'
            question_types.append(question_type)
        # 停车场
        if self.check_words(self.parking, question) and ('hotel' in types):
            question_type = 'hotel_parking'
            question_types.append(question_type)
        # 餐厅
        if self.check_words(self.dining_hall, question) and ('hotel' in types):
            question_type = 'hotel_dining_hall'
            question_types.append(question_type)
        # 无烟房
        if self.check_words(self.no_smoking_room, question) and ('hotel' in types):
            question_type = 'hotel_no_smoking_room'
            question_types.append(question_type)
        # 健身房
        if self.check_words(self.gym, question) and ('hotel' in types):
            question_type = 'hotel_gym'
            question_types.append(question_type)
        # 棋牌室
        if self.check_words(self.chess_room, question) and ('hotel' in types):
            question_type = 'hotel_chess_room'
            question_types.append(question_type)
        # 残疾人设施
        if self.check_words(self.disabled_facilities, question) and ('hotel' in types):
            question_type = 'hotel_disabled_facilities'
            question_types.append(question_type)
        # 会议室
        if self.check_words(self.meeting_room, question) and ('hotel' in types):
            question_type = 'hotel_meeting_room'
            question_types.append(question_type)
        # 温泉
        if self.check_words(self.spa, question) and ('hotel' in types):
            question_type = 'hotel_spa'
            question_types.append(question_type)
        # 交通站
        if self.check_words(self.traffic_station, question) and ('hotel' in types):
            question_type = 'hotel_traffic_station'
            question_types.append(question_type)
        # 24小时热水
        if self.check_words(self.hot_water, question) and ('hotel' in types):
            question_type = 'hotel_hot_water'
            question_types.append(question_type)
        # 商务中心
        if self.check_words(self.business_center, question) and ('hotel' in types):
            question_type = 'hotel_business_center'
            question_types.append(question_type)
        # 电梯
        if self.check_words(self.elevator, question) and ('hotel' in types):
            question_type = 'hotel_elevator'
            question_types.append(question_type)
        # 泳池
        if self.check_words(self.swimming_pool, question) and ('hotel' in types):
            question_type = 'hotel_swimming_pool'
            question_types.append(question_type)
        # SPA
        if self.check_words(self.SPA, question) and ('hotel' in types):
            question_type = 'hotel_SPA'
            question_types.append(question_type)
        # 烫衣服务
        if self.check_words(self.ironing_service, question) and ('hotel' in types):
            question_type = 'hotel_ironing_service'
            question_types.append(question_type)
        # 自助办理入住
        if self.check_words(self.self_checkin, question) and ('hotel' in types):
            question_type = 'hotel_self_checkin'
            question_types.append(question_type)
        # 装修时间
        if self.check_words(self.renovation_time, question) and ('hotel' in types):
            question_type = 'hotel_renovation_time'
            question_types.append(question_type)
        # 亲子房
        if self.check_words(self.family_room, question) and ('hotel' in types):
            question_type = 'hotel_family_room'
            question_types.append(question_type)
        # 净化房
        if self.check_words(self.clean_room, question) and ('hotel' in types):
            question_type = 'hotel_clean_room'
            question_types.append(question_type)
        # 商务房
        if self.check_words(self.business_room, question) and ('hotel' in types):
            question_type = 'hotel_business_room'
            question_types.append(question_type)
        # 智能房
        if self.check_words(self.smart_room, question) and ('hotel' in types):
            question_type = 'hotel_smart_room'
            question_types.append(question_type)
        # 行政房
        if self.check_words(self.executive_suite, question) and ('hotel' in types):
            question_type = 'hotel_executive_suite'
            question_types.append(question_type)
        # 套房
        if self.check_words(self.suite, question) and ('hotel' in types):
            question_type = 'hotel_suite'
            question_types.append(question_type)

        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            if self.check_words(['能吃','能喝','可以吃','可以喝'], question):
                question_types.append('disease_can_eat')
            print(question_type)
            question_types.append(question_type)

        #已知食物找疾病
        if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types and 'disease' not in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        #　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病医疗周期
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types :
            question_type = 'disease_easyget'
            question_types.append(question_type)

        # 疾病传染性
        if self.check_words(self.getway_qwds, question) and 'disease' in types:
            question_type = 'disease_getway'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，且类型为疾病，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，且类型为症状，那么则将该症状的疾病信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.hotel_wds:
                wd_dict[wd].append('hotel')

            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()         # 初始化trie树
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))     # 向trie树中添加单词
        actree.make_automaton()    # 将trie树转化为Aho-Corasick自动机
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '乙肝'))
            wd = i[1][1]      # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)       # stop_wds取重复的短的词，如region_wds=['乙肝', '肝硬化', '硬化']，则stop_wds=['硬化']
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}  # 获取词和词所对应的实体类型
        global diseases_dict
        if final_dict:
            diseases_dict = final_dict
        else:
            diseases_dict = {}
        print("final_dict : ",final_dict)
        if 'diseases_dict' in globals():
            print("diseases_dict : ",diseases_dict)
        else:
            print("diseases_dict does not exist.")
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)