from .base_spider import BaseSpider
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re


class LianjiaSpider(BaseSpider):
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
            print(f"[链家] 未找到区域 {district} 的映射")
            return houses

        url = f"{self.search_url}/{district_pinyin}/pg{page}"
        print(f"[链家] 正在爬取: {url}")

        soup = self.get_page(url)
        if not soup:
            return houses

        house_items = soup.select('ul.sellListContent li.clear')
        if not house_items:
            house_items = soup.select('div.leftContent ul.sellListContent li')

        for item in house_items:
            try:
                house = self._parse_house_item(item, district)
                if house:
                    houses.append(house)
            except Exception as e:
                print(f"[链家] 解析房源失败: {e}")
                continue

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

            follow_elem = item.select_one('div.followInfo')
            follow_info = self.clean_text(follow_elem.text) if follow_elem else ""

            tag_elems = item.select('div.tag span')
            tags = [self.clean_text(tag.text) for tag in tag_elems]

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

            return {
                '标题': title,
                '链接': house_url,
                '区域': district,
                '小区': position.split('-')[0] if '-' in position else position,
                '位置': position,
                '户型': layout,
                '面积': area,
                '朝向': orientation,
                '楼层': floor,
                '总价(万)': price,
                '单价': unit_price,
                '关注信息': follow_info,
                '标签': ','.join(tags),
                '来源': '链家网',
                '房源信息': house_info
            }
        except Exception as e:
            print(f"[链家] 解析房源项失败: {e}")
            return None

    def get_house_detail(self, house_url: str) -> Dict:
        detail = {}
        soup = self.get_page(house_url)
        if not soup:
            return detail

        try:
            intro_elem = soup.select_one('div.introContent')
            if intro_elem:
                detail['房源介绍'] = self.clean_text(intro_elem.text)

            base_info = soup.select('div.base li')
            for info in base_info:
                text = self.clean_text(info.text)
                if '：' in text or ':' in text:
                    key, value = re.split('[：:]', text, 1)
                    detail[key.strip()] = value.strip()

            transaction_info = soup.select('div.transaction li')
            for info in transaction_info:
                text = self.clean_text(info.text)
                if '：' in text or ':' in text:
                    key, value = re.split('[：:]', text, 1)
                    detail[key.strip()] = value.strip()

            img_elems = soup.select('div.imgList img')
            detail['图片链接'] = ','.join([img.get('src', '') for img in img_elems[:5]])

        except Exception as e:
            print(f"[链家] 获取详情失败: {e}")

        return detail
