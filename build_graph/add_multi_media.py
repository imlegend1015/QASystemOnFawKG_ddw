#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-11

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class MultiMediaGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        central_control_screen_size = []  # 中控液晶屏尺寸
        bluetooth_car_phone = [] #蓝牙车载电话
        rels_motorcycle_central_control = []  # 车型-中控液晶屏关系
        rels_motorcycle_bluetooth_phone = []  # 车型-蓝牙车载电话关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'multi_media' in elem.keys():
                if '中控液晶屏尺寸' in elem['multi_media'].keys():
                    if elem['multi_media']['中控液晶屏尺寸'] not in central_control_screen_size:
                        temp_str1 = ''.join(elem['multi_media']['中控液晶屏尺寸'])
                        central_control_screen_size.append(temp_str1)
                    temp_str2 = ''.join(elem['multi_media']['中控液晶屏尺寸'])
                    #print(temp_str2)
                    rels_motorcycle_central_control.append([motor, temp_str2])
                if '蓝牙/车载电话' in elem['multi_media'].keys():
                    if elem['multi_media']['蓝牙/车载电话'] not in bluetooth_car_phone:
                        temp_str3 = ''.join(elem['multi_media']['蓝牙/车载电话'])
                        bluetooth_car_phone.append(temp_str3)
                    temp_str4 = ''.join(elem['multi_media']['蓝牙/车载电话'])
                #print(temp_str2)
                    rels_motorcycle_bluetooth_phone.append([motor, temp_str4])
        return central_control_screen_size, bluetooth_car_phone, rels_motorcycle_central_control, rels_motorcycle_bluetooth_phone





    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        central_control_screen_size, bluetooth_car_phone, rels_motorcycle_central_control, rels_motorcycle_bluetooth_phone = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Central_control_screen_size', central_control_screen_size)
        print('Central_control_screen_size nodes have ' + str(len(central_control_screen_size)) + '\n')
        neo.create_node('Bluetooth_car_phone',bluetooth_car_phone)
        print('Bluetooth_car_phone nodes have ' + str(len(bluetooth_car_phone)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        central_control_screen_size, bluetooth_car_phone, rels_motorcycle_central_control, rels_motorcycle_bluetooth_phone = self.read_nodes()

        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Central_control_screen_size', rels_motorcycle_central_control, 'Central_control_screen_size_is',
                                '中控液晶屏尺寸是')
        neo.create_relationship('Motorcycle', 'Bluetooth_car_phone', rels_motorcycle_bluetooth_phone, 'Bluetooth_car_phone_is',
                                '蓝牙/车载电话是')


        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        central_control_screen_size, bluetooth_car_phone, rels_motorcycle_central_control, rels_motorcycle_bluetooth_phone = self.read_nodes()

        f_1 = open('../dict/central_control_screen_size.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(central_control_screen_size)))
        f_1.close()

        f_2 = open('../dict/bluetooth_car_phone.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(bluetooth_car_phone)))
        f_2.close()





if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = MultiMediaGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
