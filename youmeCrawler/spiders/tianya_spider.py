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
        # head = sel.xpath('//div[@id="post_head"]')

        # title = head.sele('h1/span[@class="s_title"]/span/text()').extract()
        # item['author_id'] = sel.xpath('//div[@id="post_head"]/div/div[@class="atl-info"]/span[1]/@value').extract()[0].strip()
        # author =  head.xpath('div/div[@class="atl-info"]/span[1]/a/text()').extract()
        # time = head.xpath('div/div[@class="atl-info"]/span[2]/text()').extract()
        # hits = head.xpath('div/div[@class="atl-info"]/span[3]/text()').extract()
        # reply = head.xpath('div/div[@class="atl-info"]/span[4]/text()').extract()
        item['content'] = sel.xpath('//div[@class="bbs-content clearfix"]').extract()[0].strip()
        items.append(item)
        print item['time']
        # return items


    def parse(self, response):  

        sel = Selector(response)  
        table_trs = sel.xpath('//table/tbody[2]/tr')
        items = []
        for tr in table_trs:  
           
            item = TianyaItem()
            item['title'] = tr.xpath('td[1]/a/text()').extract()[0].strip()
            item['author'] = tr.xpath('td[2]/a/text()').extract()[0].strip()
            item['hits'] = tr.xpath('td[3]/text()').extract()[0].strip()
            item['replies'] = tr.xpath('td[4]/text()').extract()[0].strip()
            item['time'] = tr.select('td[5]/@title').extract()[0].strip()
            item['content_url'] = tr.xpath('td[1]/a/@href').extract()[0].strip()
    
            items.append(item)

            for item in items:
                yield Request("http://bbs.tianya.cn%s" % item['content_url'], meta={'item':item}, callback=self.content_parse)
