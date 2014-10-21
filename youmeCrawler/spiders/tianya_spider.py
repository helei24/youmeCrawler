# -*- coding: utf-8 -*-

import chardet
from scrapy.spider import Spider  
from scrapy.selector import Selector
from youmeCrawler.items import TianyaItem
from scrapy.http import Request
class TianyaSpider(Spider):

    name = "tianya"  
    
    download_delay = 1
    allowed_domains = ["bbs.tianya.cn"]  
    start_urls = [  
        "http://bbs.tianya.cn/list-feeling-1.shtml" 
    ]  
 
    def content_parse(self, response):
        
        sel = Selector(response)

        item = response.meta['item']
        items = []

        user_id = item['author_id']
        
        item['content'] = ''

        atl_items = sel.xpath('//div[@class="atl-item"]')
        for atl_item in atl_items:
            
            content_or_coment = atl_item.xpath('div[@class="atl-content"]/div[2]/div[@class="bbs-content"]/text()').extract()[0].strip()
            
            user_tmp_id = atl_item.xpath('div[@class="atl-head"]/div[@class="atl-info"]/span[1]/a/@href').extract()[0].strip().split('/')[3]
            print user_tmp_id

            if(user_tmp_id == user_id):
                item['content'] += content_or_coment
            else:
                item['coment'] = content_or_coment   



        items.append(item)
        # print item['time']
        # return items


    def parse(self, response):  

        sel = Selector(response)  
        table_trs = sel.xpath('//table/tbody[2]/tr')
        items = []
        for tr in table_trs:  
           
            item = TianyaItem()
            item['title'] = tr.xpath('td[1]/a/text()').extract()[0].strip()
            item['author'] = tr.xpath('td[2]/a/text()').extract()[0].strip()
            item['author_id'] = tr.xpath('td[2]/a/@href').extract()[0].strip().split('/')[3]
            item['hits'] = tr.xpath('td[3]/text()').extract()[0].strip()
            item['replies'] = tr.xpath('td[4]/text()').extract()[0].strip()
            item['time'] = tr.xpath('td[5]/@title').extract()[0].strip()
            item['content_url'] = tr.xpath('td[1]/a/@href').extract()[0].strip()
    
            items.append(item)

            for item in items:
                yield Request("http://bbs.tianya.cn%s" % item['content_url'], meta={'item':item}, callback=self.content_parse)
