#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-11

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class SteeringWheelGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        steering_wheel_material = []  #方向盘材质

        rels_motorcycle_steering_wheel_material = []  #
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'inner_config' in elem.keys():
                if '方向盘材质' in elem['inner_config'].keys():
                    temp_str1 = ''.join(elem['inner_config']['方向盘材质'])
                    if temp_str1 not in steering_wheel_material:
                        steering_wheel_material.append(temp_str1)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_steering_wheel_material.append([motor, temp_str1])

        return steering_wheel_material, rels_motorcycle_steering_wheel_material

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        steering_wheel_material, rels_motorcycle_steering_wheel_material = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Steering_wheel_material', steering_wheel_material)
        print('Steering_wheel_material nodes have ' + str(len(steering_wheel_material)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        steering_wheel_material, rels_motorcycle_steering_wheel_material = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Steering_wheel_material', rels_motorcycle_steering_wheel_material, 'steering_wheel_material_is',
                                '方向盘材质是')

        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        steering_wheel_material, rels_motorcycle_steering_wheel_material = self.read_nodes()

        f_1 = open('../dict/steering_wheel_material.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(steering_wheel_material)))
        f_1.close()







if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = SteeringWheelGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
