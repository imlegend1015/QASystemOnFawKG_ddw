#!/usr/bin/env python3
# coding: utf-8
# File: build_base_graph.py
# Author: hanrd
# Date: 19-03-05
from utils.data_loader import JsonFileLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class BaseGraph:
    def __init__(self):
        self.data_list_0 = JsonFileLoader("../data/brand_firm_series.json").get_data_list()
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        self.data_list_2 = JsonFileLoader("../data/brand_website.json").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共8类节点
        brands = []  # 品牌
        brand_websites = []  # 厂商官网
        firms = []  # 厂商
        series = []  # 车系
        car_levels = []  # 车辆级别（如： SUV、轿车等）
        motorcycles = []  # 车型
        energy = []  # 能源类别
        sale_level = ['在售', '停售', '未售']  # 在售|停售|未售

        car_infos = []  # 车型信息

        # 构建节点实体关系
        rels_brd_website = []  # 品牌-官网关系
        rels_brd_firm = []  # 品牌-厂商关系
        rels_brd_series = []  # 品牌-车系关系
        rels_firm_series = []  # 厂商-车系关系
        rels_series_salelevel = []  # 车系-销售级别
        rels_series_carlevel = []  # 车系-级别关系
        rels_firm_motortype = []  # 厂商-车型关系
        rels_series_motortype = []  # 车系-车型关系
        rels_motortype_energy = []  # 车型-能源关系
        rels_motortype_salelevel = []  # 车型-销售级别关系
        rels_motortype_carlevel = []  # 车型-级别关系

        data_list = self.data_list_0
        print('读入brand_firm_series信息条目：' + str(len(data_list)) + '\n')
        for elem in data_list:
            brand_name = elem['brand_name']
            brand_id = elem['brand_id']
            brands.append(str(brand_id) + '#' + str(brand_name))  # 品牌

            for firm in elem['on_sale_list']:  # 在售
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])  # 厂商
                    for se in firm['serieslist']:
                        rels_firm_series.append([firm['firm'], se['series_name']])  # 厂商-车系关系
                    rels_brd_firm.append([brand_name, firm['firm']])  # 品牌-厂商关系
                for se in firm['serieslist']:
                    series_id = se['series_id']
                    series_price = se['price']
                    seri = str(series_id) + '#' + str(se['series_name']) + '#' + str(series_price)
                    if seri not in series:
                        series.append(seri)  # 车系
                        rels_series_salelevel.append([se['series_name'], sale_level[0]])  # 车系-销售级别关系
                        rels_brd_series.append([brand_name, se['series_name']])  # 品牌-车系关系
                        rels_series_carlevel.append([se['series_name'], se['level_name']])  # 车系-级别关系
                    level_id = se['level_id']
                    car_lev = str(level_id) + '#' + str(se['level_name'])
                    if car_lev not in car_levels:
                        car_levels.append(car_lev)  # 级别
            for firm in elem['halt_sale_list']:  # 停售
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])  # 厂商
                    for se in firm['serieslist']:
                        rels_firm_series.append([firm['firm'], se['series_name']])  # 厂商-车系关系
                    rels_brd_firm.append([brand_name, firm['firm']])  # 品牌-厂商关系
                for se in firm['serieslist']:
                    series_id = se['series_id']
                    series_price = se['price']
                    seri = str(series_id) + '#' + str(se['series_name']) + '#' + str(series_price)
                    if seri not in series:
                        series.append(seri)  # 车系
                        rels_series_salelevel.append([se['series_name'], sale_level[1]])  # 车系-销售级别关系
                        rels_brd_series.append([brand_name, se['series_name']])  # 品牌-车系关系
                        rels_series_carlevel.append([se['series_name'], se['level_name']])  # 车系-级别关系
                    level_id = se['level_id']
                    car_lev = str(level_id) + '#' + str(se['level_name'])
                    if car_lev not in car_levels:
                        car_levels.append(car_lev)  # 级别
            for firm in elem['for_sale_list']:  # 未售
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])  # 厂商
                    for se in firm['serieslist']:
                        rels_firm_series.append([firm['firm'], se['series_name']])  # 厂商-车系关系
                    rels_brd_firm.append([brand_name, firm['firm']])  # 品牌-厂商关系
                for se in firm['serieslist']:
                    series_id = se['series_id']
                    series_price = se['price']
                    seri = str(series_id) + '#' + str(se['series_name']) + '#' + str(series_price)
                    if seri not in series:
                        series.append(seri)  # 车系
                        rels_series_salelevel.append([se['series_name'], sale_level[2]])  # 车系-销售级别关系
                        rels_brd_series.append([brand_name, se['series_name']])  # 品牌-车系关系
                        rels_series_carlevel.append([se['series_name'], se['level_name']])  # 车系-级别关系
                    level_id = se['level_id']
                    car_lev = str(level_id) + '#' + str(se['level_name'])
                    if car_lev not in car_levels:
                        car_levels.append(car_lev)  # 级别

        data_list_1 = self.data_list_1
        print('读入motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            car_infos.append(elem)
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            motor_id = elem['motorcycle_type_id']
            mot = str(motor_id) + '#' + str(motor)
            if mot not in motorcycles:
                motorcycles.append(mot)  # 车型
            rels_series_motortype.append([elem['series_name'], motor])  # 车系-车型关系
            rels_motortype_salelevel.append([motor, elem['on_sale']])  # 车型-销售级别关系
            rels_motortype_carlevel.append([motor, elem['level_name']])  # 车型-级别关系
            if "base_param" in elem.keys():
                if "能源类型" in elem['base_param'].keys():
                    en = elem['base_param']['能源类型']
                    if en is not "" and en not in energy:  # and en is not "-"
                        energy.append(en)
                    rels_motortype_energy.append([motor, en])  # 车型-能源类型关系
                if "厂商" in elem['base_param'].keys():
                    fr = elem['base_param']['厂商']
                    if fr is not "-":
                        rels_firm_motortype.append([fr, motor])  # 厂商-车型关系

        data_list_2 = self.data_list_2
        print('读入brand_website信息条目：' + str(len(data_list_2)) + '\n')
        for elem in data_list_2:
            website = elem['off_web']
            if website != '' and website not in brand_websites:
                brand_websites.append(website)
                rels_brd_website.append([elem['brand_name'], website])

        print("读入信息完毕\n")
        return brands, brand_websites, firms, series, car_levels, motorcycles, energy, sale_level, car_infos, \
               rels_brd_website, rels_brd_firm, rels_brd_series, rels_firm_series, rels_series_salelevel, \
               rels_series_carlevel, rels_firm_motortype, rels_series_motortype, rels_motortype_energy, \
               rels_motortype_salelevel, rels_motortype_carlevel

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        brands, brand_websites, firms, series, car_levels, motorcycles, energy, sale_level, car_infos, rels_brd_website\
            , rels_brd_firm, rels_brd_series, rels_firm_series, rels_series_salelevel, rels_series_carlevel, \
        rels_firm_motortype, rels_series_motortype, rels_motortype_energy, rels_motortype_salelevel, \
        rels_motortype_carlevel = self.read_nodes()
        neo = Neo4jOp()
        print('开始创建车型节点\n')
        neo.create_motorcycle_nodes(car_infos)
        print('车型节点创建完毕\n')
        neo.create_node('Brand', brands)
        print('Brand nodes have ' + str(len(brands)) + '\n')
        neo.create_node('Brand_website', brand_websites)
        print('Brand_website nodes have ' + str(len(brand_websites)) + '\n')
        neo.create_node('Firm', firms)
        print('Firm nodes have ' + str(len(firms)) + '\n')
        neo.create_node('Series', series)
        print('Series nodes have ' + str(len(series)) + '\n')
        neo.create_node('Car_level', car_levels)
        print('Car_level nodes have ' + str(len(car_levels)) + '\n')
        neo.create_node('Energy', energy)
        print('Energy nodes have ' + str(len(energy)) + '\n')
        neo.create_node('Sale_level', sale_level)
        print('Sale_level nodes have ' + str(len(sale_level)) + '\n')
        print('节点类型创建完毕')
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        print('开始创建关系')
        brands, brand_websites, firms, series, car_levels, motorcycles, energy, sale_level, car_infos, rels_brd_website\
            , rels_brd_firm, rels_brd_series, rels_firm_series, rels_series_salelevel, rels_series_carlevel, \
        rels_firm_motortype, rels_series_motortype, rels_motortype_energy, rels_motortype_salelevel, \
        rels_motortype_carlevel = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Brand', 'Brand_website', rels_brd_website, 'website_is', '品牌官网是')
        neo.create_relationship('Brand', 'Firm', rels_brd_firm, 'belongs_to', '隶属于')
        neo.create_relationship('Brand', 'Series', rels_brd_series, 'include_series', '包含车系')
        neo.create_relationship('Firm', 'Series', rels_firm_series, 'produce_series', '生产车系')
        neo.create_relationship('Series', 'Sale_level', rels_series_salelevel, 'series_sale_level', '销售级别')
        neo.create_relationship('Series', 'Car_level', rels_series_carlevel, 'series_level_is', '车系级别')
        neo.create_relationship('Firm', 'Motorcycle', rels_firm_motortype, 'sales', '出售')
        neo.create_relationship('Series', 'Motorcycle', rels_series_motortype, 'include_motor', '包含车型')
        neo.create_relationship('Motorcycle', 'Energy', rels_motortype_energy, 'energy_type_is', '能源类型是')
        neo.create_relationship('Motorcycle', 'Sale_level', rels_motortype_salelevel, 'car_sale_level', '销售级别')
        neo.create_relationship('Motorcycle', 'Car_level', rels_motortype_carlevel, 'car_level_is', '车型级别是')
        print('关系创建完毕')

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        brands, brand_websites, firms, series, car_levels, motorcycles, energy, sale_level, car_infos, rels_brd_website\
            , rels_brd_firm, rels_brd_series, rels_firm_series, rels_series_salelevel, rels_series_carlevel, \
        rels_firm_motortype, rels_series_motortype, rels_motortype_energy, rels_motortype_salelevel, \
        rels_motortype_carlevel = self.read_nodes()
        f_brand = open('../dict/base_info/brand.txt', 'w+', encoding='utf-8')
        f_brand.seek(0)
        f_brand.truncate()  # 清空文件
        f_website = open('../dict/base_info/website.txt', 'w+', encoding='utf-8')
        f_website.seek(0)
        f_website.truncate()  # 清空文件
        f_firm = open('../dict/base_info/firm.txt', 'w+', encoding='utf-8')
        f_firm.seek(0)
        f_firm.truncate()  # 清空文件
        f_series = open('../dict/base_info/series.txt', 'w+', encoding='utf-8')
        f_series.seek(0)
        f_series.truncate()  # 清空文件
        f_car_level = open('../dict/base_info/car_level.txt', 'w+', encoding='utf-8')
        f_car_level.seek(0)
        f_car_level.truncate()  # 清空文件
        f_motorcycle = open('../dict/base_info/motorcycle.txt', 'w+', encoding='utf-8')
        f_motorcycle.seek(0)
        f_motorcycle.truncate()  # 清空文件
        f_energy = open('../dict/base_info/energy.txt', 'w+', encoding='utf-8')
        f_energy.seek(0)
        f_energy.truncate()  # 清空文件
        f_sale_level = open('../dict/base_info/sale_level.txt', 'w+', encoding='utf-8')
        f_sale_level.seek(0)
        f_sale_level.truncate()  # 清空文件

        f_brand.write('\n'.join(list(brands)))
        f_website.write('\n'.join(list(brand_websites)))
        f_firm.write('\n'.join(list(firms)))
        f_series.write('\n'.join(list(series)))
        f_car_level.write('\n'.join(list(car_levels)))
        f_motorcycle.write('\n'.join(list(motorcycles)))
        f_energy.write('\n'.join(list(energy)))
        f_sale_level.write('\n'.join(list(sale_level)))

        f_brand.close()
        f_website.close()
        f_firm.close()
        f_series.close()
        f_car_level.close()
        f_motorcycle.close()
        f_energy.close()
        f_sale_level.close()
        print('导出数据结束')


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = BaseGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
