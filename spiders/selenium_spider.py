from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Dict, Optional
import time
import random
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumSpider:
    def __init__(self, config: Dict):
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.driver = None
        self.wait_timeout = config.get('timeout', 30)
        self.delay = config.get('delay', 2)
        
    def init_driver(self):
        if self.driver:
            return
            
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            print(f"[{self.name}] Chrome驱动初始化成功")
        except Exception as e:
            print(f"[{self.name}] Chrome驱动初始化失败: {e}")
            raise

    def get_page(self, url: str) -> bool:
        if not self.driver:
            self.init_driver()
        
        try:
            print(f"[{self.name}] 正在访问: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(self.delay, self.delay + 1))
            return True
        except Exception as e:
            print(f"[{self.name}] 访问页面失败: {e}")
            return False

    def wait_for_element(self, by: By, value: str, timeout: int = None) -> Optional[object]:
        if not timeout:
            timeout = self.wait_timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"[{self.name}] 等待元素超时: {value}")
            return None

    def find_elements(self, by: By, value: str) -> List:
        try:
            return self.driver.find_elements(by, value)
        except NoSuchElementException:
            return []

    def find_element(self, by: By, value: str) -> Optional[object]:
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None

    def execute_script(self, script: str):
        return self.driver.execute_script(script)

    def scroll_page(self, times: int = 3):
        for i in range(times):
            self.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{times} * {i+1});")
            time.sleep(0.5)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __del__(self):
        self.close()
