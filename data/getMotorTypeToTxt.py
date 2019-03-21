# coding:utf-8
import json
import codecs


def getmotorcycle():
    write_file = codecs.open("../dict/motorcycle.txt", 'a+', encoding="utf-8")
    with open("./motorcycle.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        print(len(load_dict))
        motor_type = []
        for ele in load_dict:
            # print(ele['brand_name'], ele['series_name'], ele['motorcycle_type_name'])
            motor = ele['series_name'] + ' ' + ele['motorcycle_type_name']
            if motor not in motor_type:
                motor_type.append(motor)
    for ele in motor_type:
        write_file.write(str(ele) + '\n')
    write_file.close()


if __name__ == '__main__':
    getmotorcycle()
