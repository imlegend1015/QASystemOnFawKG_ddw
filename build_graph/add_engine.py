#!/usr/bin/env python3
# coding: utf-8
# File: add_engine.py
# Author: hanrd
# Date: 19-03-06

from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class EngineGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
        # self.data_list_1 = MongoLoader("MotorcycleTypeItem").get_data_list()

    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共9类节点
        engine_cato = []  # 发动机类别
        engine = []  # 发动机
        output_vol = []  # 排量
        intake_form = []  # 进气形式
        cylinder_num = []  # 气缸
        cylinder_form = []  # 气缸排列方式
        admission_gear = []  # 配气机构
        oil_supply_mode = []  # 供油方式
        envir_standard = []  # 环保标准
        # material = []  # 材料

        args = list()  # 发动机属性列表
        args_dict = dict()
        engine_1 = []

        rels_motorcycle_engine_cato = []  # 车型-发动机类别关系
        rels_motorcycle_engine = []  # 车型-发动机型号关系
        rels_engine_type = []  # 发动机-发动机类别关系
        rels_engine_output = []  # 发动机-排量关系
        rels_engine_intake_form = []  # 发动机-进气形式关系
        rels_engine_cylinder_num = []  # 发动机-气缸数关系
        rels_engine_cylinder_form = []  # 发动机-气缸排列方式关系
        rels_engine_admission_gear = []  # 发动机-配气机构关系
        rels_engine_energy = []  # 发动机-燃料关系
        rels_engine_oil_supply_mode = []  # 发动机-供油方式关系
        rels_engine_envir_standard = []  # 发动机-环保标准关系

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            key_used = []
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            en_cat = ''
            if 'base_param' in elem.keys():
                if '发动机' in elem['base_param'].keys():
                    en_cat = elem['base_param']['发动机']
                    if elem['base_param']['发动机'] not in engine_cato:
                        engine_cato.append(elem['base_param']['发动机'])
                    rels_motorcycle_engine_cato.append([motor, elem['base_param']['发动机']])
            if 'engine' in elem.keys():
                ele = elem['engine']
                key_list = ele.keys()
                eng = ''
                if '发动机型号' in key_list:
                    key_used.append('发动机型号')
                    eng = ele['发动机型号']
                    rels_motorcycle_engine.append([motor, ele['发动机型号']])
                    rels_engine_type.append([ele['发动机型号'], en_cat])
                    if ele['发动机型号'] not in engine:
                        engine.append(ele['发动机型号'])
                if '排量(mL)' in key_list:
                    key_used.append('排量(mL)')
                    out = str(ele['排量(mL)']) + 'ml'
                    rels_engine_output.append([eng, out])
                    if out not in output_vol:
                        output_vol.append(out)
                if '排量(L)' in key_list:
                    key_used.append('排量(L)')
                    out = str(ele['排量(L)']) + 'L'
                    rels_engine_output.append([eng, out])
                    if out not in output_vol:
                        output_vol.append(out)
                if '进气形式' in key_list:
                    key_used.append('进气形式')
                    in_way = str(ele['进气形式'])
                    rels_engine_intake_form.append([eng, in_way])
                    if in_way not in intake_form:
                        intake_form.append(in_way)
                if '气缸数(个)' in key_list:
                    key_used.append('气缸数(个)')
                    cl_num = str(ele['气缸数(个)'])
                    rels_engine_cylinder_num.append([eng, cl_num])
                    if cl_num not in cylinder_num:
                        cylinder_num.append(cl_num)
                if '气缸排列形式' in key_list:
                    key_used.append('气缸排列形式')
                    cl_form = str(ele['气缸排列形式'])
                    rels_engine_cylinder_form.append([eng, cl_form])
                    if cl_form not in cylinder_form:
                        cylinder_form.append(cl_form)
                if '配气机构' in key_list:
                    key_used.append('配气机构')
                    org = str(ele['配气机构'])
                    rels_engine_admission_gear.append([eng, org])
                    if org not in admission_gear:
                        admission_gear.append(org)
                if '燃料形式' in key_list:
                    key_used.append('燃料形式')
                    oil = str(ele['燃料形式'])
                    rels_engine_energy.append([eng, oil])
                if '供油方式' in key_list:
                    key_used.append('供油方式')
                    way = str(ele['供油方式'])
                    rels_engine_oil_supply_mode.append([eng, way])
                    if way not in oil_supply_mode:
                        oil_supply_mode.append(way)
                if '环保标准' in key_list:
                    key_used.append('环保标准')
                    sta = str(ele['环保标准'])
                    rels_engine_envir_standard.append([eng, sta])
                    if sta not in envir_standard:
                        envir_standard.append(sta)
                if '发动机型号' in key_list:
                    eng = ele['发动机型号']
                    if eng not in engine_1:
                        engine_1.append(eng)
                        # args_dict['name'] = eng
                        for k in key_list:
                            if k not in key_used:
                                args_dict[k] = ele[k]
                        args.append(args_dict)
                        args_dict = dict()
        return engine_cato, engine, output_vol, intake_form, cylinder_num, cylinder_form, admission_gear, \
               oil_supply_mode, envir_standard, args, rels_motorcycle_engine_cato, rels_motorcycle_engine, \
               rels_engine_type, rels_engine_output, rels_engine_intake_form, rels_engine_cylinder_num, \
               rels_engine_cylinder_form, rels_engine_admission_gear, rels_engine_energy, rels_engine_oil_supply_mode, \
               rels_engine_envir_standard

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        engine_cato, engine, output_vol, intake_form, cylinder_num, cylinder_form, admission_gear, \
        oil_supply_mode, envir_standard, args, rels_motorcycle_engine_cato, rels_motorcycle_engine, \
        rels_engine_type, rels_engine_output, rels_engine_intake_form, rels_engine_cylinder_num, \
        rels_engine_cylinder_form, rels_engine_admission_gear, rels_engine_energy, rels_engine_oil_supply_mode, \
        rels_engine_envir_standard = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Engine_cato', engine_cato)
        print('Engine_cato nodes have ' + str(len(engine_cato)) + '\n')
        neo.create_node('Engine', engine, args)
        print('Engine nodes have ' + str(len(engine)) + '\n')
        neo.create_node('Output_vol', output_vol)
        print('Output_vol nodes have ' + str(len(output_vol)) + '\n')
        neo.create_node('Intake_form', intake_form)
        print('Intake_form nodes have ' + str(len(intake_form)) + '\n')
        neo.create_node('Cylinder_num', cylinder_num)
        print('Cylinder_num nodes have ' + str(len(cylinder_num)) + '\n')
        neo.create_node('Cylinder_form', cylinder_form)
        print('Cylinder_form nodes have ' + str(len(cylinder_form)) + '\n')
        neo.create_node('Admission_gear', admission_gear)
        print('Admission_gear nodes have ' + str(len(admission_gear)) + '\n')
        neo.create_node('Oil_supply_mode', oil_supply_mode)
        print('Oil_supply_mode nodes have ' + str(len(oil_supply_mode)) + '\n')
        neo.create_node('Envir_standard', envir_standard)
        print('Envir_standard nodes have ' + str(len(envir_standard)) + '\n')
        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        engine_cato, engine, output_vol, intake_form, cylinder_num, cylinder_form, admission_gear, \
        oil_supply_mode, envir_standard, args, rels_motorcycle_engine_cato, rels_motorcycle_engine, \
        rels_engine_type, rels_engine_output, rels_engine_intake_form, rels_engine_cylinder_num, \
        rels_engine_cylinder_form, rels_engine_admission_gear, rels_engine_energy, rels_engine_oil_supply_mode, \
        rels_engine_envir_standard = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Engine_cato', rels_motorcycle_engine_cato, 'engine_type_is',
                                '发动机级别是')
        neo.create_relationship('Motorcycle', 'Engine', rels_motorcycle_engine, 'engine_is',
                                '发动机是')
        neo.create_relationship('Engine', 'Engine_cato', rels_engine_type, 'is_type',
                                '发动机分类是')
        neo.create_relationship('Engine', 'Output_vol', rels_engine_output, 'output_vol_is',
                                '排量是')
        neo.create_relationship('Engine', 'Intake_form', rels_engine_intake_form, 'intake_form_is',
                                '进气方式是')
        neo.create_relationship('Engine', 'Cylinder_num', rels_engine_cylinder_num, 'cylinder_num_is',
                                '气缸数是')
        neo.create_relationship('Engine', 'Cylinder_form', rels_engine_cylinder_form, 'cylinder_form_is',
                                '气缸排列方式是')
        neo.create_relationship('Engine', 'Admission_gear', rels_engine_admission_gear, 'admiss_gear_is',
                                '配气机构是')
        neo.create_relationship('Engine', 'Energy', rels_engine_energy, 'oil_is',
                                '燃料是')
        neo.create_relationship('Engine', 'Oil_supply_mode', rels_engine_oil_supply_mode, 'oio_supply_is',
                                '供油方式是')
        neo.create_relationship('Engine', 'Envir_standard', rels_engine_envir_standard, 'envir_standard_is',
                                '环保标准是')
        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        engine_cato, engine, output_vol, intake_form, cylinder_num, cylinder_form, admission_gear, \
        oil_supply_mode, envir_standard, args, rels_motorcycle_engine_cato, rels_motorcycle_engine, \
        rels_engine_type, rels_engine_output, rels_engine_intake_form, rels_engine_cylinder_num, \
        rels_engine_cylinder_form, rels_engine_admission_gear, rels_engine_energy, rels_engine_oil_supply_mode, \
        rels_engine_envir_standard = self.read_nodes()
        f_0 = open('../dict/engine/engine_cato.txt', 'w+', encoding='utf-8')
        f_0.seek(0)
        f_0.truncate()  # 清空文件
        f_1 = open('../dict/engine/engine.txt', 'w+', encoding='utf-8')
        f_1.seek(0)
        f_1.truncate()  # 清空文件
        f_2 = open('../dict/engine/output_vol.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件
        f_3 = open('../dict/engine/intake_form.txt', 'w+', encoding='utf-8')
        f_3.seek(0)
        f_3.truncate()  # 清空文件
        f_4 = open('../dict/engine/cylinder_num.txt', 'w+', encoding='utf-8')
        f_4.seek(0)
        f_4.truncate()  # 清空文件
        f_5 = open('../dict/engine/cylinder_form.txt', 'w+', encoding='utf-8')
        f_5.seek(0)
        f_5.truncate()  # 清空文件
        f_6 = open('../dict/engine/admission_gear.txt', 'w+', encoding='utf-8')
        f_6.seek(0)
        f_6.truncate()  # 清空文件
        f_7 = open('../dict/engine/oil_supply_mode.txt', 'w+', encoding='utf-8')
        f_7.seek(0)
        f_7.truncate()  # 清空文件
        f_env_level = open('../dict/engine/envir_standard.txt', 'w+', encoding='utf-8')
        f_env_level.seek(0)
        f_env_level.truncate()  # 清空文件

        f_0.write('\n'.join(list(engine_cato)))
        f_1.write('\n'.join(list(engine)))
        f_2.write('\n'.join(list(output_vol)))
        f_3.write('\n'.join(list(intake_form)))
        f_4.write('\n'.join(list(cylinder_num)))
        f_5.write('\n'.join(list(cylinder_form)))
        f_6.write('\n'.join(list(admission_gear)))
        f_7.write('\n'.join(list(oil_supply_mode)))
        f_env_level.write('\n'.join(list(envir_standard)))

        f_0.close()
        f_1.close()
        f_2.close()
        f_3.close()
        f_4.close()
        f_5.close()
        f_6.close()
        f_7.close()
        f_env_level.close()
        print('导出数据结束')


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = EngineGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
