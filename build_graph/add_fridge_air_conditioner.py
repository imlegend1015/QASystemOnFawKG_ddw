#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-11

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class FridgeAirGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        air_temperature_control = []  #空调温度控制方式

        rels_motorcycle_temperature_control = []  # 车型-空调温度控制方式关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'fridge_air_conditioner' in elem.keys():
                if '空调温度控制方式' in elem['fridge_air_conditioner'].keys():
                    temp_str1 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    if temp_str1 not in air_temperature_control:
                        air_temperature_control.append(temp_str1)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_temperature_control.append([motor, temp_str1])

        return air_temperature_control,rels_motorcycle_temperature_control

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        air_temperature_control, rels_motorcycle_temperature_control = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Air_temperature_control', air_temperature_control)
        print('Air_temperature_control nodes have ' + str(len(air_temperature_control)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        air_temperature_control, rels_motorcycle_temperature_control = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Air_temperature_control', rels_motorcycle_temperature_control, 'Air_temperature_control_is',
                                '空调温度控制方式是')

        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        air_temperature_control, rels_motorcycle_temperature_control = self.read_nodes()

        f_1 = open('../dict/air_temperature_control.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(air_temperature_control)))
        f_1.close()







if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = FridgeAirGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
