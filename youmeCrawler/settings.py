# -*- coding: utf-8 -*-

# Scrapy settings for youmeCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'youmeCrawler'

SPIDER_MODULES = ['youmeCrawler.spiders']
NEWSPIDER_MODULE = 'youmeCrawler.spiders'

ITEM_PIPELINES = {
    'youmeCrawler.pipelines.YoumecrawlerPipeline':300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'youmeCrawler (+http://www.yourdomain.com)'

