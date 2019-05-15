# import sys
# sys.path.append('..')
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy.http import FormRequest
import urllib.parse
import scrapy
from tudi.items import TudiItem
import datetime ,time,re




class ListSpider(CrawlSpider):
    # 爬虫名称
    name = "tudideal"
    
    # 允许域名
    allowed_domains = ["landchina.com"]
    start_urls = ['http://www.landchina.com/default.aspx?tabid=262&ComName=default'
    ]
    def parse(self, response):
            item = TudiItem()
            # page=response.selector.xpath('//td[@class="pager"]/text()')[0].extract()
            # count = page[page.find("共".decode('utf-8')) +1 :page.find("页".decode('utf-8'))]
            viewstate = response.selector.xpath('//div[@class="aspNetHidden"]/input[@id="__VIEWSTATE"]/@value').extract_first()  #不知道为什么用[0].extract()会报错
            item['viewstate'] = viewstate
            eventvalidation=  response.selector.xpath('//div[@class="aspNetHidden"]/input[@id="__EVENTVALIDATION"]/@value').extract_first()
            item['eventvalidation'] = eventvalidation
            tab_querysortitemlist =  response.selector.xpath('//div[@class="tagOrderBody"]/table/tbody/tr/td/span/input[@id="TAB_QuerySort0"]/@value')[0].extract()
            item['tab_querysortitemlist'] = tab_querysortitemlist
            tab_querysubmitorderdata= response.selector.xpath('//td[@id="mainModuleContainer_478_1112_1536_tdExtendProContainer"]//input[@id="TAB_QuerySubmitOrderData"]/@value')[0].extract()
            item['tab_querysubmitorderdata'] = tab_querysubmitorderdata
           # for i in range(1, int(count) + 1):
            yield FormRequest(url="http://www.landchina.com/default.aspx?tabid=262&ComName=default",
                          formdata={'TAB_QuerySubmitPagerData': '0',
                                    'hidComName': 'default',
                                    '__VIEWSTATE': viewstate,
                                    '__EVENTVALIDATION': eventvalidation,
                                    'TAB_QuerySortItemList': tab_querysortitemlist,
                                    'TAB_QuerySubmitConditionData': urllib.parse.unquote_to_bytes("66cc8979-1a1d-4fd5-b22a-0aeb1e14c6fd%3A2%A8%88%7E%D5%D0%C5%C4%B9%D2%B3%F6%C8%C3%7C4a611fc4-75b2-9531-ac26-8d25b002dc2b%3A2019-4-29%7E2019-5-9"),
                                    'TAB_QuerySubmitOrderData': tab_querysubmitorderdata,
                                    'TAB_QuerySubmitSortData': '',
                                    'TAB_RowButtonActionControl': ''},callback=self.parse_item,
                              meta={"viewstate": viewstate, "eventvalidation": eventvalidation, "tab_querysubmitorderdata": tab_querysubmitorderdata ,"tab_querysortitemlist":tab_querysortitemlist}
                          )

    # 解析内容函数
    def parse_item(self, response):
            item = TudiItem()
            item['viewstate'] = response.meta['viewstate']
            item['eventvalidation'] = response.meta['eventvalidation']
            item['tab_querysortitemlist'] = response.meta['tab_querysortitemlist']
            item['tab_querysubmitorderdata'] = response.meta['tab_querysubmitorderdata']
            page=response.selector.xpath('//td[@class="pager"]/text()')[0].extract()
            count = page[page.find("共") +1 :page.find("页")]
            # count = page[page.find("共".decode('utf-8')) + 1:page.find("页".decode('utf-8'))]
            for i in range(1, int(count)+1):
            # for i in range(2, 57):
                yield FormRequest(url="http://www.landchina.com/default.aspx?tabid=262&ComName=default",
                              formdata={'TAB_QuerySubmitPagerData':str(i),
                                        'hidComName': 'default',
                                        '__VIEWSTATE': item['viewstate'],
                                        '__EVENTVALIDATION': item['eventvalidation'],
                                        'TAB_QuerySortItemList': item['tab_querysortitemlist'],
                                        'TAB_QuerySubmitConditionData': urllib.parse.unquote_to_bytes("66cc8979-1a1d-4fd5-b22a-0aeb1e14c6fd%3A2%A8%88%7E%D5%D0%C5%C4%B9%D2%B3%F6%C8%C3%7C4a611fc4-75b2-9531-ac26-8d25b002dc2b%3A2019-4-29%7E2019-5-9"),
                                        'TAB_QuerySubmitOrderData': item['tab_querysubmitorderdata'] ,
                                        'TAB_QuerySubmitSortData': '',
                                        'TAB_RowButtonActionControl': ''
                                        },callback=self.parse_first
                                  )

