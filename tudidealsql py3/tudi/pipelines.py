# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import json
# import codecs
#
#
# class TudiPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('data.json', mode='wb', encoding='utf-8')#数据存储到data.json
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item),ensure_ascii=False) + "\n"
#         self.file.write(line)
#
#         return item


import json
import codecs
import time
import uuid
from twisted.enterprise import adbapi
import pymssql
class TudiPipeline(object):
    # 数据库参数
    def open_spider(self, spider):
        self.db = pymssql.connect(
            server='172.16.9.80',
            database='YuanChao',
            charset='utf8'
        )

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        sql1 = "insert into 土地成交PQ准备表(id,页数,序号,土地宗数,外页标题,外页行政区,外页发布时间,网址,地块编号,城市,内页省份,内页区县,内页标题上,内页出让方式,地块名称,土地位置,土地四至,详细规划,建设用地面积,起始时间,截止时间,成交时间,交易状况,受让单位,成交价,备注,更新日期,内页发布日期,内页标题下,标题地块编号) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql1, (uuid.uuid1() , item['pagenum'] ,	item['haoma'] ,	item['piece'] ,	item['outline'] ,	item['outdistrict'] , item['issuedate1']  ,item['url'] ,
                              	item['landno'] ,	item['cityname'] ,item['province'] ,item['district']  ,item['upheadline'] ,item['method'],item['landname'] ,item['landlocation'] ,item['landextend']  ,
                              item['application'] ,item['area'] ,item['day1'] ,item['day2'],item['day3'],'已成交' ,item['buyer']  ,item['price']  ,item['spare'] , time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),item['issuedate2'] , item['downheadline']  , item['headno'] ))

        self.db.commit()
        return item
