# -*- coding:utf-8 -*-

import scrapy
from scrapy.conf import settings
from ..items import EcspiersItem

from urllib import parse
import time
import re
import json


class TMSpider(scrapy.Spider):
    name = 'tmall_m'
    allowed_domains = ["tmall.com"]
    start_urls = [
        'https://m.tmall.com'
    ]

    def parse(self, response):
        for shop_domain in settings['TMALL_SHOP_DOMAINS']:
            url = 'https://{0}.m.tmall.com/shop/shop_auction_search.do'.format(shop_domain)
            params = {
                'sort': 's',
                'p': 1,
                'from': 'h5',
                'ajson': 1,
                '_tm_source': 'tmallsearch',
                'callback': 'json{}'.format(time.time())
            }
            url = '{0}?{1}'.format(url, parse.urlencode(params))
            yield scrapy.Request(url, callback=self.parse_get_items, meta={'shop_domain': shop_domain})

    def parse_get_items(self, response):
        shop_domain = response.meta['shop_domain']
        data = re.findall('json.*?\(({.*})\)', response.text)
        if data:
            data = json.loads(data[0])
            items = data.get('items')
            if items:
                for each in items:
                    item_id = each.get('item_id')
                    params = {
                        'itemId': item_id,
                        'callback': 'json{}'.format(time.time())
                    }
                    url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?{}'.format(parse.urlencode(params))
                    yield scrapy.Request(url, callback=self.parse_get_dsr, meta={'each_item': each})
            total_page = data.get('total_page')
            current_page = data.get('current_page')
            if total_page and current_page:
                if int(current_page) < int(total_page):
                    print('当前爬取页码是>>>>>>>>>>>>>>>>>>>>>', current_page)
                    next_page = int(current_page) + 1
                    url = 'https://{0}.m.tmall.com/shop/shop_auction_search.do'.format(shop_domain)
                    params = {
                        'sort': 's',
                        'p': next_page,
                        'from': 'h5',
                        'ajson': 1,
                        '_tm_source': 'tmallsearch',
                        'callback': 'json{}'.format(time.time())
                    }
                    url = '{0}?{1}'.format(url, parse.urlencode(params))
                    yield scrapy.Request(url, callback=self.parse_get_items, meta={'shop_domain': shop_domain})

    def parse_get_dsr(self, response):
        each = response.meta['each_item']
        data = re.findall('json.*?\(({.*})\)', response.text)
        if data:
            data = json.loads(data[0])
            dsr = data.get('dsr').get('gradeAvg')
            each['dsr'] = dsr
        item = EcspiersItem()
        for key in settings['TMALL_ITEM_TITLE']:
            item[key] = each.get(key)
        yield item

