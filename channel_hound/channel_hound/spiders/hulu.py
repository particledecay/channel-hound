# -*- coding: utf-8 -*-
import scrapy

from channel_hound.items import ChannelItem


class HuluSpider(scrapy.Spider):
    name = 'hulu'
    allowed_domains = ['hulu.com']
    start_urls = ['http://hulu.com/live-tv']
    service = 'Hulu w/ Live TV'

    def parse(self, response):
        network_list = response.xpath('//div[@id="channels"]/following-sibling::div//div[@class="network-list"]/img')
        package = {'service': HuluSpider.service, 'name': 'Base', 'price': '44.99'}
        for channel in network_list:
            name = channel.xpath('./@alt').extract()[0]
            yield ChannelItem(name=name, package=package)