# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from scrapy.conf import settings


class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlStoreStockPipeLine(object):

    def __init__ (self):
         self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

    """
    def from_settings (cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=true,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',dbargs)
        return cls(dbpool)
    """

    #pipeline默认调用
    def process_item (self,item,spider):
        d = self.dbpool.runInteraction(self.do_upinsert,item,spider)
        #d.addErrBack(self.handle_error,item,spider)
        #d.addErr
        d.addBoth(lambda _:item)
        return d

    #将每行更新或写入数据库中
    def do_upinsert (self,conn,item,spider):
        stock_id = self.get_id(item)

        #print stock_id
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
            select 1 from t_stock where stock_id = %s and stock_name = %s
            """,(stock_id,item['stock_name']))

        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update t_stock set stock_name = %s where stock_id = %s
                """, (item['stock_name']),stock_id)
        else:
            conn.execute("""
                insert into t_stock(stock_id ,stock_name) values(%s,%s)
                """,(item['stock_id'],item['stock_name']))

    def get_id (self,item):
        return item['stock_id']

    def handle_error (self,failure,item,spider):
        log.err(failure)

