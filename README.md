#Author：wangny

本项目为基于知识图谱的智能问答系统

目前所作工作为知识图谱的数据层部分

已有数据为爬取得一万两千多条从汽车之家爬取的汽车配置信息







```
./build_graph: 存放KG构建代码
./data: 存放数据
./dict: 存放每类实体的txt
./log: 终端输出
./utils: 工具
./webCrawler_scrapy: 爬取汽车之家app
```

## 运行：
``` bash
cd build_graph
```
```
python build_base_graph.py

(终端输出的提示信息，同时也会保存在./log/log.txt中)
```
