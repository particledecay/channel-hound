# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel_hound.settings')
import django
django.setup()

from scrapy.exporters import JsonItemExporter

from services.models import Channel, Package, Service


class JsonPipeline(object):

    def __init__(self):
        self.file = open('channels.json', 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class DatabasePipeline(object):

    def process_item(self, item, spider):
        existing_svc = Service.objects.filter(name__iexact=item['package']['service'])
        if existing_svc:
            svc = existing_svc[0]
        else:
            svc = Service(name=item['package']['service'])
            svc.save()

        existing_pkg = Package.objects.filter(name__iexact=item['package']['name'],
                                              service=svc)
        if existing_pkg:
            pkg = existing_pkg[0]
        else:
            pkg = Package(name=item['package']['name'], price=item['package']['price'])
            pkg.service = svc
            pkg.save()

        existing_chn = Channel.objects.filter(name__iexact=item['name'])
        if existing_chn:
            chn = existing_chn[0]
        else:
            chn = Channel(name=item['name'])
            chn.save()
        chn.packages.add(pkg)

        return item