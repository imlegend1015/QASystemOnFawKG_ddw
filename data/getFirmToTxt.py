import json
import codecs


def getfirms():
    write_file = codecs.open("../dict/firm.txt", 'a+', encoding="utf-8")
    with open("./brand_firm_series.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        firms = []
        for ele in load_dict:
            for firm in ele['on_sale_list']:
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])
            for firm in ele['halt_sale_list']:
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])
            for firm in ele['for_sale_list']:
                if firm['firm'] not in firms:
                    firms.append(firm['firm'])
        for elem in firms:
            write_file.write(str(elem) + '\n')
    write_file.close()


if __name__ == '__main__':
    getfirms()
