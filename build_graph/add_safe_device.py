#!/usr/bin/env python3
# coding: utf-8


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

        child_seat = []  # 儿童座椅
        anti_lock = []  # ABS防抱死
        brake_power = []  # 制动力分配（EBD/CBC等）
        brake_assist = []  # 刹车辅助(EBA/BAS/BA等）
        traction_control = []  # 牵引力控制(ASR/TCS/TRC等)
        body_stability_control = []  # 车身稳定控制(ESC/ESP/DSC等)

        rels_motorcycle_child_seat = []  # 车型-儿童座椅关系
        rels_motorcycle_anti_lock = []  # 车型-ABS防抱死关系
        rels_motorcycle_brake_power = []  # 车型-制动力分配关系
        rels_motorcycle_brake_assist = []  # 车型-刹车辅助关系
        rels_motorcycle_traction_control = []  # 车型-牵引力控制关系
        rels_motorcycle_body_stability_control = []  # 车型-车身稳定控制关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'safe_device' in elem.keys():
                if 'ISOFIX儿童座椅接口' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['ISOFIX儿童座椅接口'])
                    if temp_str1 not in child_seat:
                        child_seat.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['ISOFIX儿童座椅接口'])
                    rels_motorcycle_child_seat.append([motor, temp_str2])
                if 'ABS防抱死' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['ABS防抱死'])
                    if temp_str1 not in anti_lock:
                        anti_lock.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['ABS防抱死'])
                    rels_motorcycle_anti_lock.append([motor, temp_str2])
                if '制动力分配(EBD/CBC等)' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['制动力分配(EBD/CBC等)'])
                    if temp_str1 not in brake_power:
                        brake_power.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['制动力分配(EBD/CBC等)'])
                    rels_motorcycle_brake_power.append([motor, temp_str2])
                if '刹车辅助(EBA/BAS/BA等)' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['刹车辅助(EBA/BAS/BA等)'])
                    if temp_str1 not in brake_assist:
                        brake_assist.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['刹车辅助(EBA/BAS/BA等)'])
                    rels_motorcycle_brake_assist.append([motor, temp_str2])
                if '牵引力控制(ASR/TCS/TRC等)' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['牵引力控制(ASR/TCS/TRC等)'])
                    if temp_str1 not in traction_control:
                        traction_control.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['牵引力控制(ASR/TCS/TRC等)'])
                    rels_motorcycle_traction_control.append([motor, temp_str2])
                if '车身稳定控制(ESC/ESP/DSC等)' in elem['safe_device'].keys():
                    temp_str1 = ''.join(elem['safe_device']['车身稳定控制(ESC/ESP/DSC等)'])
                    if temp_str1 not in body_stability_control:
                        body_stability_control.append(temp_str1)
                    temp_str2 = ''.join(elem['safe_device']['车身稳定控制(ESC/ESP/DSC等)'])
                    rels_motorcycle_body_stability_control.append([motor, temp_str2])

        return child_seat,anti_lock,brake_power,brake_assist,traction_control,body_stability_control, rels_motorcycle_child_seat,rels_motorcycle_anti_lock,rels_motorcycle_brake_power,rels_motorcycle_brake_assist,rels_motorcycle_traction_control,rels_motorcycle_body_stability_control

        #return auto_lights,rels_motorcycle_auto_light

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')

        child_seat,anti_lock, brake_power, brake_assist, traction_control, body_stability_control, rels_motorcycle_child_seat,rels_motorcycle_anti_lock, rels_motorcycle_brake_power, rels_motorcycle_brake_assist, rels_motorcycle_traction_control, rels_motorcycle_body_stability_control = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('child_seat', child_seat)
        neo.create_node('anti_lock', anti_lock)
        neo.create_node('brake_power', brake_power)
        neo.create_node('brake_assist', brake_assist)
        neo.create_node('traction_control', traction_control)
        neo.create_node('body_stability_control', body_stability_control)
        print('child_seat nodes have ' + str(len(child_seat)) + '\n')
        print('anti_lock nodes have ' + str(len(anti_lock)) + '\n')
        print('brake_power nodes have ' + str(len(brake_power)) + '\n')
        print('brake_assist nodes have ' + str(len(brake_assist)) + '\n')
        print('traction_control nodes have ' + str(len(traction_control)) + '\n')
        print('body_stability_control nodes have ' + str(len(body_stability_control)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')

        child_seat,anti_lock, brake_power, brake_assist, traction_control, body_stability_control, rels_motorcycle_child_seat,rels_motorcycle_anti_lock, rels_motorcycle_brake_power, rels_motorcycle_brake_assist, rels_motorcycle_traction_control, rels_motorcycle_body_stability_control = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'child_seat', rels_motorcycle_child_seat, 'child_seat_is',
                                'ISOFIX儿童座椅接口是')
        neo.create_relationship('Motorcycle', 'anti_lock', rels_motorcycle_anti_lock,'anti_lock_is',
                                'ABS防抱死是)')
        neo.create_relationship('Motorcycle', 'brake_power', rels_motorcycle_brake_power, 'brake_power_is',
                                '制动力分配（EBD/CBC等）是')
        neo.create_relationship('Motorcycle', 'brake_assist', rels_motorcycle_brake_assist, 'brake_assist_is',
                                '刹车辅助(EBA/BAS/BA等)是')
        neo.create_relationship('Motorcycle', 'traction_control', rels_motorcycle_traction_control, 'traction_control_is',
                                '牵引力控制(ASR/TCS/TRC等)是')
        neo.create_relationship('Motorcycle', 'body_stability_control', rels_motorcycle_body_stability_control,'body_stability_control_is',
                                '车身稳定控制(ESC/ESP/DSC等)是')

        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')

        child_seat,anti_lock, brake_power, brake_assist, traction_control, body_stability_control, rels_motorcycle_child_seat, rels_motorcycle_anti_lock,rels_motorcycle_brake_power, rels_motorcycle_brake_assist, rels_motorcycle_traction_control, rels_motorcycle_body_stability_control = self.read_nodes()
        f = open('../dict/child_seat.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(child_seat)))
        f = open('../dict/anti_lock.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(anti_lock)))
        f = open('../dict/brake_power.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(brake_power)))
        f = open('../dict/brake_assit.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(brake_assist)))
        f = open('../dict/traction_control.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(traction_control)))
        f = open('../dict/body_stability_control.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(body_stability_control)))


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = LightingGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
