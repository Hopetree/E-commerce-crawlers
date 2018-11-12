# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy import log
from scrapy.conf import settings
import time



class TMPipeline(object):
    def __init__(self):
        if len(settings['TMALL_SHOP_DOMAINS']) == 1:
            name = settings['TMALL_SHOP_DOMAINS'][0]
        else:
            name = 'tmall_{}'.format(time.strftime('%Y%m%d-%H%M%S'))
        self.file = r'G:\Mycodes\ECspiers\ECspiers\data\{}.csv'.format(name)
        self.headers = settings['TMALL_ITEM_TITLE']
        self.create_file()

    def create_file(self):
        with open(self.file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers, extrasaction='ignore')
            writer.writeheader()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
        if valid:
            with open(self.file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers, extrasaction='ignore')
                writer.writerow(item)
            log.msg('write item to file successfully !', level=log.DEBUG, spider=spider)
        return item
