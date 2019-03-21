#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-10

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class LightingGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        '''
        low_beam_lights = []  # 近光灯光源
        high_beam_lights = [] #远光灯光源
        rels_motorcycle_low_beam = []  # 车型-近光灯关系
        rels_motorcycle_high_beam = []  # 车型-远光灯关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'lighting' in elem.keys():
                if '近光灯光源' in elem['lighting'].keys():
                    if elem['lighting']['近光灯光源'] not in low_beam_lights:
                        low_beam_lights.append(elem['lighting']['近光灯光源'])
                    rels_motorcycle_low_beam.append([motor, elem['lighting']['近光灯光源']])
                if '远光灯光源' in elem['lighting'].keys():
                    if elem['lighting']['远光灯光源'] not in high_beam_lights:
                        high_beam_lights.append(elem['lighting']['远光灯光源'])
                    rels_motorcycle_high_beam.append([motor, elem['lighting']['远光灯光源']])
        return low_beam_lights,high_beam_lights, rels_motorcycle_low_beam,rels_motorcycle_high_beam
        '''
        #auto_lights = []
        height_lights = []
        #rels_motorcycle_auto_light = []  # 车型-近光灯关系
        rels_motorcycle_height_lights = []
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'lighting' in elem.keys():
                if '自动头灯' in elem['lighting'].keys():
                    if '大灯高度可调' in elem['lighting'].keys():
                        if elem['lighting']['大灯高度可调'] not in height_lights:
                            height_lights.append(elem['lighting']['大灯高度可调'])
                    rels_motorcycle_height_lights.append([motor, elem['lighting']['大灯高度可调']])

        return height_lights,rels_motorcycle_height_lights

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        '''
        low_beam_lights, high_beam_lights, rels_motorcycle_low_beam, rels_motorcycle_high_beam = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Low_beam_lights', low_beam_lights)
        neo.create_node('High_beam_lights',high_beam_lights)
        print('Low_beam_lights nodes have ' + str(len(low_beam_lights)) + '\n')
        print('High_beam_lights nodes have ' + str(len(high_beam_lights)) + '\n')
        '''
        height_lights, rels_motorcycle_height_lights = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Height_Lights',height_lights)
        print('Height_Lights nodes have ' + str(len(height_lights)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        """
        low_beam_lights, high_beam_lights, rels_motorcycle_low_beam, rels_motorcycle_high_beam = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Low_beam_lights', rels_motorcycle_low_beam, 'Low_beam_lights_is',
                                '近光灯光源是')
        neo.create_relationship('Motorcycle', 'High_beam_lights', rels_motorcycle_high_beam, 'High_beam_lights_is',
                                '远光灯光源是')
                                """
        height_lights, rels_motorcycle_height_lights = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Height_Lights', rels_motorcycle_height_lights, 'Height_Lights_is',
                                '大灯高度可调是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        #low_beam_lights, high_beam_lights, rels_motorcycle_low_beam, rels_motorcycle_high_beam = self.read_nodes()
        height_lights, rels_motorcycle_height_lights = self.read_nodes()


        f_2 = open('../dict/height_lighting.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(height_lights)))
        #f.write('\n'.join(list(high_beam_lights)))


        f_2.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = LightingGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
