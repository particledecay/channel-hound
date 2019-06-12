# -*- coding: utf-8 -*-
import json

import scrapy

from channel_hound.items import ChannelItem


class PsvueSpider(scrapy.Spider):
    name = 'psvue'
    allowed_domains = ['playstation.com']
    start_urls = [
        'https://vue.api.playstation.com/v1/channels/channelEntitlement?imageType=medium&zipCode=33076',
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        for package_obj in jsonresponse['subscriptions']:
            package = {'service': 'Playstation Vue', 'name': package_obj['entitlementName'],
                       'price': package_obj['regularPrice']}
            for channel in package_obj['channels']:
                yield ChannelItem(name=channel['name'], package=package)