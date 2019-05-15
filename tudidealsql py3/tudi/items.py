# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class TudiItem(Item):
    landno = Field()
    district= Field()
    time= Field()
    province=Field()
    link=Field()
    net = Field()
    haoma=Field()
    day1=Field()
    day2=Field()
    day3 = Field()
    count= Field()
    landlocation= Field()
    landname= Field()
    landextend= Field()
    application= Field()
    area = Field()
    price = Field()
    buyer = Field()
    method = Field()
    outdistrict = Field()
    pagenum = Field()
    planting = Field()
    volumn = Field()
    initialprice = Field()
    no2 = Field()
    issuedate = Field()
    guapaiday1= Field()
    guapaiday2= Field()
    paimaiday3= Field()
    paimaiday4= Field()
    zhaobiaoday5= Field()
    zhaobiaoday6= Field()
    pagetotal = Field()
    viewstate = Field()
    eventvalidation = Field()
    tab_querysortitemlist = Field()
    tab_querysubmitorderdata = Field()
    outline  = Field()
    issuedate1 = Field()
    url = Field()
    cityname = Field()
    piece = Field()
    headline = Field()
    spare = Field()
    issuedate2 = Field()
    upheadline = Field()
    downheadline = Field()
    headno = Field()





