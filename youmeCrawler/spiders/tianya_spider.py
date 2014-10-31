# -*- coding: utf-8 -*-

import chardet
from scrapy.spider import Spider  
from scrapy.selector import Selector
from youmeCrawler.items import PostItem, CommentItem
from scrapy.http import Request
from youmeCrawler.youmeLogger import logger

class TianyaSpider(Spider):
####################################################################################################
    name = "tianya"  
    
    download_delay = 1
    allowed_domains = ["bbs.tianya.cn"]  
    start_urls = [  
        "http://bbs.tianya.cn/list-feeling-1.shtml" 
    ]  
 
    def content_parse(self, response):
        
        global logger

        logger.debug('Begin to parse post content and its comment info.')
        sel = Selector(response)

        item = response.meta['item']
        items = []

        author_id = item['author_id']   #author id of of current post
        item['atime'] = sel.xpath('//div[@id="post_head"]/div[1]/div[@class="atl-info"]/span[2]/text()').extract()[0].strip()[3:]          #get the publish time of each part(content or comment) 
        item['content'] = sel.xpath('//div[@class="atl-item"]/div[@class="atl-content"]/div[2]/div[@class="bbs-content clearfix"]/text()').extract()[0].strip()

        atl_items = sel.xpath('//div[@class="atl-item"]')
        for atl_item in atl_items:
            
            content_or_comment = atl_item.xpath('div[@class="atl-content"]/div[2]/div[@class="bbs-content"]/text()').extract()
            if len(content_or_comment) == 0:
                continue
            else:
                content_or_comment = content_or_comment[0].strip()
                author = atl_item.xpath('div[@class="atl-head"]/div[@class="atl-info"]/span[1]/a/text()').extract()[0].strip()
                author_tmp_id = atl_item.xpath('div[@class="atl-head"]/div[@class="atl-info"]/span[1]/a/@href').extract()[0].strip().split('/')[3]
                atime = atl_item.xpath('div[@class="atl-head"]/div[@class="atl-info"]/span[2]/text()').extract()[0].strip()[3:]                                  #时间：2014-10-18 16:02:05    
            
                if author_tmp_id == author_id:
                    item['content'] += content_or_comment
                else:
                    item_comment = CommentItem()
                    item_comment['comment'] = content_or_comment   
                    item_comment['post_id'] = item['post_id']
                    item_comment['comment_author_id'] = author_tmp_id
                    item_comment['comment_author'] = author
                    item_comment['atime'] = atime 
                    item_comment['is_post'] = False  

                    item_comment_str = 'post_id: ' + item_comment['post_id'] + '\tcomment: ' + item_comment['comment'] + '\tcomment_author_id: ' + item_comment['comment_author_id']\
                    + '\tcomment_author: ' + item_comment['comment_author'] + '\tatime: ' + item_comment['atime'] + '\tis_post: ' + str(item_comment['is_post']) 

                    logger.debug('Comment info: ' + item_comment_str)
                    items.append(item_comment)

        item_str =  'post_id: ' + item['post_id'] + '\ttitle: ' + item['title'] + '\tpost_url: ' + item['post_url'] + '\tauthor_id: ' \
            + item['author_id'] + '\tauthor: ' + item['author'] + '\tcontent: ' + item['content'] + '\thits: ' + item['hits'] + \
            '\treplies: ' + item['replies'] + '\tatime: ' + item['atime'] + '\tis_post: ' + str(item['is_post']) 
            
        logger.debug('Post info: ' + item_str)             
        items.append(item)

        # print item['time']
        return items


    def parse(self, response):  

        global logger

        logger.debug('Begin to parse post head at title list.')
        sel = Selector(response)  
        table_trs = sel.xpath('//table/tbody[2]/tr')
        items = []
        for tr in table_trs:
            
            item = PostItem()
            item['title'] = tr.xpath('td[1]/a/text()').extract()[0].strip()
            item['author'] = tr.xpath('td[2]/a/text()').extract()[0].strip()
            item['author_id'] = tr.xpath('td[2]/a/@href').extract()[0].strip().split('/')[3]
            item['hits'] = tr.xpath('td[3]/text()').extract()[0].strip()
            item['replies'] = tr.xpath('td[4]/text()').extract()[0].strip()
            item['post_url'] = tr.xpath('td[1]/a/@href').extract()[0].strip()
            item['post_id'] = item['post_url'].split('-')[2]
            item['atime'] = tr.xpath('td[5]/@title').extract()[0].strip()
            item['is_post'] = True
            
            items.append(item)

        for item in items:
            # print item['post_url']
            logger.debug('Begin to request post, id :' + item['post_id'] + '\turl: ' + 'http://bbs.tianya.cn%s' % item['post_url'])
            yield Request("http://bbs.tianya.cn%s" % item['post_url'], meta={'item':item}, callback=self.content_parse)
