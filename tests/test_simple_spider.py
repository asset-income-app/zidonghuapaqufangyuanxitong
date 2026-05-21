"""
测试真实爬虫 - 使用requests（无需Chrome）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiders.simple_spider import LianjiaSimpleSpider, AnjukeSimpleSpider


def test_lianjia():
    print("\n" + "="*60)
    print("测试链家网爬虫")
    print("="*60)
    
    config = {
        'base_url': 'https://sanya.lianjia.com',
        'name': '链家网',
        'timeout': 30,
        'delay': 2
    }
    
    try:
        spider = LianjiaSimpleSpider(config)
        
        district = "吉阳区"
        page = 1
        
        print(f"[爬取] {district} 第 {page} 页...")
        
        houses = spider.get_house_list(district, page)
        
        if houses:
            print(f"\n[成功] 获取到 {len(houses)} 条真实房源！\n")
            print("前3条房源:")
            for i, house in enumerate(houses[:3], 1):
                print(f"\n{i}. {house.get('标题', 'N/A')}")
                print(f"   价格: {house.get('总价(万)', 'N/A')}万")
                print(f"   面积: {house.get('面积', 'N/A')}平米")
                print(f"   户型: {house.get('户型', 'N/A')}")
                print(f"   来源: {house.get('来源', 'N/A')}")
            
            return True, len(houses)
        else:
            print("[失败] 未获取到数据")
            return False, 0
            
    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        return False, 0


def test_anjuke():
    print("\n" + "="*60)
    print("测试安居客爬虫")
    print("="*60)
    
    config = {
        'base_url': 'https://sanya.anjuke.com',
        'name': '安居客',
        'timeout': 30,
        'delay': 2
    }
    
    try:
        spider = AnjukeSimpleSpider(config)
        
        district = "吉阳区"
        page = 1
        
        print(f"[爬取] {district} 第 {page} 页...")
        
        houses = spider.get_house_list(district, page)
        
        if houses:
            print(f"\n[成功] 获取到 {len(houses)} 条真实房源！\n")
            print("前3条房源:")
            for i, house in enumerate(houses[:3], 1):
                print(f"\n{i}. {house.get('标题', 'N/A')}")
                print(f"   价格: {house.get('总价(万)', 'N/A')}万")
                print(f"   面积: {house.get('面积', 'N/A')}平米")
            
            return True, len(houses)
        else:
            print("[失败] 未获取到数据")
            return False, 0
            
    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        return False, 0


def main():
    print("\n" + "="*60)
    print("真实爬虫测试（无需Chrome）")
    print("="*60)
    
    results = []
    
    # 测试链家
    success, count = test_lianjia()
    results.append(('链家网', success, count))
    
    # 测试安居客
    success, count = test_anjuke()
    results.append(('安居客', success, count))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for name, success, count in results:
        status = "成功" if success else "失败"
        print(f"{name}: {status} ({count}条数据)")
    
    total_success = sum(1 for _, s, _ in results if s)
    total_count = sum(c for _, _, c in results)
    
    print(f"\n总计: {total_success}/{len(results)} 个爬虫成功")
    print(f"共获取: {total_count} 条真实房源数据")
    
    if total_success > 0:
        print("\n真实爬虫测试成功！系统可以正常爬取数据！")
    else:
        print("\n爬虫测试失败，可能原因：")
        print("  1. 网络连接问题")
        print("  2. 网站有反爬虫机制")
        print("  3. 网站结构已改变")


if __name__ == "__main__":
    main()
