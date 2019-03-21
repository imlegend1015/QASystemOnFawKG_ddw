# coding:utf-8
# 获取品牌名构成的文件

import json
import codecs


def getbrand():
    write_file = codecs.open("../dict/brand.txt", 'a+', encoding="utf-8")
    with open("./brand_firm_series.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        for ele in load_dict:
            brand = ele['brand_name']
            write_file.write(brand + '\n')
    write_file.close()


if __name__ == '__main__':
    getbrand()
