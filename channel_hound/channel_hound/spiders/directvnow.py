# -*- coding: utf-8 -*-
import scrapy

from channel_hound.items import ChannelItem


class DirectvnowSpider(scrapy.Spider):
    name = 'directvnow'
    allowed_domains = ['directvnow.com', 'directv.com']
    start_urls = [
        'https://cdn.directv.com/content/dam/dtv/prod/website_directvnow/modals/compare-packages-dbs.html'
    ]
    service = 'DIRECTV NOW'

    def parse(self, response):
        packages = self.get_packages(response)

        for channel in self.get_channels(response, packages):
            yield channel

    def get_packages(self, response):
        package_elements = response.xpath('//div[contains(@class, "header")]//div[contains(@class, "col-custom")]')
        packages = []

        for package_element in package_elements:
            package = {'service': DirectvnowSpider.service}
            package['name'] = package_element.xpath('.//div[@class="title"]//text()').extract()[0]
            package['price'] = package_element.xpath('.//div[@class="price"]//text()').extract()[0]
            packages.append(package)

        return packages

    def get_channels(self, response, packages):
        channel_elements = response.xpath('//div[contains(@class, "channel")]')
        channels = []

        for channel_element in channel_elements:
            title = self.get_channel_title(channel_element)
            for idx, availability in enumerate(channel_element.xpath('.//div[contains(@class, "col-custom")]')):
                if availability.xpath('./span[@class="checked"]'):
                    channels.append(ChannelItem(name=title, package=packages[idx]))

        return channels

    def get_channel_title(self, channel_element):
        title_elements = channel_element.xpath('.//div[contains(@class, "ch--title")]//text()').extract()
        stripped_titles =  filter(lambda title: title, map(lambda txt: txt.strip(), title_elements))
        return ''.join(stripped_titles)
