# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KdkcItems(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #지역
    region = scrapy.Field()
    # 확진환자 증감
    increasing = scrapy.Field()
    # 확진환자 총계
    cc_sum = scrapy.Field()
    # 격리 중 환자
    isolating = scrapy.Field()
    # 완치자
    recovered = scrapy.Field()
    # 사망자
    dead = scrapy.Field()
    # 검사 총계
    ch_sum = scrapy.Field()
    # 검사 중
    ch_examined = scrapy.Field()
    # 결과 음성
    ch_negative = scrapy.Field()
    # 총계 
    total = scrapy.Field()
