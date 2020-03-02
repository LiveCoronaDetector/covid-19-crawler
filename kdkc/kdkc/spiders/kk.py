# -*- coding: utf-8 -*-
import scrapy
from ..items import KdkcItems


class KkSpider(scrapy.Spider):
    name = 'kk'
    allowed_domains = ['http://ncov.mohw.go.kr']
    start_urls = ['http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=']

    def parse(self, response):
        item = KdkcItems()
        # 지역
        item['region'] = response.css('th[scope=row]::text').getall()
        # 확진환자 증감
        item['increasing'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[1]/text()').getall()
        # 확진환자 총계
        item['cc_sum'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[2]/text()').getall()
        # 격리 중 환자
        item['isolating'] =  response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[3]/text()').getall()
        # 완치자
        item['recovered'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[4]/text()').getall()
        # 사망자
        item['dead'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[5]/text()').getall()
        # 검사 총계
        item['ch_sum'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[6]/text()').getall()
        # 검사 중
        item['ch_examined'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[7]/text()').getall()
        # 결과 음성
        item['ch_negative'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[8]/text()').getall()
        # 총계
        item['total'] = response.xpath('//div[@id="content"]/div/div[4]/table/tbody/tr/td[9]/text()').getall()
        yield item

