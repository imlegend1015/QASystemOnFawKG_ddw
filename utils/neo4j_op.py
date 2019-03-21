# coding: utf-8
# File: neo4j_op.py
# Author: hanrd
# Date: 19-03-05
from py2neo import Graph, Node


class Neo4jOp:

    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="951015")

    def create_node(self, label, nodes, args=None):
        count = 0
        if args is None:
            for node_name in nodes:
                if node_name.find('#') == -1:  # 没有id
                    node = Node(label, name=node_name)
                    self.g.create(node)
                    count += 1
                    if count % 100 == 0:
                        print('create '+label+' node '+str(count)+' of '+str(len(nodes)))
                else:
                    rs = node_name.split('#')
                    if len(rs) == 2:  # 有id没有price
                        _id = rs[0]
                        name = rs[1]
                        node = Node(label, name=name, id=_id)
                        self.g.create(node)
                        count += 1
                        if count % 100 == 0:
                            print('create ' + label + ' node ' + str(count) + ' of ' + str(len(nodes)))
                    elif len(rs) == 3:  # 有id有price
                        _id = rs[0]
                        name = rs[1]
                        price = rs[2]
                        node = Node(label, name=name, id=_id, price=price)
                        self.g.create(node)
                        count += 1
                        if count % 100 == 0:
                            print('create ' + label + ' node ' + str(count) + ' of ' + str(len(nodes)))
        else:
            index = 0
            for node_name in nodes:
                if node_name.find('#') == -1:  # 没有id
                    args[index]['name'] = node_name
                    node = Node(label, **args[index])
                    self.g.create(node)
                    index += 1
                    count += 1
                    if count % 100 == 0:
                        print('create ' + label + ' node ' + str(count) + ' of ' + str(len(nodes)))
        return

    def get_args(self, car_dict):
        args = dict()
        # spe_keys = ["base_param", "car_body", "engine", "gear_box", "chassis_trans", "wheel_brake", "safe_device",
        #             "assist_operate", "guard_theft_device", "inner_config", "seat_config", "multi_media", "lighting",
        #             "mirror", "fridge_air_conditioner", "select_bag", "electromotor"]
        args['name'] = car_dict['series_name'] + ' ' + car_dict['motorcycle_type_name']
        args['series_tags'] = car_dict['series_tags']
        args['category'] = car_dict['category']
        args['motorcycle_type_id'] = car_dict['motorcycle_type_id']
        args['recom_price'] = car_dict['recom_price']
        args['description'] = car_dict['description']


        return args

    """创建知识图谱中心车型的节点"""
    def create_motorcycle_nodes(self, car_infos):
        count = 0
        for car_dict in car_infos:
            args = self.get_args(car_dict)
            node = Node("Motorcycle", **args)
            self.g.create(node)
            count += 1
            if count % 100 == 0:
                print("正在创建第%d个车型节点" % count)
        print("车型节点数目：" + str(count))
        return

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all_num = len(set(set_edges))
        print('关系数目是'+str(all_num))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                if count % 100 == 0:
                    print('正在创建关系'+str(rel_type)+': '+str(count) + ' of ' + str(all_num))
            except Exception as e:
                print(e)
        return
