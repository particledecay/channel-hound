# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy.http import Request

from channel_hound.items import ChannelItem


class SlingSpider(scrapy.Spider):
    name = 'sling'
    allowed_domains = ['sling.com']
    start_urls = ['https://sling.com']
    translated_package_names = {
        'domestic': 'SLING ORANGE',
        'sling-mss': 'SLING BLUE',
        'sling-combo': 'ORANGE & BLUE',
    }

    def __init__(self, *args, **kwargs):
        self.regex_package = re.compile(r'PackageId=([^\.]+)')
        self._urls = [
            'https://www.sling.com/bin/getdynamicchannels.classification=us.planId=one-week-promo.PackageId=domestic.channelLogoPath=_content_dam_sling-tv_channels_AllLOBLogos_Color.html',
            'https://www.sling.com/bin/getdynamicchannels.classification=us.planId=one-week-promo.PackageId=sling-mss.channelLogoPath=_content_dam_sling-tv_channels_AllLOBLogos_Color.html',
            'https://www.sling.com/bin/getdynamicchannels.classification=us.planId=one-week-promo.PackageId=sling-combo.channelLogoPath=_content_dam_sling-tv_channels_AllLOBLogos_Color.html',
        ]
        super().__init__(*args, **kwargs)

    def parse(self, response):
        package_prices = {}
        price_elements = response.xpath('//div[contains(@class, "dyn-grid")]//a[contains(@class, "dyn-grid_package-tab")]')
        for price_element in price_elements:
            price = price_element.xpath('./h3/text()').extract()[0]
            plan_name = price_element.xpath('./h6/text()').extract()[0]

            package_prices[plan_name.upper().strip()] = price.replace("$", "")

        for url in self._urls:
            yield Request(url, callback=self.parse_package, meta={'package_prices': package_prices})

    def parse_package(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        matched_package = self.regex_package.search(response.url)
        if not matched_package:
            return

        package_id = matched_package.groups()[0]
        package_name = SlingSpider.translated_package_names[package_id]

        package = {'service': 'Sling', 'name': package_name}
        package['price'] = response.meta['package_prices'][self.translated_package_names[package_id]]

        for channel in jsonresponse:
            yield ChannelItem(name=channel['altText'], package=package)
