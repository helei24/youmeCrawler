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
from time import mktime
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
import redis
from youmeCrawler.youmeLogger import logger

class YoumecrawlerPipeline(object):

	global logger
	
	#redis pool connection part
	pool = redis.ConnectionPool(host='127.0.0.1', port=6379) 
	
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb', db = 'youme', user = 'root', passwd = '', cursorclass = MySQLdb.cursors.DictCursor, charset = 'utf8', use_unicode = False)

	def process_item(self, item, spider):

		r = redis.Redis(connection_pool=self.pool)

		if r.get(item['post_id']) is None:
			
			logger.debug(item['post_id'] + ' is not in Redis.')
			if item['is_post']:
				
				item_str =  'post_id: ' + item['post_id'] + '\ttitle: ' + item['title'] + '\tpost_url: ' + item['post_url'] + '\tauthor_id: ' \
            	+ item['author_id'] + '\tauthor: ' + item['author'] + '\tcontent: ' + item['content'] + '\thits: ' + item['hits'] + \
            	'\treplies: ' + item['replies'] + '\tatime: ' + item['atime'] + '\tis_post: ' + str(item['is_post']) 
				
				logger.info('Store post to DB, ' + item_str)
				query = self.dbpool.runInteraction(self.insert_post, item)
				query.addErrback(self.handle_error)
				r.set(item['post_id'], item['atime'])
			else:
				
				item_comment_str = 'post_id: ' + item['post_id'] + '\tcomment: ' + item['comment'] + '\tcomment_author_id: ' + item['comment_author_id']\
                + '\tcomment_author: ' + item['comment_author'] + '\tatime: ' + item['atime'] + '\tis_post: ' + str(item['is_post']) 
				
				logger.info('Store comment to DB, ' + item_comment_str)
				query = self.dbpool.runInteraction(self.insert_comment, item)
				query.addErrback(self.handle_error)
		else:
			logger.debug(item['post_id'] + ' exists in Redis.')	

	def insert_post(self, tx, item):

		atime = item['atime'].encode("utf-8")
		tx.execute('insert into post(post_id, title, author_id, author, content, hits, replies, post_url, atime)'\
		'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (int(item['post_id']), item['title'], int(item['author_id']), item['author'], item['content'], int(item['hits']), int(item['replies']), item['post_url'], datetime.datetime.strptime(atime, "%Y-%m-%d %H:%M:%S")))

	def insert_comment(self, tx, item):

		tx.execute('insert into comment(post_id, comment_author_id, comment_author, comment, atime) values (%s, %s, %s, %s, %s)',(int(item['post_id']), int(item['comment_author_id']), item['comment_author'], item['comment'], datetime.datetime.strptime(item['atime'].encode("utf-8"), "%Y-%m-%d %H:%M:%S")))

	def handle_error(self, e):
		logger.error('Store error: ' + e)