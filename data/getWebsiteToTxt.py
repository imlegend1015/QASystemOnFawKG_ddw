# coding:utf-8
# 获取品牌官网构成的文件

import json
import codecs


def getwebsite():
    write_file = codecs.open("../dict/website.txt", 'a+', encoding="utf-8")
    with open("./brand_website.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        for ele in load_dict:
            brand = ele['off_web']
            if brand != '':
                write_file.write(brand + '\n')
    write_file.close()


if __name__ == '__main__':
    getwebsite()
