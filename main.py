import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from langdetect import detect, detect_langs
from novel import NOVEL
import time
import os

if os.name == 'nt':
# Specify the path to your user profile directory
    USER_DATA_DIR = r"C:\Users\ASUS\Desktop\Research\GPT_Translator\user_data"
else:
    USER_DATA_DIR = r'/home/ytee/test/GPT_Translator/user_data'

class GPT_HANDLER:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")  # Path to the user data directory
        options.add_argument("--profile-directory=Default")      # Use the default profile
                
        # Initialize undetected ChromeDriver
        self.driver = uc.Chrome(options=options)
        self.driver.maximize_window()
        self.ac = ActionChains(self.driver)

    def wait_response_done(self):
        x3 = '//button[@data-testid="composer-speech-button"]|//button[@data-testid="send-button" and @disabled]'
        xret ='//div[@data-message-author-role="assistant"]'
        x2 = '//button[@aria-label="Edit message"]'
        xwhite = '//div[@class="whitespace-pre-wrap"]'
        xgrid = '//div[(contains(@class, "group/conversation")) and (.//div[text()="Send"])]//textarea'
        xsend= '//button[./*[text()="Send"]]'
        xbottom = '//button[contains(@class, "bg-token-main-surface-primary")]'
        xbad = '//button[@aria-label="Bad response"]'

        while True:
            while True:
                try:
                    elm = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, x3)))
                    break
                except:
                    time.sleep(10)

            #verify if mandarin
            try:
                elm = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, xbottom)))
                elm.click()
                time.sleep(1)
            except:
                print("button not found?")
            
            elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xret)))
            elm2 = WebDriverWait(elm[-1], 10).until(EC.presence_of_all_elements_located((By.XPATH, './/p')))
            if not elm2:
                print("no response found?")
                continue

            validation = []
            for elm22 in elm2:
                verify_txt = elm22.text
                if verify_txt:
                    try:
                        lang = detect(verify_txt)
                        validation.append(lang)
                    except:
                        print(verify_txt)
                        pass
                    

            if len(validation) == 0:
                print("no response found2?")
                continue

            score = sum([1 if 'zh' in lang else 0 for lang in validation ] ) / len(validation)
            if score > 0.8:
                return
            else:
                print('not mandarin: %s' % verify_txt)
                elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xbad)))
                if len(elm) < 2:
                    # first sent
                    continue
                self.driver.execute_script("arguments[0].scrollIntoView();", elm[-2])

                elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xwhite)))
                self.ac.move_to_element(elm[-1]).perform()

                elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, x2)))
                elm[-1].click()

                elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xgrid)))
                elm = elm[-1]
                
                part = '请翻译以下成中文：'
                if not part in elm.text:
                    elm.send_keys(Keys.CONTROL + Keys.HOME)
                    self.ac.reset_actions()
                    elm.send_keys(part)
                    elm.send_keys(Keys.SHIFT + Keys.ENTER)
                    self.ac.reset_actions()
                    
                elm = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xsend)))
                elm[-1].click()


    def verify_text_sent(self, part):
        if part:
            x = f'//p[contains(text(), "{part}")]'
            try:
                EC.presence_of_element_located((By.XPATH, x))(self.driver)
                return True
            except:
                return False
        else:
            return True
    
    def send_msg(self):
        x2 = '//button[@data-testid="send-button"]'
        elm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, x2)))
        elm.click()

    def new_chat(self, txt):
        self.driver.get("https://chatgpt.com/g/g-p-67715a83c998819188174385ab9fd445-as-a-reincarnated-aristocrat/project")
        x1 = '//p[@data-placeholder="New chat in this project"]'
        # x1 = '//textarea[@placeholder="New chat in this project"]'
        
        
        elm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, x1)))
        for part in txt.split('\n'):
            while True:
                elm.send_keys(part)
                if self.verify_text_sent(part):
                    break
            elm.send_keys(Keys.SHIFT + Keys.ENTER)
            self.ac.reset_actions()
                # if self.verify_text_sent(part):
                #     break

        self.send_msg()

        

    def resume_chat(self, txt):
        # x1 = '//textarea[@placeholder="Message ChatGPT"]'
        x1 = '//p[@data-placeholder="Message ChatGPT"]'
        
        elm = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, x1)))
        for part in txt.split('\n'):
            elm.send_keys(part)
            elm.send_keys(Keys.SHIFT + Keys.ENTER)
            self.ac.reset_actions()
            # if self.verify_text_sent(part):
            #     break

        self.send_msg()

    def main(self, page):
        max_page = page + 7
        n = NOVEL(url='https://ncode.syosetu.com/n5619fv/',page=page)
        pages= []
        for data in n.iter_page():
            page = data['page']
            txt = data['data']
            if page > max_page:
                return
            
            if page not in pages:
                if len(pages) == 4:
                    pages = []
                    # return #may have hit gpt limit
                
                if not pages:
                    first = True

                pages.append(page)
            
            if first:
                page_info = f'{page} - {page+3}\n\n'
                self.new_chat(page_info+txt)
                first=False
            else:
                self.resume_chat(txt)
            self.wait_response_done()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <page_start>")
        sys.exit(1)
    gpt = GPT_HANDLER()
    page = sys.argv[1]  
    gpt.main(int(page))
    print("Done")