# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime
from scrapy.spiders        import Spider
from scrapy.selector       import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http           import Request
from stock.items           import StockListItem

class StockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["eastmoney.com"]
    download_delay = 4
    start_urls = (
        'http://quote.eastmoney.com/stocklist.html',
    )
    day = datetime.datetime.now()
    count = 0

    def parse(self, response):
        # save fifle
        #self.save(response)

        #fetch
        return self.parse_response(response)



    def save (self,response):
        filename = response.url.split("/")[3]
        with open(filename, 'wb') as f:
            f.write(response.body)

        #### print
        print filename


    def parse_response (self,response):
        sel = Selector(response)
        sites = sel.xpath('//div [@class="quotebody"]//ul/li/a')
        items = []

        for site in sites:
            stockname = site.xpath('text()').extract()[0].encode('utf-8');
            item = self.split_item(stockname)
            if item:
                items.append(item)

        return items

    def split_item (self,stockname):

        matchObj = re.match(r'(.*)\((.*)\)', stockname)

        if matchObj:
            item = StockListItem()
            item['stock_name'] = matchObj.group(1)
            item['stock_id']   = matchObj.group(2)
            #item['f_url']  = self.quotes_url(matchObj.group(2))
            return item

        else:
            print "no match", stockname
            return matchObj

    def quotes_url (self,stock_id):
        #now = time.strptime(self.day,'%Y%m%d');
        now = self.day.strftime("%Y%m%d")
        url = 'http://quotes.money.163.com/service/chddata.html?code='+ stock_id + '&start=19960826&end='+ now +'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        return url


