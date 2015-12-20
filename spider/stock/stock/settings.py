# Scrapy settings for dirbot project

SPIDER_MODULES = ['stock.spiders']
NEWSPIDER_MODULE = 'stock.spiders'
DEFAULT_ITEM_CLASS = 'stock.items.StockListItem'

ITEM_PIPELINES = {'stock.pipelines.StockPipeline': 1,
                  'stock.pipelines.MysqlStoreStockPipeLine' : 1,
                }

#mysql settings
MYSQL_HOST   = 'localhost'
MYSQL_DBNAME = 'db_chuanxi'
MYSQL_USER   = 'chuanxi'
MYSQL_PASSWD = 'chuanxi2015@cx.com'
