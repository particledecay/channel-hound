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
        all_channels = response.xpath('//div[@class="zip__network"]')
        base_price = response.xpath('substring-after(substring-before(//span[@class="price"]/text(), "/"), "$")').extract()[0].strip()
        for channel in all_channels:
            name = channel.xpath('./p[@class="zip__network-name"]/text()').extract()[0].strip()
            package = {'service': YoutubetvSpider.service}
            channel_page = channel.xpath('./a[1]/@href').extract()
            if not channel_page:
                if channel.xpath('./ancestor::ul[@class="zip__networks"]/preceding-sibling::h4[contains(., "Additional Networks")]'):
                    package['name'] = 'Add-On'
                else:
                    package['name'] = 'Base'
                package['price'] = base_price

                yield ChannelItem(name=name, package=package)
            else:
                yield Request(channel_page[0], callback=self.parse_base_channels, meta={'name': name, 'base_price': base_price, 'package': package})

    def parse_base_channels(self, response):
        package = response.meta['package']
        price = response.xpath('substring-after(substring-before(//div[@class="ytv-promo-drawer-text-primary"]/text(), "/"), "$")').extract()
        if not price:
            price = response.meta['base_price']
        else:
            price = price[0].strip()
        package['price'] = price
        if response.xpath('//div[@class="ytv-promo-drawer-additional-description"][contains(., "additional fee")]'):
            package['name'] = 'Add-On'
        else:
            package['name'] = 'Base'

        yield ChannelItem(name=response.meta['name'], package=package)

