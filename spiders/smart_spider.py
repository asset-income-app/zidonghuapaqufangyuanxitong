"""
智能爬虫系统 - 自动检测网络并选择可用网站
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time
import random
import socket


class SmartSpider:
    def __init__(self, config: Dict):
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.session = requests.Session()
        self.delay = config.get('delay', 2)
        self.timeout = config.get('timeout', 10)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })

    def check_network(self, url: str) -> bool:
        try:
            domain = url.split('/')[2]
            socket.gethostbyname(domain)
            return True
        except:
            return False

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        if not self.check_network(url):
            print(f"[{self.name}] 网络无法访问: {url}")
            return None
        
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
            print(f"[{self.name}] 请求失败: {str(e)[:50]}")
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


class FangSpider(SmartSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = '房天下'
        self.base_url = 'https://sanya.esf.fang.com'

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        
        district_mapping = {
            "吉阳区": "jiyang",
            "天涯区": "tianya"
        }
        
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            return houses

        url = f"{self.base_url}/house-{district_pinyin}/c2500__pg_{page}/"
        
        soup = self.get_page(url)
        if not soup:
            return houses

        try:
            items = soup.select('div.houseList div.list')
            
            if items:
                print(f"[{self.name}] 找到 {len(items)} 个房源")

            for item in items:
                try:
                    house = self._parse_house_item(item, district)
                    if house and house.get('标题'):
                        houses.append(house)
                except:
                    continue

        except Exception as e:
            print(f"[{self.name}] 解析失败: {e}")
        
        return houses

    def _parse_house_item(self, item, district: str) -> Optional[Dict]:
        try:
            title_elem = item.select_one('p.title a')
            if not title_elem:
                return None
            
            title = self.clean_text(title_elem.text)
            house_url = title_elem.get('href', '')

            price_elem = item.select_one('p.price span')
            price_text = price_elem.text if price_elem else "0"
            price = self.parse_price(price_text)

            info_elem = item.select_one('p.room')
            info = self.clean_text(info_elem.text) if info_elem else ""

            area = None
            layout = ""
            
            if info:
                parts = info.split('|')
                for part in parts:
                    part = part.strip()
                    if '平米' in part or '㎡' in part:
                        area = self.parse_area(part)
                    elif re.match(r'\d室', part):
                        layout = part

            return {
                '标题': title,
                '链接': house_url,
                '区域': district,
                '小区': '',
                '位置': district,
                '户型': layout,
                '面积': area,
                '朝向': '',
                '楼层': '',
                '总价(万)': price,
                '单价': '',
                '标签': '',
                '来源': '房天下',
                '房源信息': info
            }

        except:
            return None


class KeSpider(SmartSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = '贝壳找房'
        self.base_url = 'https://sy.ke.com'

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        
        district_mapping = {
            "吉阳区": "jiyang",
            "天涯区": "tianya"
        }
        
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            return houses

        url = f"{self.base_url}/ershoufang/{district_pinyin}/pg{page}/"
        
        soup = self.get_page(url)
        if not soup:
            return houses

        try:
            items = soup.select('ul.sellListContent li.clear')
            
            if items:
                print(f"[{self.name}] 找到 {len(items)} 个房源")

            for item in items:
                try:
                    house = self._parse_house_item(item, district)
                    if house and house.get('标题'):
                        houses.append(house)
                except:
                    continue

        except Exception as e:
            print(f"[{self.name}] 解析失败: {e}")
        
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
                '来源': '贝壳',
                '房源信息': house_info
            }

        except:
            return None
