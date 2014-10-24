# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class YoumecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PostItem(Item): 

    post_id = Field()
    title = Field()
    post_url = Field()
    author_id = Field()
    author = Field()
    content = Field()
    hits = Field()
    replies = Field()
    is_post = Field()
    atime = Field()

class CommentItem(Item):
    
    post_id = Field()
    comment = Field()
    comment_author_id = Field()
    comment_author = Field()
    is_post = Field()
    atime = Field()
