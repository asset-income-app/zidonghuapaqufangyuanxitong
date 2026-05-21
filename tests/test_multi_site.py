"""
真实爬取系统 - 多网站备用方案
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiders.simple_spider import LianjiaSimpleSpider, AnjukeSimpleSpider
from spiders.smart_spider import FangSpider, KeSpider
import pandas as pd


def test_all_websites():
    print("\n" + "="*70)
    print("三亚房源真实爬取系统")
    print("="*70)
    print("\n正在测试多个网站，寻找可用数据源...\n")
    
    all_houses = []
    
    spiders = [
        ('房天下', FangSpider, {'base_url': 'https://sanya.esf.fang.com', 'timeout': 15}),
        ('贝壳找房', KeSpider, {'base_url': 'https://sy.ke.com', 'timeout': 15}),
        ('链家网', LianjiaSimpleSpider, {'base_url': 'https://sanya.lianjia.com', 'timeout': 15}),
        ('安居客', AnjukeSimpleSpider, {'base_url': 'https://sanya.anjuke.com', 'timeout': 15}),
    ]
    
    for name, spider_class, config in spiders:
        print(f"\n[{name}] 开始测试...")
        print("-" * 70)
        
        try:
            spider = spider_class(config)
            
            for district in ['吉阳区', '天涯区']:
                print(f"  爬取 {district}...", end=' ')
                houses = spider.get_house_list(district, page=1)
                
                if houses:
                    print(f"成功! 获取 {len(houses)} 条")
                    all_houses.extend(houses)
                else:
                    print("失败")
                
                time.sleep(1)
                
        except Exception as e:
            print(f"  错误: {str(e)[:50]}")
    
    # 结果汇总
    print("\n" + "="*70)
    print("爬取结果")
    print("="*70)
    
    if all_houses:
        print(f"\n成功! 共获取 {len(all_houses)} 条真实房源数据\n")
        
        # 按来源统计
        df = pd.DataFrame(all_houses)
        source_count = df['来源'].value_counts()
        
        print("数据来源统计:")
        for source, count in source_count.items():
            print(f"  {source}: {count} 条")
        
        # 显示示例
        print("\n前3条房源示例:")
        print("-" * 70)
        
        for i, house in enumerate(all_houses[:3], 1):
            print(f"\n{i}. {house.get('标题', 'N/A')}")
            print(f"   价格: {house.get('总价(万)', 'N/A')}万")
            print(f"   面积: {house.get('面积', 'N/A')}平米")
            print(f"   来源: {house.get('来源', 'N/A')}")
        
        # 保存数据
        output_file = 'output/真实房源_' + time.strftime('%Y%m%d_%H%M%S') + '.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n数据已保存: {output_file}")
        print("\n真实爬取成功!")
        
        return True
    else:
        print("\n未能获取到数据")
        print("\n原因分析:")
        print("  1. 网络环境限制 - 无法访问房产网站")
        print("  2. DNS解析失败 - 域名无法解析")
        print("  3. 网站反爬虫 - 被识别为爬虫")
        
        print("\n解决方案:")
        print("  1. 检查网络连接和DNS设置")
        print("  2. 使用VPN或代理")
        print("  3. 使用模拟数据模式测试系统")
        print("  4. 稍后重试")
        
        return False


if __name__ == "__main__":
    test_all_websites()
