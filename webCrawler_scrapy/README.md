```
./item : 存放item类
./lib : 存放工具类
./logs : 存放log日志
```

# auto_home_brand_firm_series.py：
爬取品牌、厂商、车系

# auto_home_motorcycle_types.py:
爬取车型及配置信息

# auto_home_users.py:
爬取用户信息

# 运行
## 准备：更改数据库配置信息
```
1.进入项目根目录
```
```
2.scrapy crawl 爬虫名
   爬虫有以下三个：brands_firms_series、motorcycle、users
```
```
3.爬取数据自动存放在mongodb中，若想输出到json文件：
  scrapy crawl 爬虫名 -o 文件名.json
```