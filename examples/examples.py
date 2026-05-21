"""
示例脚本 - 演示各种使用场景
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import ConfigManager, logger
from main import HouseCrawlerEngine
from core import DataProcessor, EnhancedExporter, DataVisualizer
import pandas as pd


def example_basic_crawl():
    """
    示例1: 基础爬取
    """
    print("\n" + "="*60)
    print("示例1: 基础爬取")
    print("="*60 + "\n")

    engine = HouseCrawlerEngine()
    result = engine.run()

    if result:
        print(f"✅ 爬取完成！共获取 {len(result['dataframe'])} 条房源")
        print(f"📊 平均价格: {result['statistics'].get('平均总价(万)', 0):.2f} 万元")
        print(f"📁 文件已保存到 output 目录")


def example_custom_config():
    """
    示例2: 自定义配置
    """
    print("\n" + "="*60)
    print("示例2: 自定义配置爬取")
    print("="*60 + "\n")

    config = ConfigManager()

    config.update_price_range(800000, 1500000)
    config.update_districts(['吉阳区'])
    config.enable_website('wuba', enabled=False)
    config.update_crawl_settings(max_pages=10, delay=2)

    config.print_config()

    engine = HouseCrawlerEngine()
    result = engine.run()

    if result:
        print(f"✅ 爬取完成！共获取 {len(result['dataframe'])} 条房源")


def example_data_analysis():
    """
    示例3: 数据分析
    """
    print("\n" + "="*60)
    print("示例3: 数据分析")
    print("="*60 + "\n")

    try:
        df = pd.read_excel('output/三亚房源_latest.xlsx')
    except:
        print("⚠️  请先运行爬虫获取数据")
        return

    print(f"数据概览: {len(df)} 条房源\n")

    print("价格统计:")
    print(df['总价(万)'].describe())

    print("\n区域分布:")
    print(df['区域'].value_counts())

    print("\n户型分布 (Top 5):")
    print(df['户型'].value_counts().head())

    print("\n性价比最高的5套房:")
    df['性价比'] = df['面积'] / df['总价(万)']
    top5 = df.nlargest(5, '性价比')[['标题', '面积', '总价(万)', '性价比']]
    print(top5)


def example_visualization():
    """
    示例4: 数据可视化
    """
    print("\n" + "="*60)
    print("示例4: 数据可视化")
    print("="*60 + "\n")

    try:
        df = pd.read_excel('output/三亚房源_latest.xlsx')
    except:
        print("⚠️  请先运行爬虫获取数据")
        return

    visualizer = DataVisualizer(output_dir="output/charts")

    print("正在生成图表...")
    chart_files = visualizer.generate_all_charts(df)

    print(f"\n✅ 已生成 {len(chart_files)} 个图表:")
    for chart in chart_files:
        print(f"  📊 {chart}")


def example_enhanced_export():
    """
    示例5: 增强导出（JSON + Markdown + 图表）
    """
    print("\n" + "="*60)
    print("示例5: 增强导出")
    print("="*60 + "\n")

    try:
        df = pd.read_excel('output/三亚房源_latest.xlsx')
    except:
        print("⚠️  请先运行爬虫获取数据")
        return

    stats = {
        '总房源数': len(df),
        '平均总价(万)': df['总价(万)'].mean(),
        '平均面积(㎡)': df['面积'].mean(),
    }

    exporter = EnhancedExporter(output_dir="output/enhanced", filename_prefix="增强报告")

    print("正在导出多种格式...")
    files = exporter.export_with_charts(df, stats)

    print("\n✅ 导出完成:")
    for file_type, file_path in files.items():
        if isinstance(file_path, list):
            print(f"\n{file_type.upper()}:")
            for path in file_path:
                print(f"  📄 {path}")
        else:
            print(f"\n{file_type.upper()}:")
            print(f"  📄 {file_path}")


def example_filter_data():
    """
    示例6: 数据筛选
    """
    print("\n" + "="*60)
    print("示例6: 数据筛选")
    print("="*60 + "\n")

    try:
        df = pd.read_excel('output/三亚房源_latest.xlsx')
    except:
        print("⚠️  请先运行爬虫获取数据")
        return

    print(f"原始数据: {len(df)} 条\n")

    print("筛选条件:")
    print("  - 价格: 100-150万")
    print("  - 面积: 90-120平米")
    print("  - 区域: 吉阳区")

    filtered = df[
        (df['总价(万)'] >= 100) &
        (df['总价(万)'] <= 150) &
        (df['面积'] >= 90) &
        (df['面积'] <= 120) &
        (df['区域'] == '吉阳区')
    ]

    print(f"\n筛选结果: {len(filtered)} 条房源")

    if not filtered.empty:
        print("\n符合条件的房源:")
        print(filtered[['标题', '小区', '户型', '面积', '总价(万)']].head(10))

        filtered.to_excel('output/筛选结果.xlsx', index=False)
        print("\n✅ 筛选结果已保存到: output/筛选结果.xlsx")


def example_price_comparison():
    """
    示例7: 价格对比分析
    """
    print("\n" + "="*60)
    print("示例7: 价格对比分析")
    print("="*60 + "\n")

    try:
        df = pd.read_excel('output/三亚房源_latest.xlsx')
    except:
        print("⚠️  请先运行爬虫获取数据")
        return

    print("各网站价格对比:\n")

    comparison = df.groupby('来源').agg({
        '总价(万)': ['count', 'mean', 'median', 'min', 'max'],
        '面积': 'mean'
    }).round(2)

    comparison.columns = ['房源数', '平均价', '中位价', '最低价', '最高价', '平均面积']

    print(comparison)

    print("\n各区域价格对比:\n")

    district_comparison = df.groupby('区域').agg({
        '总价(万)': ['count', 'mean', 'median'],
        '面积': 'mean'
    }).round(2)

    district_comparison.columns = ['房源数', '平均价', '中位价', '平均面积']

    print(district_comparison)


def main():
    print("\n" + "#"*60)
    print("# 三亚房源爬取系统 - 使用示例")
    print("#"*60)

    examples = {
        '1': ('基础爬取', example_basic_crawl),
        '2': ('自定义配置爬取', example_custom_config),
        '3': ('数据分析', example_data_analysis),
        '4': ('数据可视化', example_visualization),
        '5': ('增强导出', example_enhanced_export),
        '6': ('数据筛选', example_filter_data),
        '7': ('价格对比', example_price_comparison),
    }

    print("\n可用示例:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")

    print("\n请选择示例 (1-7, 或 'all' 运行所有): ", end="")
    choice = input().strip()

    if choice == 'all':
        for key in sorted(examples.keys()):
            _, func = examples[key]
            func()
    elif choice in examples:
        _, func = examples[choice]
        func()
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
