#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-10

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class ChassisTranGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        chassis_trans = []  # 驱动方式
        rels_motorcycle_chassis = []  # 车型-驱动方式关系
        args = []
        arg_dict = dict()

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'chassis_trans' in elem.keys():
                if '驱动方式' in elem['chassis_trans'].keys():
                    if elem['chassis_trans']['驱动方式'] not in chassis_trans:
                        chassis_trans.append(elem['chassis_trans']['驱动方式'])
                        for key in elem['chassis_trans'].keys():
                            if key != '驱动方式':
                                arg_dict[key] = elem['chassis_trans'][key]
                        args.append(arg_dict)
                        arg_dict = dict()

                    rels_motorcycle_chassis.append([motor, elem['chassis_trans']['驱动方式']])
        return chassis_trans, rels_motorcycle_chassis,args

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        chassis_trans, rels_motorcycle_chassis,args = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Chassis_trans', chassis_trans,args)
        print('Chassis_trans nodes have ' + str(len(chassis_trans)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        chassis_trans, rels_motorcycle_chassis ,args = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Chassis_trans', rels_motorcycle_chassis, 'ChassisTrans_is',
                                '驱动方式是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        chassis_trans, rels_motorcycle_chassis, args = self.read_nodes()
        f = open('../dict/chassis_trans.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(chassis_trans)))

        f.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = ChassisTranGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
