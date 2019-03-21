#!/usr/bin/env python3
# coding: utf-8
# File: add_chassis_trans.py
# Author: Wangny
# Date: 19-03-10

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class AssistOperateGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点

        front_rear_parking_radar = []  #前后驻车雷达
        driving_assistance_image = [] #驾驶辅助影像
        driving_mode = []  #驾驶模式切换

        rels_motorcycle_parking_radar = []
        rels_motorcycle_driving_assistance = []
        rels_motorcycle_driving_mode = []

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'assist_operate' in elem.keys():
                if '前/后驻车雷达' in elem['assist_operate'].keys():
                    temp_str1 = ''.join(elem['assist_operate']['前/后驻车雷达'])
                    if temp_str1 not in front_rear_parking_radar:
                        front_rear_parking_radar.append(temp_str1)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_parking_radar.append([motor, temp_str1])
                if '驾驶辅助影像' in elem['assist_operate'].keys():
                    temp_str2 = ''.join(elem['assist_operate']['驾驶辅助影像'])
                    if temp_str2 not in driving_assistance_image:
                        driving_assistance_image.append(temp_str2)
                    #temp_str2 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_driving_assistance.append([motor, temp_str2])
                if '驾驶模式切换' in elem['assist_operate'].keys():
                    temp_str3 = ''.join(elem['assist_operate']['驾驶模式切换'])
                    if temp_str3 not in driving_mode:
                        driving_mode.append(temp_str3)
                    #temp_str3 = ''.join(elem['fridge_air_conditioner']['空调温度控制方式'])
                    rels_motorcycle_driving_mode.append([motor, temp_str3])
        return front_rear_parking_radar,driving_assistance_image,driving_mode,rels_motorcycle_parking_radar,rels_motorcycle_driving_assistance,rels_motorcycle_driving_mode



    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        front_rear_parking_radar, driving_assistance_image, driving_mode, rels_motorcycle_parking_radar, rels_motorcycle_driving_assistance, rels_motorcycle_driving_mode = self.read_nodes()

        neo = Neo4jOp()
        neo.create_node('Front_rear_parking_radar', front_rear_parking_radar)
        print('Front_rear_parking_radar nodes have ' + str(len(front_rear_parking_radar)) + '\n')
        neo.create_node('Driving_assistance_image',driving_assistance_image)
        print('Driving_assistance_image nodes have ' + str(len(driving_assistance_image)) + '\n')
        neo.create_node('Driving_mode', driving_mode)
        print('Driving_mode nodes have ' + str(len(driving_mode)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        front_rear_parking_radar, driving_assistance_image, driving_mode, rels_motorcycle_parking_radar, rels_motorcycle_driving_assistance, rels_motorcycle_driving_mode = self.read_nodes()

        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Front_rear_parking_radar', rels_motorcycle_parking_radar, 'Front_rear_parking_radar_is',
                                '前后驻车雷达是')
        neo.create_relationship('Motorcycle', 'Driving_assistance_image', rels_motorcycle_driving_assistance, 'Driving_assistance_image_is',
                                '驾驶辅助影像是')
        neo.create_relationship('Motorcycle', 'Driving_mode', rels_motorcycle_driving_mode,
                                'Driving_mode_is',
                                '驾驶模式切换是')


        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        front_rear_parking_radar, driving_assistance_image, driving_mode, rels_motorcycle_parking_radar, rels_motorcycle_driving_assistance, rels_motorcycle_driving_mode = self.read_nodes()

        f_1 = open('../dict/front_rear_parking_radar.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_1.write('\n'.join(list(front_rear_parking_radar)))
        f_1.close()

        f_2 = open('../dict/driving_assistance_image.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_2.write('\n'.join(list(driving_assistance_image)))
        f_2.close()

        f_3 = open('../dict/driving_mode.txt', 'w+', encoding='utf-8')
        f_3.seek(0)
        f_3.truncate()  # 清空文件
        f_3.write('\n'.join(list(driving_mode)))
        f_3.close()




if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = AssistOperateGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
