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

class YoumecrawlerPipeline(object):
	
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb', db = 'youme', user = 'root', passwd = '', cursorclass = MySQLdb.cursors.DictCursor, charset = 'utf8', use_unicode = False)

	def process_item(self, item, spider):

		if item['is_post']:
			query = self.dbpool.runInteraction(self.insert_post, item)
			query.addErrback(self.handle_error)
		else:
			print ""
			# query = self.dbpool.runInteraction(self.insert_comment, item)
			# query.addErrback(self.handle_error)
		# return item

	def insert_post(self, tx, item):

		atime = item['time'].encode("utf-8")
		print type(time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(atime, "%Y-%m-%d %H:%M:%S")))
		# tx.execute('insert into post(post_id, title, author_id, author, content, hits, replies, post_url, time)'\
		# 'values (%s, %s, %s, %s, %s, %s, %s, %s)', (int(item['post_id']), item['title'], int(item['author_id']), item['author'], item['content'], int(item['hits']), int(item['replies']),\
		# item['post_url'], time.strptime(atime, "%Y-%m-%d %H:%M:%S")))

	def insert_comment(self, tx, item):
		tx.execute('insert into comment(post_id, comment_author_id, comment_author, comment, time) values (%s, %s, %s, %s, %s, %s)',\
		int(item['post_id']), int(item['comment_author_id']), item['comment_author'], item['comment'], time.strptime(item['time'], "%Y-%m-%d %H:%M"))	

	def handle_error(self, e):
		log.err(e)