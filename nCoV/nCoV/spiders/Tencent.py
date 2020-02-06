# -*- coding: utf-8 -*-
import json

import scrapy
from nCoV.items import NcovItem


class HenanSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['inews.qq.com']
    start_urls = ['https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5']
    base_url = ""

    def parse(self, response):
        item = NcovItem()
        rs = json.loads(response.text)
        item['date'] = json.loads(rs.get('data')).get('lastUpdateTime')
        item['areaTree'] = json.loads(rs.get('data')).get('areaTree')[0]['children']
        return item
