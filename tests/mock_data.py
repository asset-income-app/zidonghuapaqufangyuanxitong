"""
模拟数据生成器 - 用于测试系统功能
"""
import pandas as pd
import random
from datetime import datetime
from typing import Dict, List


class MockDataGenerator:
    def __init__(self):
        self.districts = ['吉阳区', '天涯区']
        self.communities = {
            '吉阳区': ['三亚湾红树林', '海棠湾一号', '亚龙湾公主郡', '吉阳小区', '三亚国际免税城'],
            '天涯区': ['天涯海角花园', '西岛渔村', '天涯小镇', '马岭社区', '三亚湾花园']
        }
        self.layouts = ['1室1厅', '2室1厅', '2室2厅', '3室1厅', '3室2厅', '4室2厅']
        self.orientations = ['东', '南', '西', '北', '东南', '西南', '东北', '西北', '南北']
        self.floors = ['低层', '中层', '高层']
        self.tags = ['海景房', '学区房', '地铁房', '精装修', '急售', '满五唯一', '近海', '花园小区']
        self.sources = ['链家', '安居客', '58同城', '贝壳']

    def generate_house(self, district: str = None) -> Dict:
        if not district:
            district = random.choice(self.districts)

        community = random.choice(self.communities[district])
        layout = random.choice(self.layouts)
        area = random.randint(50, 200)
        base_price_per_sqm = random.randint(15000, 35000)
        total_price = round(area * base_price_per_sqm / 10000, 1)

        house = {
            '标题': f"{community} {layout} {area}平米",
            '链接': f"https://example.com/house/{random.randint(100000, 999999)}",
            '区域': district,
            '小区': community,
            '位置': f"{district}-{community}",
            '户型': layout,
            '面积': area,
            '朝向': random.choice(self.orientations),
            '楼层': f"{random.randint(1, 30)}层/{random.choice(self.floors)}",
            '总价(万)': total_price,
            '单价': f"{base_price_per_sqm}元/平米",
            '标签': '|'.join(random.sample(self.tags, random.randint(1, 3))),
            '来源': random.choice(self.sources),
            '房源信息': f"{layout} | {area}平米 | {random.choice(self.orientations)}",
            '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return house

    def generate_houses(self, count: int = 100, district: str = None) -> List[Dict]:
        houses = []
        for _ in range(count):
            house = self.generate_house(district)
            houses.append(house)
        return houses

    def generate_dataframe(self, count: int = 100) -> pd.DataFrame:
        houses = self.generate_houses(count)
        df = pd.DataFrame(houses)
        return df


def run_with_mock_data():
    print("\n" + "="*60)
    print("使用模拟数据测试系统")
    print("="*60)

    from core.processor import DataProcessor
    from core.exporter import Exporter
    from core.database import Database
    from utils.config_manager import ConfigManager

    config_manager = ConfigManager()
    config = {
        'price_range': config_manager.get('price_range'),
        'districts': config_manager.get('districts')
    }

    print("\n[1/5] 生成模拟数据...")
    generator = MockDataGenerator()
    houses = generator.generate_houses(100)
    print(f"  已生成 {len(houses)} 条模拟数据")

    print("\n[2/5] 处理数据...")
    processor = DataProcessor(config)
    df = processor.process_houses(houses)
    print(f"  处理后数据: {len(df)} 条")

    print("\n[3/5] 计算统计数据...")
    stats = {
        '总房源数': len(df),
        '平均总价(万)': df['总价(万)'].mean() if '总价(万)' in df.columns else 0,
        '最低总价(万)': df['总价(万)'].min() if '总价(万)' in df.columns else 0,
        '最高总价(万)': df['总价(万)'].max() if '总价(万)' in df.columns else 0,
        '平均面积(㎡)': df['面积'].mean() if '面积' in df.columns else 0,
        '各区域房源数': df['区域'].value_counts().to_dict() if '区域' in df.columns else {},
        '各网站房源数': df['来源'].value_counts().to_dict() if '来源' in df.columns else {}
    }
    print(f"  平均价格: {stats['平均总价(万)']:.2f} 万元")
    print(f"  价格范围: {stats['最低总价(万)']:.2f} - {stats['最高总价(万)']:.2f} 万元")

    print("\n[4/5] 导出数据...")
    exporter = Exporter('output')
    files = exporter.export_all(df, stats)
    print(f"  已导出 {len(files)} 个文件")

    print("\n[5/5] 保存到数据库...")
    db = Database()
    count = db.insert_houses_batch(houses)
    print(f"  已保存 {count} 条数据到数据库")

    print("\n" + "="*60)
    print("模拟数据测试完成！")
    print("="*60)
    print("\n您现在可以:")
    print("  1. 在 output/ 目录查看导出的文件")
    print("  2. 启动Web界面查看数据")
    print("  3. 使用数据库查询功能")

    return {
        'dataframe': df,
        'statistics': stats,
        'files': files
    }


if __name__ == "__main__":
    import sys
    import io
    import os

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    result = run_with_mock_data()
    print(f"\n测试成功！共处理 {len(result['dataframe'])} 条数据")
