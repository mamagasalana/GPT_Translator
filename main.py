import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
        while True:
            try:
                elm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, x3)))
                break
            except:
                time.sleep(10)

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
        
    def new_chat(self, txt):
        self.driver.get("https://chatgpt.com/g/g-p-6767cd8419d0819189eaa12acdc44a23-i-parry-everything/project")
        x1 = '//p[@data-placeholder="New chat in this project"]'
        # x1 = '//textarea[@placeholder="New chat in this project"]'
        x2 = '//button[@data-testid="send-button"]'
        
        elm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, x1)))
        for part in txt.split('\n'):
            while True:
                elm.send_keys(part)
                if self.verify_text_sent(part):
                    break
            elm.send_keys(Keys.SHIFT + Keys.ENTER)
            self.ac.reset_actions()
                # if self.verify_text_sent(part):
                #     break

        
        elm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, x2)))
        elm.click()
        

    def resume_chat(self, txt):
        # x1 = '//textarea[@placeholder="Message ChatGPT"]'
        x1 = '//p[@data-placeholder="Message ChatGPT"]'
        x2 = '//button[@data-testid="send-button"]'
        
        elm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, x1)))
        for part in txt.split('\n'):
            elm.send_keys(part)
            elm.send_keys(Keys.SHIFT + Keys.ENTER)
            self.ac.reset_actions()
            # if self.verify_text_sent(part):
            #     break

            
        elm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, x2)))
        elm.click()
        

    def main(self, page):
        n = NOVEL(page=page)
        pages= []
        for data in n.iter_page():
            page = data['page']
            txt = data['data']

            if page not in pages:
                if len(pages) == 4:
                    pages = []
                    return #may have hit gpt limit
                
                if not pages:
                    first = True

                pages.append(page)
            
            if first:
                self.new_chat(txt)
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