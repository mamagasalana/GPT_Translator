import requests
from lxml import html
import logging

logging.basicConfig(
     filename='page.log',
     level=logging.INFO, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
class NOVEL:
    def __init__(self, max_page, url='https://ncode.syosetu.com/n6537fu/', page=1):
        self.url = url
        self.page= page
        self.max_page = max_page
        self.session = requests.session()

    def iter_page(self):
        while self.page <= self.max_page :
            url2 = self.url + str(self.page)
            logging.info(url2)
            r=  self.session.get(url2, headers=HEADERS)
            for content in self.iter_content(r.content):
                if 'error' in content:
                    return
                else:
                    content['page'] = self.page
                    yield content
            self.page+=1

    def iter_content(self, cnt, max_length=1800):
        ret = {'data' : None}
        tree = html.fromstring(cnt)
        if tree.xpath('//h1[text()="エラー"]'):
            ret['error'] = True
            return ret

        x2 = '//div[@class="js-novel-text p-novel__text"]'
        lines = tree.xpath(x2)[0].text_content().split('\n')
        grouped_text = []
        current_group = []
        current_length = 0

        for line in lines:
            line_length = len(line)
            # Check if adding this line would exceed the max length
            if current_length + line_length + len(current_group) > max_length:
                # Save the current group and start a new one
                grouped_text.append("\n".join(current_group))
                current_group = [line]
                current_length = line_length
            else:
                # Add line to the current group
                current_group.append(line)
                current_length += line_length

        # Add the last group if not empty
        if current_group:
            grouped_text.append("\n".join(current_group))

        for g in grouped_text:
            ret['data'] = g
            yield ret

if __name__ =='__main__':
    a = NOVEL()
    for xx in a.iter_page():
        print(xx)


