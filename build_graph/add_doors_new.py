#!/usr/bin/env python3
# coding: utf-8


from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class DoorsGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共1类节点
        door_num = []  # 车门个数
        seat_num = []  #座位个数
        rels_motorcycle_door = []  # 车型-车门个数关系
        rels_motorcycle_seat = []  # 车型-座位个数关系
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            #motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'car_body' in elem.keys():
                if '车门数(个)' in elem['car_body'].keys():
                    number=str(elem['car_body']['车门数(个)'])
                    rels_motorcycle_door.append([motor, number])
                    if number not in door_num:
                        door_num.append(number)
                if '座位数(个)' in elem['car_body'].keys():
                    number1=str(elem['car_body']['座位数(个)'])
                    rels_motorcycle_seat.append([motor, number1])
                    if number1 not in seat_num:
                        seat_num.append(number1)
        print(door_num)
        print(seat_num)
        return door_num,seat_num, rels_motorcycle_door,rels_motorcycle_seat

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        door_num, seat_num, rels_motorcycle_door, rels_motorcycle_seat = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('door_num', door_num)
        print('door_num nodes have ' + str(len(door_num)) + '\n')
        neo.create_node('seat_num', door_num)
        print('seat_num nodes have ' + str(len(seat_num)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        door_num, seat_num, rels_motorcycle_door, rels_motorcycle_seat = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'door_num', rels_motorcycle_door, 'door_num_is',
                                '车门个数是')
        neo.create_relationship('Motorcycle', 'seat_num', rels_motorcycle_seat, 'seat_num_is',
                                '座位个数是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        door_num, seat_num, rels_motorcycle_door, rels_motorcycle_seat = self.read_nodes()
        f = open('../dict/door_num.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f = open('../dict/seat_num.txt', 'w+', encoding='utf-8')
        f.seek(0)
        f.truncate()  # 清空文件
        f.write('\n'.join(list(door_num)))
        f.write('\n'.join(list(seat_num)))

        f.close()


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = DoorsGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