# 解析内容函数
    def parse_first(self, response):
        for sel in response.xpath('//tr[@onmouseout="this.className=rowClass"]'):
            item = TudiItem()
            link = sel.xpath('td[@class="queryCellBordy"]/a/@href')[0].extract()
            item['link'] = link
            url = "http://www.landchina.com/" + item['link']
            haoma = sel.xpath('td[@class="gridTdNumber"]/text()')[0].extract()
            item['haoma'] = haoma
            outdistrict1 = sel.xpath('td[@class="queryCellBordy"][1]/span/text()').extract_first()
            outdistrict2 = sel.xpath('td[@class="queryCellBordy"][1]/text()').extract_first()
            print (1111111111,outdistrict1) #看是否获取到
            print (22222222222,outdistrict2)#看是否获取到
            if outdistrict1 == None :
                print ('==================') #看这个判断是否获取到
                item['outdistrict'] = outdistrict2
            else :
                item['outdistrict'] = outdistrict1
            outline1 = sel.xpath('td[@class="queryCellBordy"][2]/a/span/text()').extract_first()
            outline2 = sel.xpath('td[@class="queryCellBordy"][2]/a/text()').extract_first()
            if outline1 == None :
                item['outline'] = outline2
            else :
                item['outline'] = outline1
            issuedate1 = sel.xpath('td[@class="queryCellBordy"][3]/text()').extract_first()
            item['issuedate1'] = issuedate1
            pagenum = response.selector.xpath('//td[@class="pager"]/span/text()')[0].extract()
            item['pagenum'] = pagenum
            yield Request(url, callback=self.parse_info,
                          meta={"haoma": haoma, "outdistrict": item['outdistrict'],  "url":url ,"pagenum": pagenum , "outline": item['outline'], "issuedate1": issuedate1})  # 这边的yield千万对齐上面的item，要不然只循环最后一条链接
                          # meta={'TudiItem':TudiItem})




    def parse_info(self, response):  # 位置要对齐上面的def
        for sel in response.xpath('//table[@style="border-collapse:collapse; border-color:#333333;font-size:12px;"]'):
            item = TudiItem()

            landno = sel.xpath('tr[1]/td[2]/text()').extract_first()
            item['landno'] = "'" + landno
            landlocation = sel.xpath('tr[1]/td[4]/text()').extract_first()
            item['landlocation'] = landlocation.replace('\r', '').replace('\n', '').strip()
            province = response.selector.xpath('//span[@id="lblXzq"]/text()')[0].extract()
            item['province'] = province
            cityname = response.selector.xpath('//span[@id="lblXzq"]/text()')[0].extract()
            item['cityname'] = cityname[cityname.find(">") + 2:cityname.rfind(">") - 1]
            district = response.selector.xpath('//span[@id="lblXzq"]/text()')[0].extract()
            item['district'] = district[district.rfind(">") + 2:]
            piece = response.selector.xpath( '//td[@id="tdContent"]/table/tr[2]/td/p[2]/u[3]/text()').extract_first()
            item['piece'] = piece
            upheadline = response.selector.xpath('//td[@class="ContentTitle3"]/span/text()').extract_first()
            item['upheadline'] = upheadline
            downheadline = response.selector.xpath('//td[@id="tdContent"]/table/tr/td/text()').extract_first()
            item['downheadline'] = downheadline.strip()
            headno = re.findall(r'<br/>(.*?)</td>', response.text, re.DOTALL)  # -------------------------------
            if headno:
                print(111111111, headno)
                item['headno'] = headno[0].strip()
            else:
                item['headno'] = None

            # item['headno'] = headno
            issuedate2 = response.selector.xpath('//table[@id="Table2"]/tr[3]/td/span/text()').extract_first()
            item['issuedate2'] = issuedate2
            landname = sel.xpath('tr[1]/td[4]/text()').extract_first()
            item['landname'] = landname.replace('\r', '').replace('\n', '').strip()
            landextend = sel.xpath('tr[1]/td[4]/text()').extract_first()
            item['landextend'] = landextend.replace('\r', '').replace('\n', '').strip()
            application = sel.xpath('tr[1]/td[6]/text()').extract_first()

            item['application'] = application
            area = sel.xpath('tr[2]/td[2]/text()').extract_first()
            item['area'] = area
            price = sel.xpath('tr[2]/td[6]/text()').extract_first()
            item['price'] = price
            buyer = sel.xpath('tr[3]/td[2]/text()').extract_first()
            item['buyer'] = buyer
            item['haoma'] = response.meta['haoma']
            item['outdistrict'] = response.meta['outdistrict']
            item['outline'] = response.meta['outline']
            item['issuedate1'] = response.meta['issuedate1']
            item['pagenum'] = response.meta['pagenum']
            item['url'] = response.meta['url']
            day1 = response.selector.xpath('//td[@id="tdContent"]/table/tr[2]/td/p[2]/u[1]/text()').extract_first()
            item['day1'] = day1
            day2 = response.selector.xpath('//td[@id="tdContent"]/table/tr[2]/td/p[2]/u[2]/text()').extract_first()
            item['day2'] = day2
            day3 = response.selector.xpath('//td[@id="tdContent"]/table/tr[2]/td/p[2]/u[2]/text()').extract_first()
            item['day3'] = day3
            method = response.selector.xpath('//td[@id="tdContent"]//p[2]/text()').extract()
            methodd = ''.join(method)
            item['method'] = methodd[methodd.rfind("出让") - 2:methodd.rfind("出让")]
            spare = sel.xpath('tr/td[@colspan="9"]/text()').extract_first()
            if spare:
                item['spare'] = spare.replace('\r', '').replace('\n', '').replace('\t', '').strip()
            else:
                item['spare'] = None
            yield item




