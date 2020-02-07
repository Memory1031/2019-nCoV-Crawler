# -*- coding: utf-8 -*-
import json

import scrapy
from nCoV.items import Community


class CommunitySpider(scrapy.Spider):
    name = 'Community'
    allowed_domains = ['html5.qq.com']
    start_urls = ['https://ncov.html5.qq.com/api/getPosition']

    def parse(self, response):
        totalCity = json.loads(response.text).get("position")
        for (province, value) in totalCity.items():
            for city in value.keys():
                yield scrapy.Request(
                    "https://ncov.html5.qq.com/api/getCommunity?province=%s&city=%s&district=全部" % (province, city),
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
        areaList = list(list(json.loads(response.text).get("community").values())[0].values())[0]
        for district in areaList.values():
            item = Community()
            item['province'] = district[0].get("province")
            item['city'] = district[0].get("city")
            item['district'] = district[0].get("district")
            item['county'] = district[0].get("county")
            item['street'] = district[0].get("street")
            item['community'] = district[0].get("community")
            item['show_address'] = district[0].get("show_address")
            item['cnt_inc_uncertain'] = district[0].get("cnt_inc_uncertain")
            item['cnt_inc_certain'] = district[0].get("cnt_inc_certain")
            item['cnt_inc_die'] = district[0].get("cnt_inc_die")
            item['cnt_inc_recure'] = district[0].get("cnt_inc_recure")
            item['cnt_sum_uncertain'] = district[0].get("cnt_sum_uncertain")
            item['cnt_sum_certain'] = district[0].get("cnt_sum_certain")
            item['cnt_sum_die'] = district[0].get("cnt_sum_die")
            item['cnt_sum_recure'] = district[0].get("cnt_sum_recure")
            item['full_address'] = district[0].get("full_address")
            item['lng'] = district[0].get("lng")
            item['lat'] = district[0].get("lat")
            yield item
