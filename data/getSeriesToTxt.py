import json
import codecs


def getseries():
    write_file = codecs.open("../dict/series.txt", 'a+', encoding="utf-8")
    with open("./brand_firm_series.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        series = []
        for ele in load_dict:
            for firm in ele['on_sale_list']:
                for se in firm['serieslist']:
                    if se['series_name'] not in series:
                        series.append(se['series_name'])
            for firm in ele['halt_sale_list']:
                for se in firm['serieslist']:
                    if se['series_name'] not in series:
                        series.append(se['series_name'])
            for firm in ele['for_sale_list']:
                for se in firm['serieslist']:
                    if se['series_name'] not in series:
                        series.append(se['series_name'])
    for ele in series:
        write_file.write(str(ele) + '\n')
    write_file.close()


if __name__ == '__main__':
    getseries()
