# -*- coding: utf-8 -*-
import scrapy

from channel_hound.items import ChannelItem


class PhiloSpider(scrapy.Spider):
    name = 'philo'
    allowed_domains = ['philo.com']
    start_urls = ['https://help.philo.com/hc/en-us/articles/360006214074-Channel-lineup']
    service = 'Philo'

    def parse(self, response):
        package = {'name': 'Base', 'service': PhiloSpider.service}

        channel_container = response.xpath('//div[@class="channels"]')
        package['price'] = channel_container.xpath('substring-before(substring-after(./h5[@class="channels-head"]/text(), "$"), "/")').extract()[0]

        channel_elements = channel_container.xpath('./div[@class="channels-list"]/div[@class="channel-logo"]')
        for channel_element in channel_elements:
            name = channel_element.xpath('./img/@title').extract()[0]
            yield ChannelItem(name=name, package=package)
