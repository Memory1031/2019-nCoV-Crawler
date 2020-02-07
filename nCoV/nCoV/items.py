# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class NcovItem(scrapy.Item):
    date = scrapy.Field()
    areaTree = scrapy.Field()


class Community(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    county = scrapy.Field()
    street = scrapy.Field()
    community = scrapy.Field()
    show_address = scrapy.Field()
    cnt_inc_uncertain = scrapy.Field()
    cnt_inc_certain = scrapy.Field()
    cnt_inc_die = scrapy.Field()
    cnt_inc_recure = scrapy.Field()
    cnt_sum_uncertain = scrapy.Field()
    cnt_sum_certain = scrapy.Field()
    cnt_sum_die = scrapy.Field()
    cnt_sum_recure = scrapy.Field()
    full_address = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
