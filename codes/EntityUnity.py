import jieba
import jieba.posseg as pseg
import re
import datetime
import os

class EntityUnity:
    def __init__(self):
        self.dict_path = './dict'
        self.d_4_delete, self.stop_word, self.d_city_province = self.my_initial()
        jieba.load_userdict(os.path.join(self.dict_path, 'Hotel_HotelBrand.txt'))

    # 提示：可以分析公司全称的组成方式，将“地名”、“公司主体部分”、“公司后缀”区分开，并制定一些启发式的规则
    # TODO：建立main_extract，当输入公司名，返回会被统一的简称
    def main_extract(self, company_name):
        """
        company_name  输入的公司名
        stop_word 停用词
        d_4_delete 后缀名
        d_city_province 地区
        """

        company_name_list = pseg.cut(company_name)
        # 前置获取到的地名
        company_name_list = self.city_prov_ahead(company_name_list, self.d_city_province)
        # 去除通用后缀
        company_name_list = self.delete_suffix(company_name_list, self.d_4_delete)

        # 你的自定义function
        company_name_list = self.my_function(company_name_list)

        company_name = ''.join(company_name_list)
        return company_name


    # 功能：将公司名中地名提前
    def city_prov_ahead(self,company_name_list, d_city_province):
        # 公司名中地名的部分
        city_prov_lst = []
        # 公司名中其他部分
        other_lst = []
        # TODO: 将公司名中地名的部分添加至city_prov_lst，将公司名中非地名的部分添加至other_lst。
        for word, flag in company_name_list:
            if word in self.d_city_province:
                city_prov_lst.append(word)
            else:
                other_lst.append(word)
        return city_prov_lst + other_lst


    # 功能：去除通用后缀
    def delete_suffix(self, company_name_list, d_4_delete):
        # TODO：识别公司名中通用后缀并删除
        for word in company_name_list[:]:
            if word in d_4_delete:
                company_name_list.remove(word)
        return company_name_list


    # 你的自定义function
    def my_function(self, company_name_list):
        other_stop_word = \
            set(('分行', '丽呈华廷','丽呈别院','丽呈华廷','丽呈東谷','丽呈睿轩','丽呈'))
        for word in company_name_list[:]:
            # 去除“分行”、“财务”
            if word in other_stop_word:
                company_name_list.remove(word)
            # 去除空格
            word = word.replace(' ', '')
        return company_name_list


    # 初始加载步骤
    # 输出需要使用的词典
    def my_initial(self):
        # 加载城市名、省份名
        d_city_province = set()
        with open(os.path.join(self.dict_path,"co_City_Dim.txt"), encoding='utf-8') as cts:
            for ct in cts.readlines():
                d_city_province.add(ct[:-1])
        with open(os.path.join(self.dict_path,"co_Province_Dim.txt"), encoding='utf-8') as prvs:
            for prv in prvs.readlines():
                d_city_province.add(prv[:-1])
        # 加载公司后缀
        d_4_delete = set()
        with open(os.path.join(self.dict_path,r"company_suffix.txt"), encoding='utf-8') as sfs:
            for sf in sfs.readlines():
                d_4_delete.add(sf[:-1])
        #加载公司领域
        scope = set()
        with open(os.path.join(self.dict_path,r"company_business_scope.txt"), encoding='utf-8') as sp:
            for p in sp.readline():
                scope.add(p[:-1])
        scope = set()
        # 加载停用词
        stop_word = set()
        with open(r"./dict/stopwords.txt", encoding='utf-8') as sts:
            for st in sts.readlines():
                stop_word.add(st[:-1])
        return d_4_delete, stop_word, d_city_province

if __name__ == '__main__':
    entityUnity = EntityUnity()
    company_name = "苏州新城花园丽呈华廷酒店"
    company_name = entityUnity.main_extract(company_name)

    print(company_name)
