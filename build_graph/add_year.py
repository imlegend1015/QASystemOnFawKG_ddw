from utils.data_loader import JsonFileLoader, MongoLoader
from utils.neo4j_op import Neo4jOp
from utils import logger
import sys


class YearGraph:
    def __init__(self):
        self.data_list_1 = JsonFileLoader("../data/motorcycle.json").get_data_list()


    """读取文件"""
    def read_nodes(self):
        print('开始读入数据\n')
        # 共2类节点
        year = []  # 车门个数

        rels_motorcycle_year = []  # 车型-年份关系

        data_list_1 = self.data_list_1
        print('motorcycle信息条目：' + str(len(data_list_1)) + '\n')
        for elem in data_list_1:
            motor = elem['series_name'] + ' ' + elem['motorcycle_type_name']
            if 'base_param' in elem.keys():
                if '上市时间' in elem['base_param'].keys():
                    year1=str(elem['base_param']['上市时间'])
                    rels_motorcycle_year.append([motor, year1[0:4]])
                    if year1[0:4] not in year:
                        year.append(year1[0:4])
        print(year)

        return year, rels_motorcycle_year

    def create_graphnodes(self):
        print('开始创建实体类型节点\n')
        year, rels_motorcycle_year = self.read_nodes()
        neo = Neo4jOp()
        neo.create_node('Year', year)
        print('Year nodes have ' + str(len(year)) + '\n')

        print('节点类型创建完毕')
        return

    def create_graphrels(self):
        print('开始创建')
        year, rels_motorcycle_year = self.read_nodes()
        neo = Neo4jOp()
        neo.create_relationship('Motorcycle', 'Year', rels_motorcycle_year, 'onlyyear_is',
                                '年份是')

        print('关系创建完毕')
        return

    '''导出数据'''
    def export_data(self):
        print('开始导出数据')
        year, rels_motorcycle_year = self.read_nodes()

        f0 = open('../dict/year.txt', 'w+', encoding='utf-8')
        f0.seek(0)
        f0.truncate()  # 清空文件
        f0.write('\n'.join(list(year)))

        f0.close()



if __name__ == '__main__':
    sys.stdout = logger.Logger()
    handler =YearGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()