# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import datetime,time
import MySQLdb
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno
import json
import codecs

class YoumecrawlerPipeline(object):
	
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb', db = 'youme', user = 'root', passwd = '', cursorclass = MySQLdb.cursors.DictCursor, charset = 'utf8',use_unicode = False)

    def process_item(self, item, spider):
    	query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handle_error)
        return item    

	def insert(self, tx, item):
		tx.execute('insert into youme values (%s, %s, %s, %s, %s, %s)', item['title'], item['author'], item['content'], int(item['hits']), int(item['replies']), item['content_url'], time.strptime(item['time'], "%Y-%m-%d %H:%M"))

	def handle_error(self, e):
		log.err(e)