"""
测试真实爬虫 - 使用Selenium爬取真实数据
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiders.lianjia_selenium import LianjiaSeleniumSpider
from spiders.anjuke_selenium import AnjukeSeleniumSpider
from utils.config_manager import ConfigManager


def test_real_crawl():
    print("\n" + "="*60)
    print("真实爬虫测试")
    print("="*60)
    
    config_manager = ConfigManager()
    config = {
        'base_url': 'https://sanya.lianjia.com',
        'name': '链家网',
        'timeout': 30,
        'delay': 2
    }
    
    print("\n[测试] 链家网爬虫")
    print("-" * 60)
    
    try:
        spider = LianjiaSeleniumSpider(config)
        
        district = "吉阳区"
        page = 1
        
        print(f"[开始] 爬取 {district} 第 {page} 页...")
        
        houses = spider.get_house_list(district, page)
        
        if houses:
            print(f"\n[成功] 获取到 {len(houses)} 条真实房源数据！")
            print("\n示例房源:")
            for i, house in enumerate(houses[:5], 1):
                print(f"\n房源 {i}:")
                print(f"  标题: {house.get('标题', 'N/A')}")
                print(f"  区域: {house.get('区域', 'N/A')}")
                print(f"  小区: {house.get('小区', 'N/A')}")
                print(f"  户型: {house.get('户型', 'N/A')}")
                print(f"  面积: {house.get('面积', 'N/A')} 平米")
                print(f"  总价: {house.get('总价(万)', 'N/A')} 万")
                print(f"  单价: {house.get('单价', 'N/A')}")
                print(f"  来源: {house.get('来源', 'N/A')}")
                print(f"  链接: {house.get('链接', 'N/A')}")
            
            spider.close()
            return True
        else:
            print(f"\n[失败] 未获取到数据")
            spider.close()
            return False
            
    except Exception as e:
        print(f"\n[错误] 爬虫测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("开始测试真实爬虫")
    print("="*60)
    print("\n提示：")
    print("  1. 需要安装Chrome浏览器")
    print("  2. 首次运行会自动下载ChromeDriver")
    print("  3. 爬取过程可能需要1-2分钟")
    print("  4. 请耐心等待...")
    
    input("\n按Enter键开始测试...")
    
    success = test_real_crawl()
    
    if success:
        print("\n" + "="*60)
        print("测试成功！真实爬虫工作正常！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("测试失败，请检查：")
        print("  1. Chrome浏览器是否已安装")
        print("  2. 网络连接是否正常")
        print("  3. 是否需要安装webdriver-manager")
        print("="*60)


if __name__ == "__main__":
    main()
