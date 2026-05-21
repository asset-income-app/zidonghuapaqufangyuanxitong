import yaml
import os
from typing import Dict, List
from datetime import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from spiders.simple_spider import LianjiaSimpleSpider, AnjukeSimpleSpider
from core.processor import DataProcessor
from core.exporter import Exporter


class HouseCrawlerEngine:
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self.spiders = self._init_spiders()
        self.processor = DataProcessor(self.config)
        self.exporter = Exporter(
            output_dir=self.config.get('output', {}).get('directory', 'output'),
            filename_prefix=self.config.get('output', {}).get('filename_prefix', '三亚房源')
        )
        self.lock = threading.Lock()
        self.all_houses = []

    def _load_config(self, config_path: str) -> Dict:
        if not os.path.exists(config_path):
            print(f"[错误] 配置文件不存在: {config_path}")
            return {}

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print(f"[配置] 已加载配置文件: {config_path}")
        return config

    def _init_spiders(self) -> List:
        spiders = []
        websites = self.config.get('websites', {})

        spider_classes = {
            'lianjia': LianjiaSimpleSpider,
            'anjuke': AnjukeSimpleSpider,
        }

        crawl_settings = self.config.get('crawl_settings', {})

        for site_key, site_config in websites.items():
            if site_config.get('enabled', False):
                spider_class = spider_classes.get(site_key)
                if spider_class:
                    spider_config = {**site_config, **crawl_settings}
                    spider = spider_class(spider_config)
                    spiders.append(spider)
                    print(f"[初始化] 已加载爬虫: {spider.name}")

        return spiders

    def crawl_single_site(self, spider, district: str, max_pages: int) -> List[Dict]:
        houses = []
        print(f"\n{'='*60}")
        print(f"[开始] {spider.name} - {district}")
        print(f"{'='*60}")

        for page in range(1, max_pages + 1):
            print(f"[{spider.name}] 正在爬取第 {page}/{max_pages} 页...")
            try:
                page_houses = spider.get_house_list(district, page)
                if not page_houses:
                    print(f"[{spider.name}] 第 {page} 页无数据，停止爬取")
                    break

                houses.extend(page_houses)
                print(f"[{spider.name}] 第 {page} 页获取 {len(page_houses)} 条房源")

            except Exception as e:
                print(f"[{spider.name}] 第 {page} 页爬取失败: {e}")
                continue

        print(f"[完成] {spider.name} - {district}: 共获取 {len(houses)} 条房源")
        return houses

    def crawl_all_sites(self) -> List[Dict]:
        all_houses = []
        districts = self.config.get('districts', ['吉阳区', '天涯区'])
        max_pages = self.config.get('crawl_settings', {}).get('max_pages', 50)

        print(f"\n{'#'*60}")
        print(f"# 开始爬取房源数据")
        print(f"# 城市: {self.config.get('city', '三亚')}")
        print(f"# 区域: {', '.join(districts)}")
        print(f"# 网站: {', '.join([s.name for s in self.spiders])}")
        print(f"# 最大页数: {max_pages}")
        print(f"{'#'*60}\n")

        for spider in self.spiders:
            for district in districts:
                try:
                    houses = self.crawl_single_site(spider, district, max_pages)
                    all_houses.extend(houses)
                except Exception as e:
                    print(f"[错误] {spider.name} - {district} 爬取失败: {e}")
                    continue

        print(f"\n{'='*60}")
        print(f"[总计] 共爬取 {len(all_houses)} 条房源数据")
        print(f"{'='*60}\n")

        return all_houses

    def process_and_export(self, houses: List[Dict]) -> Dict:
        print("\n[处理] 开始处理数据...")

        df = self.processor.process_houses(houses)

        if df.empty:
            print("[警告] 处理后数据为空")
            return {}

        print(f"[处理] 数据清洗完成，剩余 {len(df)} 条有效房源")

        stats = self.processor.get_statistics(df)

        print("\n[统计] 数据统计信息:")
        for key, value in stats.items():
            if not isinstance(value, dict):
                print(f"  - {key}: {value}")

        print("\n[导出] 开始导出文件...")
        exported_files = self.exporter.export_all(df, stats)

        print("\n[导出] 导出完成:")
        for file_type, file_path in exported_files.items():
            print(f"  - {file_type.upper()}: {file_path}")

        return {
            'dataframe': df,
            'statistics': stats,
            'files': exported_files
        }

    def run(self, use_mock_data: bool = False) -> Dict:
        start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        try:
            if use_mock_data:
                print("\n[模式] 使用模拟数据（测试模式）")
                from tests.mock_data import MockDataGenerator
                generator = MockDataGenerator()
                houses = generator.generate_houses(100)
                print(f"[模拟] 已生成 {len(houses)} 条模拟数据")
            else:
                houses = self.crawl_all_sites()

            if not houses:
                print("\n[警告] 未获取到任何房源数据")
                return {}

            result = self.process_and_export(houses)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            print(f"\n{'='*60}")
            print(f"爬取任务完成!")
            print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"总耗时: {duration:.2f} 秒")
            print(f"{'='*60}\n")

            return result

        except Exception as e:
            print(f"\n[错误] 爬取任务失败: {e}")
            import traceback
            traceback.print_exc()
            return {}


def main():
    import sys
    
    use_mock = '--mock' in sys.argv or '-m' in sys.argv
    
    engine = HouseCrawlerEngine()
    result = engine.run(use_mock_data=use_mock)

    if result:
        print("\n任务执行成功！")
        print(f"共获取 {len(result['dataframe'])} 条房源数据")
        print(f"文件已保存到 output 目录")
    else:
        print("\n❌ 任务执行失败，请检查日志")


if __name__ == "__main__":
    main()
