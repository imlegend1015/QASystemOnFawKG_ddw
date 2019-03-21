from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys

class CarBodyGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()
    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共3类节点
        '''
        carbody_cato = []  #车身类别
        doornum=[]#车身的门的个数
        seatnum=[]#车座位的个数
        rels_motorcycle_carbody_cato = []  # 车型-车身类别关系
        rels_carbody_doornum = []  # 车身-门数关系
        rels_carbody_seatnum = []  # 车身-座位数关系

        args = []# 车身carbody属性列表
        arg_dict = dict()
        carbody_1 = []
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            key_used = []
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            en_cat = ''
            if 'base_param' in elem.keys():
                if '长*宽*高(mm)' in elem['base_param'].keys():
                    en_cat = elem['base_param']['长*宽*高(mm)']
                    if elem['base_param']['长*宽*高(mm)'] not in carbody_cato:
                        carbody_cato.append(elem['base_param']['长*宽*高(mm)'])
                    rels_motorcycle_carbody_cato.append([motor, elem['base_param']['长*宽*高(mm)']])
            if 'car_body' in elem.keys():
                ele = elem['car_body']
                key_list = ele.keys()
                eng = ''
                if '车门数(个)' in key_list:
                    key_used.append('车门数(个)')
                    doornum1 = str(ele['车门数(个)'])
                    rels_carbody_doornum.append([eng, doornum1])
                    if doornum1 not in doornum:
                        doornum.append(doornum1)

                if '座位数(个)' in key_list:
                    key_used.append('座位数(个)')
                    seatnum1  = str(ele['座位数(个)'])
                    rels_carbody_seatnum.append([eng, seatnum1])
                    if seatnum1 not in seatnum:
                        seatnum.append(seatnum1)
        
        '''
        carbody_cato = []  # 车身类别

        rels_motorcycle_carbody_cato = []  # 车型-车身类别关系



        args = []  # 车身carbody属性列表
        arg_dict = dict()
        carbody_1 = []
        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            key_used = []
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            en_cat = ''
            if 'base_param' in elem.keys():
                if '长*宽*高(mm)' in elem['base_param'].keys():
                    en_cat = elem['base_param']['长*宽*高(mm)']
                    if elem['base_param']['长*宽*高(mm)'] not in carbody_cato:
                        carbody_cato.append(elem['base_param']['长*宽*高(mm)'])
                    rels_motorcycle_carbody_cato.append([motor, elem['base_param']['长*宽*高(mm)']])

            '''
            if 'car_body' in elem.keys():
                if '车门数(个)' in elem['car_body'].keys():
                    if elem['car_body']['车门数（个）'] not in doornum:
                        doornum.append(elem['car_body']['车门数（个）'])

                    rels_carbody_doornum.append([motor, elem['car_body']['车门数（个）']])
            '''


        return carbody_cato,args,rels_motorcycle_carbody_cato

    def create_graph_carbody_cato_nodes(self):
        print('开始创建实体类型节点\n')
        carbody_cato, args, rels_motorcycle_carbody_cato = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Carbody_cato',carbody_cato)
        print('Carbody_cato nodes have ' + str(len(carbody_cato)) + '\n')

        print('节点类型创建完毕')
        return



    def create_graph_carbody_cato_rels(self):
        print('开始创建')
        carbody_cato, args, rels_motorcycle_carbody_cato = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Carbody_cato',rels_motorcycle_carbody_cato, 'car_body_is',
                                '车身分类是')

        print('关系创建完毕')
        return




    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        carbody_cato, args, rels_motorcycle_carbody_cato = self.read_nodes()


        f_2 = open('../dict/car_body/carbody_cato.txt', 'w+', encoding='utf-8')
        f_2.seek(0)
        f_2.truncate()  # 清空文件




        f_2.write('\n'.join(list(carbody_cato)))



        f_2.close()
        print("导出结束")


if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler = CarBodyGraph()
    handler.create_graph_carbody_cato_nodes()
    handler.create_graph_carbody_cato_rels()
    handler.export_data()
