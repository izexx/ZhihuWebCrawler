# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import ZhihuSpiderItem
import time

class ImageSpider(scrapy.Spider):
    count = 0
    name = 'zhihu'
    start_urls = ['https://www.zhihu.com/people/excited-vczh/activities']
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Referer": "https://www.zhihu.com/search?type=content&q=vczh"
    }
    cookies = {
        '__utma': "51854390.1745411408.1553844546.1568265843.1568447484.3",
        '__utmv': "51854390.100--|2=registration_date=20190731=1^3=entry_date=20190118=1",
        '__utmz': "51854390.1568447484.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/21414417",
        '_zap': "a2ee6fd3-1908-44bb-bb9f-1da96f8ef3ff",
        '_xsrf': "egkghxdLBNgHzm3k70GLfUG8ziR0NWg3",
        'capsion_ticket':"2|1:0|10:1568442868|14:capsion_ticket|44:ODM3NzY3NWQ0MmJkNDkwYzhhNTgxMjFiNjhkOGYzNGQ=|46334e49db0d88af6444418850ca581467f3e51c5596c301d13c1195f2ae2ae4",
        'z_c0': "2|1:0|10:1568442878|4:z_c0|92:Mi4xdjQ1U0VRQUFBQUFBNEtQakVFN1JEaVlBQUFCZ0FsVk5fdGRwWGdCdzdzRUZsTzdjaHFjTTJueHdhWXN1TmlzWnpB|8ce8764ddea5c0ed836eaf7bcc60c379bb7510d19b14e26baa60054484911d96",
    }
    scroll_header = {
        "Referer": "https://www.zhihu.com/people/excited-vczh/activities",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Host": "www.zhihu.com",
        "Content-Type": "application/x-protobuf",
        "x-requested-with": "fetch"
        }
    scroll_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/activities?limit=7&session_id=1067720421109129216'
    pattern = r'https://pic[1-2].zhimg.com/v2-[0-9a-z]*?_r.jpg'
    url_list = []
    tags = {20013528, 19571869, 19566151, 19556945, 19552223, 19616599, 19552207, 19641262,
            19554539, 19559956, 19561847, 19669747, 19574208, 19612196, 19792298, 19584431,
            19561625, 19575990, 19564412, 19565769, 19552207}
    words = ["女性", "漂亮", "美丽", "身材", "胸", "蹆", "化妆", "可爱", "性感", "美女", "姑娘", "女生", "裙子", "颜值",
             "择偶", "相亲", "妹子", "小姐姐"]

    def start_requests(self):
        # 首先是登陆页面
        return [
            # scrapy.http.Request('https://www.zhihu.com/people/excited-vczh/activities', headers=self.headers),
            scrapy.http.Request(self.scroll_url, headers=self.headers)]

    def parse(self, response):
        try:
            js_obj = json.loads(response.body)
            next_url = js_obj['paging']['next']
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse)
            for i in js_obj['data']:
                if 'gender' in i['target']['author'].keys() and i['target']['author']['gender'] == 0:
                        #and 'question' in i['target'].keys() \
                        #and not set(i['target']['question']['bound_topic_ids']).isdisjoint(self.tags):
                        for word in self.words:
                            if 'question' in i['target'].keys() and word in i['target']['question']['title']:
                                item = ZhihuSpiderItem()
                                item['image_urls'] = re.findall(self.pattern, i['target']['content'])
                                yield item
                                break
            self.log('continue scroll:--' + next_url)
        except json.decoder.JSONDecodeError:
            self.log('--JSON解析失败')



