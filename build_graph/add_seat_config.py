#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-11

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class SeatConfigGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        seat_material = []  #座椅材质
        main_seat_adjustment = []  #主座椅调节方式
        sub_seat_adjustment = []  #副座椅调节方式
        main_sub_electric_adjustment = []  #主副驾驶座电动调节
        rear_seat_electric_adjustment = []  #后排座椅电动调节
        rear_seat_down = [] #后排座椅放倒形式

        rels_motorcycle_seat_material = []
        rels_motorcycle_main_seat_adjustment = []
        rels_motorcycle_sub_seat_adjustment = []
        rels_motorcycle_main_sub_electric_adjustment = []
        rels_motorcycle_rear_seat_electric_adjustment = []
        rels_motorcycle_rear_seat_down = []

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'seat_config' in elem.keys():
                if '座椅材质' in elem['seat_config'].keys():
                    temp_str1 = ''.join(elem['seat_config']['座椅材质'])
                    if temp_str1 not in seat_material:
                        seat_material.append(temp_str1)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_seat_material.append([motor, temp_str1])
                if '主座椅调节方式' in elem['seat_config'].keys():
                    temp_str2 = ''.join(elem['seat_config']['主座椅调节方式'])
                    if temp_str2 not in main_seat_adjustment:
                        main_seat_adjustment.append(temp_str2)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_main_seat_adjustment.append([motor, temp_str2])
                if '副座椅调节方式' in elem['seat_config'].keys():
                    temp_str3 = ''.join(elem['seat_config']['副座椅调节方式'])
                    if temp_str3 not in sub_seat_adjustment:
                        sub_seat_adjustment.append(temp_str3)
                    rels_motorcycle_sub_seat_adjustment.append([motor, temp_str3])
                if '主/副驾驶座电动调节' in elem['seat_config'].keys():
                    temp_str4 = ''.join(elem['seat_config']['主/副驾驶座电动调节'])
                    if temp_str4 not in main_sub_electric_adjustment:
                        sub_seat_adjustment.append(temp_str4)
                    rels_motorcycle_main_sub_electric_adjustment.append([motor, temp_str4])
                if '后排座椅电动调节' in elem['seat_config'].keys():
                    temp_str5 = ''.join(elem['seat_config']['后排座椅电动调节'])
                    if temp_str5 not in rear_seat_electric_adjustment:
                        rear_seat_electric_adjustment.append(temp_str5)
                    rels_motorcycle_rear_seat_electric_adjustment.append([motor, temp_str5])
                if '后排座椅放倒形式' in elem['seat_config'].keys():
                    temp_str6 = ''.join(elem['seat_config']['后排座椅放倒形式'])
                    if temp_str6 not in rear_seat_down:
                        rear_seat_down.append(temp_str6)
                    rels_motorcycle_rear_seat_down.append([motor, temp_str6])
        return seat_material, main_seat_adjustment, sub_seat_adjustment,main_sub_electric_adjustment, rear_seat_electric_adjustment, rear_seat_down,rels_motorcycle_seat_material, rels_motorcycle_main_seat_adjustment, rels_motorcycle_sub_seat_adjustment, rels_motorcycle_main_sub_electric_adjustment, rels_motorcycle_rear_seat_electric_adjustment, rels_motorcycle_rear_seat_down

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        seat_material, main_seat_adjustment, sub_seat_adjustment,main_sub_electric_adjustment, rear_seat_electric_adjustment, rear_seat_down, rels_motorcycle_seat_material, rels_motorcycle_main_seat_adjustment, rels_motorcycle_sub_seat_adjustment, rels_motorcycle_main_sub_electric_adjustment, rels_motorcycle_rear_seat_electric_adjustment, rels_motorcycle_rear_seat_down = self.read_nodes()

        neo = Neo4jOp()

        neo.create_node(' Seat_material', seat_material)
        print(' seat_material nodes have ' + str(len(seat_material)) + '\n')

        neo.create_node('Main_seat_adjustment', main_seat_adjustment)
        print('Main_seat_adjustment nodes have ' + str(len(main_seat_adjustment)) + '\n')

        neo.create_node('Sub_seat_adjustment', sub_seat_adjustment)
        print('Sub_seat_adjustment nodes have ' + str(len(sub_seat_adjustment)) + '\n')

        neo.create_node('Main_sub_electric_adjustment', main_sub_electric_adjustment)
        print('Main_sub_electric_adjustment nodes have ' + str(len(main_sub_electric_adjustment)) + '\n')

        neo.create_node('Rear_seat_electric_adjustment', rear_seat_electric_adjustment)
        print('Rear_seat_electric_adjustment nodes have ' + str(len(rear_seat_electric_adjustment)) + '\n')

        neo.create_node('Rear_seat_down', rear_seat_down)
        print('Rear_seat_down nodes have ' + str(len(rear_seat_down)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        seat_material, main_seat_adjustment, sub_seat_adjustment,main_sub_electric_adjustment, rear_seat_electric_adjustment, rear_seat_down, rels_motorcycle_seat_material, rels_motorcycle_main_seat_adjustment, rels_motorcycle_sub_seat_adjustment, rels_motorcycle_main_sub_electric_adjustment, rels_motorcycle_rear_seat_electric_adjustment, rels_motorcycle_rear_seat_down = self.read_nodes()

        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'seat_material', rels_motorcycle_seat_material, 'Seat_material_is',
                                '座椅材质是')

        neo.create_relationship('Motorcycle', 'main_seat_adjustment', rels_motorcycle_main_seat_adjustment,
                                'Main_seat_adjustment_is',
                                '主座椅调节方式是')

        neo.create_relationship('Motorcycle', 'sub_seat_adjustment', rels_motorcycle_sub_seat_adjustment,
                                'sub_seat_adjustment_is',
                                '副座椅调节方式是')

        neo.create_relationship('Motorcycle', 'main_sub_electric_adjustment', rels_motorcycle_main_sub_electric_adjustment,
                                'Main_sub_electric_adjustment_is',
                                '主/副驾驶座电动调节方式是')

        neo.create_relationship('Motorcycle', 'rear_seat_electric_adjustment', rels_motorcycle_rear_seat_electric_adjustment,
                                'Rear_seat_electric_adjustment_is',
                                '后排座椅电动调节方式是')

        neo.create_relationship('Motorcycle', 'rear_seat_down', rels_motorcycle_rear_seat_down,
                                'rear_seat_down_is',
                                '后排座椅放倒形式是')

        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        seat_material, main_seat_adjustment, sub_seat_adjustment,main_sub_electric_adjustment, rear_seat_electric_adjustment, rear_seat_down, rels_motorcycle_seat_material, rels_motorcycle_main_seat_adjustment, rels_motorcycle_sub_seat_adjustment, rels_motorcycle_main_sub_electric_adjustment, rels_motorcycle_rear_seat_electric_adjustment, rels_motorcycle_rear_seat_down = self.read_nodes()


        f_1 = open('../dict/seat/seat_material.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(seat_material)))
        f_1.close()

        f_2 = open('../dict/seat/main_seat_adjustment.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(main_seat_adjustment)))
        f_2.close()

        f_3 = open('../dict/seat/sub_seat_adjustment.txt', 'w+', encoding='utf-8')
        f_3.seek(0)
        f_3.truncate()  # 清空文件
        f_3.write('\n'.join(list(sub_seat_adjustment)))
        f_3.close()

        f_4 = open('../dict/seat/main_sub_electric_adjustment.txt', 'w+', encoding='utf-8')
        f_4.seek(0)
        f_4.truncate()  # 清空文件
        f_4.write('\n'.join(list(main_sub_electric_adjustment)))
        f_4.close()

        f_5 = open('../dict/seat/rear_seat_electric_adjustment.txt', 'w+', encoding='utf-8')
        f_5.seek(0)
        f_5.truncate()  # 清空文件
        f_5.write('\n'.join(list(rear_seat_electric_adjustment)))
        f_5.close()

        f_6 = open('../dict/seat/rear_seat_down.txt', 'w+', encoding='utf-8')
        f_6.seek(0)
        f_6.truncate()  # 清空文件
        f_6.write('\n'.join(list(rear_seat_down)))
        f_6.close()








if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = SeatConfigGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
