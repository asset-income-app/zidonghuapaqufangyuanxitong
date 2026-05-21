from .selenium_spider import SeleniumSpider
from typing import List, Dict, Optional
import re


class LianjiaSeleniumSpider(SeleniumSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.base_url = config.get('base_url', 'https://sanya.lianjia.com')
        self.name = '链家网'

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        
        district_mapping = {
            "吉阳区": "jiyang",
            "天涯区": "tianya"
        }
        
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            print(f"[链家] 未找到区域 {district} 的映射")
            return houses

        url = f"{self.base_url}/ershoufang/{district_pinyin}/pg{page}/"
        
        if not self.get_page(url):
            return houses

        try:
            self.wait_for_element(By.CSS_SELECTOR, 'ul.sellListContent', timeout=10)
            
            items = self.find_elements(By.CSS_SELECTOR, 'ul.sellListContent li.clear')
            
            if not items:
                items = self.find_elements(By.CSS_SELECTOR, 'div.leftContent ul.sellListContent li')
            
            print(f"[链家] 找到 {len(items)} 个房源元素")

            for item in items:
                try:
                    house = self._parse_house_item(item, district)
                    if house:
                        houses.append(house)
                except Exception as e:
                    print(f"[链家] 解析房源失败: {e}")
                    continue

        except Exception as e:
            print(f"[链家] 解析页面失败: {e}")
        
        return houses

    def _parse_house_item(self, item, district: str) -> Optional[Dict]:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, 'div.title a')
            title = title_elem.text.strip()
            house_url = title_elem.get_attribute('href')

            position_elem = item.find_element(By.CSS_SELECTOR, 'div.positionInfo')
            position = position_elem.text.strip()

            house_info_elem = item.find_element(By.CSS_SELECTOR, 'div.houseInfo')
            house_info = house_info_elem.text.strip()

            price_elem = item.find_element(By.CSS_SELECTOR, 'div.totalPrice span')
            price_text = price_elem.text.strip()
            price = self.parse_price(price_text)

            unit_price_elem = item.find_element(By.CSS_SELECTOR, 'div.unitPrice span')
            unit_price = unit_price_elem.text.strip()

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

    def parse_price(self, price_str: str) -> Optional[float]:
        if not price_str:
            return None
        try:
            price_str = re.sub(r'[^\d.]', '', price_str)
            return float(price_str) if price_str else None
        except:
            return None

    def parse_area(self, area_str: str) -> Optional[float]:
        if not area_str:
            return None
        try:
            area_str = re.sub(r'[^\d.]', '', area_str)
            return float(area_str) if area_str else None
        except:
            return None

    def get_house_detail(self, house_url: str) -> Dict:
        return {}
