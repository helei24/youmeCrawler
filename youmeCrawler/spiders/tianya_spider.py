from scrapy.spider import Spider  
from scrapy.selector import HtmlXPathSelector
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
        
        sel1 = HtmlXPathSelector(response)
        content = self1.select('//div[@class="bbs-content clearfix"]')
        print content
        return content


    def parse(self, response):  

        sel = HtmlXPathSelector(response)  
        table_trs = sel.xpath('//table/tbody[2]/tr')  
        items = []
        for tr in table_trs:  
            item = TianyaItem()
            item['title'] = tr.select('//td[1]/a/text()').extract()
            item['content_url'] = tr.xpath('//td[1]/a/@href').extract()[0].strip() 
            item['content']= Request("http://bbs.tianya.cn"+item['content_url'], meta={'item':item}, callback=self.content_parse)

            item['author'] = tr.select('//td[2]/a/text()').extract()
            item['hits'] = tr.select('//td[3]/text()').extract()
            item['replies'] = tr.select('//td[4]/text()').extract()
            item['time'] = tr.select('//td[5]/@title').extract()
            items.append(item)

            # print item['content_url']
            # print item['replies']
        # return items