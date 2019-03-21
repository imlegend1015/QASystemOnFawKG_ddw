#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-10

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class GuardTheftGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        sunroof_type = []  # 天窗类型
        roof_rack = []  #车顶行李架

        rels_motorcycle_sunroof_type = []  # 车型-天窗类型关系
        rels_motorcycle_roof_rack = []  # 车型-车顶行李架关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'guard_theft_device' in elem.keys():
                if '天窗类型' in elem['guard_theft_device'].keys():
                    temp_str1 = ''.join(elem['guard_theft_device']['天窗类型'])
                    if elem['guard_theft_device']['天窗类型'] not in sunroof_type:

                        sunroof_type.append(temp_str1)
                    #temp_str2 = ''.join(elem['guard_theft_device']['天窗类型'])
                    #print(temp_str2)
                    rels_motorcycle_sunroof_type.append([motor, temp_str1])
                if '车顶行李架' in elem['guard_theft_device'].keys():
                    temp_str3 = ''.join(elem['guard_theft_device']['车顶行李架'])
                    if elem['guard_theft_device']['车顶行李架'] not in roof_rack:

                        roof_rack.append(temp_str3)
                    #temp_str4 = ''.join(elem['guard_theft_device']['车顶行李架'])
                #print(temp_str2)
                    rels_motorcycle_roof_rack.append([motor, temp_str3])
        return sunroof_type,roof_rack,rels_motorcycle_sunroof_type,rels_motorcycle_roof_rack





    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        sunroof_type, roof_rack, rels_motorcycle_sunroof_type, rels_motorcycle_roof_rack = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Sunroof_type', sunroof_type)
        print('Sunroof_type nodes have ' + str(len(sunroof_type)) + '\n')
        neo.create_node('Roof_rack',roof_rack)
        print('Roof_rack nodes have ' + str(len(roof_rack)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        sunroof_type, roof_rack, rels_motorcycle_sunroof_type, rels_motorcycle_roof_rack = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Sunroof_type', rels_motorcycle_sunroof_type, 'sunroof_type_is',
                                '天窗类型是')
        neo.create_relationship('Motorcycle', 'Roof_rack', rels_motorcycle_roof_rack, 'roof_rack_is',
                                '车顶行李架是')


        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        sunroof_type, roof_rack, rels_motorcycle_sunroof_type, rels_motorcycle_roof_rack = self.read_nodes()

        f_1 = open('../dict/sunroof_type.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(sunroof_type)))
        f_1.close()

        f_2 = open('../dict/roof_rack.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(roof_rack)))
        f_2.close()





if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = GuardTheftGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
