from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent


class BaseSpider(ABC):
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = config.get('base_url', '')
        self.name = config.get('name', 'Unknown')
        self.session = requests.Session()
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.delay = config.get('delay', 2)
        self.timeout = config.get('timeout', 30)
        self.retry_times = config.get('retry_times', 3)

    def get_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        for attempt in range(self.retry_times):
            try:
                self.headers['User-Agent'] = self.ua.random
                response = self.session.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                time.sleep(random.uniform(self.delay, self.delay + 1))
                return BeautifulSoup(response.text, 'lxml')
            except Exception as e:
                print(f"[{self.name}] 第{attempt + 1}次请求失败: {url}, 错误: {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.delay * 2)
        return None

    def post_page(self, url: str, data: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        for attempt in range(self.retry_times):
            try:
                self.headers['User-Agent'] = self.ua.random
                response = self.session.post(
                    url,
                    headers=self.headers,
                    data=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                time.sleep(random.uniform(self.delay, self.delay + 1))
                return BeautifulSoup(response.text, 'lxml')
            except Exception as e:
                print(f"[{self.name}] 第{attempt + 1}次POST请求失败: {url}, 错误: {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.delay * 2)
        return None

    @abstractmethod
    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        pass

    @abstractmethod
    def get_house_detail(self, house_url: str) -> Dict:
        pass

    def parse_price(self, price_str: str) -> Optional[float]:
        if not price_str:
            return None
        try:
            price_str = price_str.replace('万', '').replace('元', '').replace(',', '').strip()
            return float(price_str)
        except:
            return None

    def parse_area(self, area_str: str) -> Optional[float]:
        if not area_str:
            return None
        try:
            area_str = area_str.replace('平米', '').replace('㎡', '').replace('m²', '').strip()
            return float(area_str)
        except:
            return None

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        return text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
