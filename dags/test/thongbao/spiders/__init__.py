import time
import scrapy
from getAndCheckDB import *
from thongbao.items import ThongbaoItem
import logging

class QuotesSpider(scrapy.Spider):
    name = "thongbao"

    def start_requests(self):
        urls = [
            'http://daotao.ute.udn.vn/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        main_html = response.css('#inner-column-container > div:nth-child(2) a[style]')
        next_page = response.css('#inner-column-container > div:nth-child(2) table:not(table[wrap]) ')
        for ht in (main_html):
            getdata = ht.css('a::attr(href)').extract()[0] 
            print(getdata)
            if(check_notification(getdata.split('mid=')[-1])):
                logging.info("[!] OLD_DATA STOP !!")
                return
            yield  scrapy.Request(url='http://daotao.ute.udn.vn/'+getdata, callback=self.getTC)

        next_page = next_page[-1].css('a::attr(href)').extract()[-1]
        print(next_page)
        yield scrapy.Request(url='http://daotao.ute.udn.vn/'+next_page,callback=self.parse)

    def getTC(self, response):
        k = ThongbaoItem()
        main_CT = response.css("#pagemain > table:nth-child(2)")
        for x in main_CT:
            k['id'] = response.url.split('mid=')[-1]
            txt = x.css('font b::text').get()
            k['title']= ' '.join(txt.split())
            cnt = x.css(' tr:nth-child(2) td::text').extract()
            k['content'] = ' '.join(cnt)
            yield k