from scrapy.spider import Spider  
from scrapy.selector import Selector
from youmeCrawler.items import TianyaItem

class TianyaSpider(Spider):

    name = "tianya"  
    
    download_delay = 1
    allowed_domains = ["bbs.tianya.cn"]  
    start_urls = [  
        "http://bbs.tianya.cn/list-feeling-1.shtml" 
    ]  
 
    def parse(self, response):  
        sel = Selector(response)  
        table_trs = sel.xpath('//table/tbody[2]/tr')  
        items = []  
        for tr in table_trs:  
            item = TianyaItem()
            item['title'] = tr.xpath('//td[1]/a/text()').extract()
            # item['content'] = tr.xpath('a/@href').extract() 
            item['author'] = tr.xpath('//td[2]/a/text()').extract()
            item['hits'] = tr.xpath('//td[3]/text()').extract()
            item['replies'] = tr.xpath('//td[4]/text()').extract()
            item['time'] = tr.xpath('//td[5]/@title').extract()
            items.append(item)  

            print type(item['replies'])
            # print item['replies']
        # return items