"""
真实爬取测试 - 显示详细过程
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiders.simple_spider import LianjiaSimpleSpider, AnjukeSimpleSpider


def test_real_crawl():
    print("\n" + "="*70)
    print("真实房源爬取测试")
    print("="*70)
    
    all_houses = []
    
    # 测试链家
    print("\n[1/2] 测试链家网")
    print("-" * 70)
    
    config_lianjia = {
        'base_url': 'https://sanya.lianjia.com',
        'name': '链家网',
        'timeout': 30,
        'delay': 2
    }
    
    try:
        spider = LianjiaSimpleSpider(config_lianjia)
        
        for district in ['吉阳区', '天涯区']:
            print(f"\n正在爬取 {district}...")
            houses = spider.get_house_list(district, page=1)
            
            if houses:
                print(f"✓ 成功获取 {len(houses)} 条房源")
                all_houses.extend(houses)
            else:
                print(f"✗ 未获取到数据")
                
            time.sleep(2)
            
    except Exception as e:
        print(f"链家爬虫错误: {e}")
    
    # 测试安居客
    print("\n[2/2] 测试安居客")
    print("-" * 70)
    
    config_anjuke = {
        'base_url': 'https://sanya.anjuke.com',
        'name': '安居客',
        'timeout': 30,
        'delay': 2
    }
    
    try:
        spider = AnjukeSimpleSpider(config_anjuke)
        
        for district in ['吉阳区', '天涯区']:
            print(f"\n正在爬取 {district}...")
            houses = spider.get_house_list(district, page=1)
            
            if houses:
                print(f"✓ 成功获取 {len(houses)} 条房源")
                all_houses.extend(houses)
            else:
                print(f"✗ 未获取到数据")
                
            time.sleep(2)
            
    except Exception as e:
        print(f"安居客爬虫错误: {e}")
    
    # 显示结果
    print("\n" + "="*70)
    print("爬取结果汇总")
    print("="*70)
    
    if all_houses:
        print(f"\n共获取 {len(all_houses)} 条真实房源数据！\n")
        
        print("前5条房源示例:")
        print("-" * 70)
        
        for i, house in enumerate(all_houses[:5], 1):
            print(f"\n{i}. {house.get('标题', 'N/A')}")
            print(f"   区域: {house.get('区域', 'N/A')}")
            print(f"   小区: {house.get('小区', 'N/A')}")
            print(f"   户型: {house.get('户型', 'N/A')}")
            print(f"   面积: {house.get('面积', 'N/A')} 平米")
            print(f"   总价: {house.get('总价(万)', 'N/A')} 万")
            print(f"   单价: {house.get('单价', 'N/A')}")
            print(f"   来源: {house.get('来源', 'N/A')}")
            print(f"   链接: {house.get('链接', 'N/A')}")
        
        # 保存到CSV
        import pandas as pd
        df = pd.DataFrame(all_houses)
        output_file = 'output/真实房源_' + time.strftime('%Y%m%d_%H%M%S') + '.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n数据已保存到: {output_file}")
        print("\n真实爬取成功！系统可以正常工作！")
        
        return True
    else:
        print("\n未获取到任何数据")
        print("\n可能的原因:")
        print("  1. 网络连接问题")
        print("  2. 网站有反爬虫机制")
        print("  3. 网站结构已改变")
        print("\n建议:")
        print("  1. 检查网络连接")
        print("  2. 稍后重试")
        print("  3. 使用模拟数据模式测试系统功能")
        
        return False


if __name__ == "__main__":
    test_real_crawl()
