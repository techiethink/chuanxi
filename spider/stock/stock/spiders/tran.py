# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from hashlib            import md5
from scrapy.conf        import settings

#http://quotes.money.163.com/service/chddata.html?code=0600741&amp;start=19960826&amp;end=20151220&amp;fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
class TranSpider(scrapy.Spider):
    name = "trans"
    allowed_domains = ["163.com"]
    download_delay  = 4
    #start_urls = ( "www.163.com" )


    def __init__ (self, category=None, *args, **kwargs):
        super(TranSpider, self).__init__(*args, **kwargs)
        self.day = datetime.datetime.now()
        self.init_mysql()
        self.init_urls()


    def parse(self, response):

        pass


    def init_mysql (self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

    def init_urls (self):
        d = self.dbpool.runInteraction(self.do_select)


    def do_select (self,conn):
        ret = conn.execute("""
            select stock_id from t_stock
            """)

        storeResult = conn.fetchall()

        urls = []
        for stock_id in storeResult:
            #print self.quotes_url(stock_id['stock_id'])
            url = self.quotes_url(stock_id['stock_id'])
            urls.append(url)

        self.start_urls = urls;
        #print self.start_urls;


    def quotes_url (self,stock_id):
        #now = time.strptime(self.day,'%Y%m%d');
        now = self.day.strftime("%Y%m%d")
        url = 'http://quotes.money.163.com/service/chddata.html?code='+ stock_id + '&start=19960826&end='+ now +'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        return url
