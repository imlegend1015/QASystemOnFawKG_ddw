#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-10

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class SafeDeviceGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')

        brake_assist = []



        rels_motorcycle_brake_assist = []

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'safe_device' in elem.keys():
                if '刹车辅助(EBA/BAS/BA等)' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['刹车辅助(EBA/BAS/BA等)'])
                    if temp_str1 not in brake_assist:
                        brake_assist.append(temp_str1)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_brake_assist.append([motor, temp_str1])
                    '''
                if 'ABS防抱死' in elem['safe_device'].keys():
                    temp_str2 = ''.join(elem['safe_device']['ABS防抱死'])
                    if temp_str2 not in ABS:
                        ABS.append(temp_str2)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_ABS.append([motor, temp_str2])
                if '制动力分配(EBD/CBC等)' in elem['safe_device'].keys():
                    temp_str3 = ''.join(elem['safe_device']['制动力分配(EBD/CBC等)'])
                    if temp_str3 not in brake_power_distribution:
                        brake_power_distribution.append(temp_str3)
                    #temp_str3 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_brake_power_distribution.append([motor, temp_str3])
                    '''
        return brake_assist,rels_motorcycle_brake_assist



    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        brake_assist, rels_motorcycle_brake_assist = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Brake_assist', brake_assist)
        print('Brake_assist nodes have ' + str(len(brake_assist)) + '\n')
        '''
        neo.create_node('ABS',ABS)
        print('ABS nodes have ' + str(len(ABS)) + '\n')
        neo.create_node('Brake_power_distribution', brake_power_distribution)
        print('Brake_power_distribution nodes have ' + str(len(brake_power_distribution)) + '\n')
        '''
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        brake_assist, rels_motorcycle_brake_assist = self.read_nodes()

        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'brake_assist', rels_motorcycle_brake_assist, 'brake_assist_is',
                                '刹车辅助是')
        '''
        neo.create_relationship('Motorcycle', 'ABS', rels_motorcycle_ABS, 'ABS_is',
                                'ABS防抱死是')
        neo.create_relationship('Motorcycle', 'brake_power_distribution', rels_motorcycle_brake_power_distribution,
                                'brake_power_distribution_is',
                                '制动力分配是')

        '''
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        brake_assist, rels_motorcycle_brake_assist = self.read_nodes()

        f_1 = open('../dict/brake_assist.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(brake_assist)))
        f_1.close()
        '''
        f_2 = open('../dict/ABS.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(ABS)))
        f_2.close()

        f_3 = open('../dict/brake_power_distribution.txt', 'w+', encoding='utf-8')
        f_3.seek(0)
        f_3.truncate()  # 清空文件
        f_3.write('\n'.join(list(brake_power_distribution)))
        f_3.close()
        '''



if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = SafeDeviceGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
