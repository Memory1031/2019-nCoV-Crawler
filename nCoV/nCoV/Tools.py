# -*- coding: utf-8 -*-
# 定义ensure_ascii=False,避免直接输出unicode
from scrapy.exporters import JsonLinesItemExporter


class CustomJsonLinesItemExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        super(CustomJsonLinesItemExporter, self).__init__(file, ensure_ascii=False, **kwargs)


FEED_EXPORTERS = {
    'json': 'finance.settings.CustomJsonLinesItemExporter',
}
