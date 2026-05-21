"""
测试脚本 - 快速验证系统功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import ConfigManager, logger
from spiders import LianjiaSpider
from core import DataProcessor, Exporter
import pandas as pd


def test_config():
    print("\n" + "="*60)
    print("测试1: 配置管理")
    print("="*60)

    config = ConfigManager()

    print(f"城市: {config.get('city')}")
    print(f"区域: {config.get('districts')}")
    print(f"价格范围: {config.get('price_range')}")

    is_valid = config.validate()
    print(f"配置验证: {'✅ 通过' if is_valid else '❌ 失败'}")

    return config


def test_spider():
    print("\n" + "="*60)
    print("测试2: 爬虫功能（仅爬取1页测试）")
    print("="*60)

    config = {
        'base_url': 'https://sanya.lianjia.com',
        'name': '链家网',
        'delay': 1,
        'timeout': 10,
        'retry_times': 2
    }

    spider = LianjiaSpider(config)

    try:
        houses = spider.get_house_list("吉阳区", page=1)
        print(f"爬取结果: ✅ 成功获取 {len(houses)} 条房源")

        if houses:
            print("\n示例房源:")
            for key, value in houses[0].items():
                print(f"  {key}: {value}")

        return houses
    except Exception as e:
        print(f"爬取结果: ❌ 失败 - {e}")
        return []


def test_processor(houses):
    print("\n" + "="*60)
    print("测试3: 数据处理")
    print("="*60)

    if not houses:
        print("数据处理: ⚠️  跳过（无数据）")
        return None

    config = {
        'price_range': {'min': 0, 'max': 2000000},
        'districts': ['吉阳区', '天涯区']
    }

    processor = DataProcessor(config)

    try:
        df = processor.process_houses(houses)
        print(f"数据处理: ✅ 成功处理 {len(df)} 条有效数据")

        stats = processor.get_statistics(df)
        print("\n统计信息:")
        for key, value in stats.items():
            if not isinstance(value, dict):
                print(f"  {key}: {value}")

        return df
    except Exception as e:
        print(f"数据处理: ❌ 失败 - {e}")
        return None


def test_exporter(df):
    print("\n" + "="*60)
    print("测试4: 导出功能")
    print("="*60)

    if df is None or df.empty:
        print("导出功能: ⚠️  跳过（无数据）")
        return

    exporter = Exporter(output_dir="output/test", filename_prefix="测试房源")

    try:
        stats = {
            '总房源数': len(df),
            '平均总价(万)': df['总价(万)'].mean() if '总价(万)' in df.columns else 0,
            '爬取时间': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        files = exporter.export_all(df, stats)

        print("导出功能: ✅ 成功")
        print("\n导出文件:")
        for file_type, file_path in files.items():
            print(f"  {file_type.upper()}: {file_path}")

    except Exception as e:
        print(f"导出功能: ❌ 失败 - {e}")


def test_logger():
    print("\n" + "="*60)
    print("测试5: 日志系统")
    print("="*60)

    try:
        logger.debug("这是一条DEBUG日志")
        logger.info("这是一条INFO日志")
        logger.warning("这是一条WARNING日志")
        logger.error("这是一条ERROR日志")

        print("日志系统: ✅ 正常工作")
    except Exception as e:
        print(f"日志系统: ❌ 失败 - {e}")


def run_all_tests():
    print("\n" + "#"*60)
    print("# 三亚房源爬取系统 - 功能测试")
    print("#"*60)

    try:
        config = test_config()
        test_logger()
        houses = test_spider()
        df = test_processor(houses)
        test_exporter(df)

        print("\n" + "#"*60)
        print("# 测试完成！")
        print("#"*60 + "\n")

    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
