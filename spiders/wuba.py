from .base_spider import BaseSpider
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re


class WubaSpider(BaseSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.search_url = f"{self.base_url}/ershoufang"

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        district_mapping = {
            "吉阳区": "jiyangqu",
            "天涯区": "tianyaqu"
        }
        district_pinyin = district_mapping.get(district, "")
        if not district_pinyin:
            print(f"[58同城] 未找到区域 {district} 的映射")
            return houses

        url = f"{self.search_url}/{district_pinyin}/pn{page}/"
        print(f"[58同城] 正在爬取: {url}")

        soup = self.get_page(url)
        if not soup:
            return houses

        house_items = soup.select('li.house-cell') or soup.select('div.house-list li')

        for item in house_items:
            try:
                house = self._parse_house_item(item, district)
                if house:
                    houses.append(house)
            except Exception as e:
                print(f"[58同城] 解析房源失败: {e}")
                continue

        return houses

    def _parse_house_item(self, item, district: str) -> Optional[Dict]:
        try:
            title_elem = item.select_one('h2.title a') or item.select_one('a.t')
            if not title_elem:
                return None

            title = self.clean_text(title_elem.text)
            house_url = title_elem.get('href', '')
            if house_url and not house_url.startswith('http'):
                house_url = 'https:' + house_url

            details_elem = item.select_one('p.baseinfo') or item.select_one('div.room')
            details = self.clean_text(details_elem.text) if details_elem else ""

            price_elem = item.select_one('span.price') or item.select_one('strong.price')
            price_text = price_elem.text if price_elem else "0"
            price = self.parse_price(price_text)

            unit_price_elem = item.select_one('span.unit-price')
            unit_price = self.clean_text(unit_price_elem.text) if unit_price_elem else ""

            address_elem = item.select_one('p.address') or item.select_one('span.address')
            address = self.clean_text(address_elem.text) if address_elem else ""

            tag_elems = item.select('span.tag') or item.select('span.label')
            tags = [self.clean_text(tag.text) for tag in tag_elems]

            area = None
            layout = ""
            floor = ""
            orientation = ""

            if details:
                parts = re.split(r'[\s|]+', details)
                for part in parts:
                    part = part.strip()
                    if '㎡' in part or '平米' in part:
                        area = self.parse_area(part)
                    elif re.match(r'\d室', part):
                        layout = part
                    elif '层' in part:
                        floor = part
                    elif any(o in part for o in ['东', '南', '西', '北']):
                        orientation = part

            community = ""
            if address:
                addr_parts = re.split(r'[\s\-]+', address)
                if addr_parts:
                    community = addr_parts[0].strip()

            return {
                '标题': title,
                '链接': house_url,
                '区域': district,
                '小区': community,
                '位置': address,
                '户型': layout,
                '面积': area,
                '朝向': orientation,
                '楼层': floor,
                '总价(万)': price,
                '单价': unit_price,
                '关注信息': '',
                '标签': ','.join(tags),
                '来源': '58同城',
                '房源信息': details
            }
        except Exception as e:
            print(f"[58同城] 解析房源项失败: {e}")
            return None

    def get_house_detail(self, house_url: str) -> Dict:
        detail = {}
        soup = self.get_page(house_url)
        if not soup:
            return detail

        try:
            info_items = soup.select('ul.house-info li') or soup.select('div.house-detail li')
            for item in info_items:
                text = self.clean_text(item.text)
                if '：' in text or ':' in text:
                    key, value = re.split('[：:]', text, 1)
                    detail[key.strip()] = value.strip()

            intro_elem = soup.select_one('div.house-desc') or soup.select_one('div.description')
            if intro_elem:
                detail['房源介绍'] = self.clean_text(intro_elem.text)

            img_elems = soup.select('div.house-pic img') or soup.select('div.img-box img')
            detail['图片链接'] = ','.join([img.get('src', '') for img in img_elems[:5]])

        except Exception as e:
            print(f"[58同城] 获取详情失败: {e}")

        return detail
