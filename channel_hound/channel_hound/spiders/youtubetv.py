# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request

from channel_hound.items import ChannelItem


class YoutubetvSpider(scrapy.Spider):
    name = 'youtubetv'
    allowed_domains = ['tv.youtube.com', 'youtube-tv-zip-lookup.appspot.com']
    start_urls = [
        'https://tv.youtube.com/welcome'
    ]
    service = 'YouTube TV'

    def parse(self, response):
        premium_row = response.xpath('//ul[contains(@class, "network-matrix__cells--premium")]/li')
        for premium_element in premium_row:
            package = {'service': YoutubetvSpider.service, 'name': 'Add-On'}
            package['price'] = premium_element.xpath('substring-after(./div[@class="caption"]/text(), "$")').extract()[0].replace("/mo", "").strip()
            name = premium_element.xpath('./div[contains(@class, "network-matrix__cells-cell-cloak")]/@aria-label').extract()[0].strip()

            yield ChannelItem(name=name, package=package)

        base_price = response.xpath('substring-after(substring-before(//p[@class="c-hero-banner__content-price"]/text(), "/"), "$")').extract()[0].strip()
        yield Request('https://youtube-tv-zip-lookup.appspot.com/zipLookup/v1/availability/33065',
                      callback=self.parse_base_channels, meta={'price': base_price})

    def parse_base_channels(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        for market in jsonresponse['markets']:
            for channel in market['channels']:
                if not channel['add_on']:
                    package = {'service': YoutubetvSpider.service, 'price': response.meta['price'], 'name': 'Base'}
                    yield ChannelItem(name=channel['display_name'], package=package)
