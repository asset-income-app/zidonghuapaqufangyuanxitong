import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time
import random


class SimpleSpider:
    def __init__(self, config: Dict):
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.base_url = config.get('base_url', '')
        self.session = requests.Session()
        self.delay = config.get('delay', 2)
        self.timeout = config.get('timeout', 30)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            print(f"[{self.name}] 正在访问: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.encoding = response.apparent_encoding
            
            if response.status_code == 200:
                time.sleep(random.uniform(self.delay, self.delay + 1))
                return BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"[{self.name}] HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"[{self.name}] 请求失败: {e}")
            return None

    def parse_price(self, price_str: str) -> Optional[float]:
        if not price_str:
            return None
        try:
            price_str = re.sub(r'[^\d.]', '', str(price_str))
            return float(price_str) if price_str else None
        except:
            return None

    def parse_area(self, area_str: str) -> Optional[float]:
        if not area_str:
            return None
        try:
            area_str = re.sub(r'[^\d.]', '', str(area_str))
            return float(area_str) if area_str else None
        except:
            return None

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        return text.strip().replace('\n', '').replace('\r', '').replace('\t', '')


class LianjiaSimpleSpider(SimpleSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = '链家网'
        self.base_url = config.get('base_url', 'https://sanya.lianjia.com')

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        
        district_mapping = {
            "吉阳区": "jiyang",
            "天涯区": "tianya"
        }
        
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            print(f"[链家] 未找到区域映射: {district}")
            return houses

        url = f"{self.base_url}/ershoufang/{district_pinyin}/pg{page}/"
        
        soup = self.get_page(url)
        if not soup:
            return houses

        try:
            items = soup.select('ul.sellListContent li.clear')
            
            if not items:
                items = soup.select('div.leftContent ul.sellListContent li')
            
            print(f"[链家] 找到 {len(items)} 个房源元素")

            for item in items:
                try:
                    house = self._parse_house_item(item, district)
                    if house and house.get('标题'):
                        houses.append(house)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[链家] 解析失败: {e}")
        
        return houses

    def _parse_house_item(self, item, district: str) -> Optional[Dict]:
        try:
            title_elem = item.select_one('div.title a')
            if not title_elem:
                return None
            
            title = self.clean_text(title_elem.text)
            house_url = title_elem.get('href', '')

            position_elem = item.select_one('div.positionInfo')
            position = self.clean_text(position_elem.text) if position_elem else ""

            house_info_elem = item.select_one('div.houseInfo')
            house_info = self.clean_text(house_info_elem.text) if house_info_elem else ""

            price_elem = item.select_one('div.totalPrice span')
            price_text = price_elem.text if price_elem else "0"
            price = self.parse_price(price_text)

            unit_price_elem = item.select_one('div.unitPrice span')
            unit_price = self.clean_text(unit_price_elem.text) if unit_price_elem else ""

            area = None
            layout = ""
            floor = ""
            orientation = ""
            
            if house_info:
                parts = house_info.split('|')
                for part in parts:
                    part = part.strip()
                    if '平米' in part or '㎡' in part:
                        area = self.parse_area(part)
                    elif re.match(r'\d室', part):
                        layout = part
                    elif '层' in part:
                        floor = part
                    elif any(o in part for o in ['东', '南', '西', '北']):
                        orientation = part

            community = position.split('-')[0].strip() if '-' in position else position

            return {
                '标题': title,
                '链接': house_url,
                '区域': district,
                '小区': community,
                '位置': position,
                '户型': layout,
                '面积': area,
                '朝向': orientation,
                '楼层': floor,
                '总价(万)': price,
                '单价': unit_price,
                '标签': '',
                '来源': '链家',
                '房源信息': house_info
            }

        except Exception as e:
            return None

    def get_house_detail(self, house_url: str) -> Dict:
        return {}


class AnjukeSimpleSpider(SimpleSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = '安居客'
        self.base_url = config.get('base_url', 'https://sanya.anjuke.com')

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        
        district_mapping = {
            "吉阳区": "jiyang",
            "天涯区": "tianya"
        }
        
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            print(f"[安居客] 未找到区域映射: {district}")
            return houses

        url = f"{self.base_url}/sale/{district_pinyin}/p{page}/"
        
        soup = self.get_page(url)
        if not soup:
            return houses

        try:
            items = soup.select('div.house-list div.list-item')
            
            print(f"[安居客] 找到 {len(items)} 个房源元素")

            for item in items:
                try:
                    house = self._parse_house_item(item, district)
                    if house and house.get('标题'):
                        houses.append(house)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"[安居客] 解析失败: {e}")
        
        return houses

    def _parse_house_item(self, item, district: str) -> Optional[Dict]:
        try:
            title_elem = item.select_one('div.house-title a')
            if not title_elem:
                return None
            
            title = self.clean_text(title_elem.text)
            house_url = title_elem.get('href', '')

            details_elem = item.select_one('div.details-item')
            details = self.clean_text(details_elem.text) if details_elem else ""

            price_elem = item.select_one('span.price-det')
            price_text = price_elem.text if price_elem else "0"
            price = self.parse_price(price_text)

            area = None
            layout = ""
            floor = ""
            
            if details:
                parts = details.split('|')
                for part in parts:
                    part = part.strip()
                    if '平米' in part or '㎡' in part:
                        area = self.parse_area(part)
                    elif re.match(r'\d室', part):
                        layout = part
                    elif '层' in part:
                        floor = part

            return {
                '标题': title,
                '链接': house_url,
                '区域': district,
                '小区': '',
                '位置': district,
                '户型': layout,
                '面积': area,
                '朝向': '',
                '楼层': floor,
                '总价(万)': price,
                '单价': '',
                '标签': '',
                '来源': '安居客',
                '房源信息': details
            }

        except Exception as e:
            return None

    def get_house_detail(self, house_url: str) -> Dict:
        return {}
