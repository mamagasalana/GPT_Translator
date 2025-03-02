from novel import NOVEL
import re
import os
import time
class FILE_HANDLER:
    def __init__(self, url='https://ncode.syosetu.com/n6169dz/'):
        self.url = url
        novel_code = re.split(r'/', url)
        self.novel_code = [x for x in novel_code if x][-1]
        if not os.path.isdir(self.novel_code):
            os.mkdir(self.novel_code)

        print('debg')
    def main2(self, page):
        n = NOVEL(max_page=939, url=self.url,page=page)
        start_page = page
        for data in n.iter_page(max_length=1e13):
            page = data['page']
            txt = data['data']  
            if page > start_page+19:
                start_page = page

            with open('%s/%s-%s.txt' % (self.novel_code, start_page, start_page+19) , 'a', encoding='utf-8') as ofile:        
                ofile.write('##################################################################\n')
                ofile.write('Chapter %s\n' % page)
                ofile.write('##################################################################\n')
                ofile.write(txt)
                ofile.flush()
        
                time.sleep(1)
                

if __name__ == '__main__':
    fh =FILE_HANDLER()
    fh.main2(78)