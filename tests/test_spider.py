"""
测试爬虫脚本 - 检查爬虫是否能正常工作
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiders.lianjia import LianjiaSpider
from spiders.anjuke import AnjukeSpider
from spiders.wuba import WubaSpider
from spiders.beike import BeikeSpider
from utils.config_manager import ConfigManager


def test_spider(spider_class, spider_name, config):
    print(f"\n{'='*60}")
    print(f"测试 {spider_name} 爬虫")
    print(f"{'='*60}")

    try:
        spider = spider_class(config)

        district = "吉阳区"
        page = 1

        print(f"正在爬取 {district} 第 {page} 页...")
        print(f"URL: {spider.search_url if hasattr(spider, 'search_url') else 'N/A'}")

        houses = spider.get_house_list(district, page)

        if houses:
            print(f"\n✅ 成功获取 {len(houses)} 条房源")
            print("\n示例房源:")
            for i, house in enumerate(houses[:3], 1):
                print(f"\n房源 {i}:")
                print(f"  标题: {house.get('标题', 'N/A')}")
                print(f"  区域: {house.get('区域', 'N/A')}")
                print(f"  户型: {house.get('户型', 'N/A')}")
                print(f"  面积: {house.get('面积', 'N/A')} ㎡")
                print(f"  总价: {house.get('总价(万)', 'N/A')} 万")
                print(f"  来源: {house.get('来源', 'N/A')}")
            return True
        else:
            print(f"\n❌ 未获取到数据")
            print("\n可能的原因:")
            print("  1. 网站有反爬虫机制")
            print("  2. 网站结构已改变")
            print("  3. 网络连接问题")
            print("  4. 区域映射不正确")
            return False

    except Exception as e:
        print(f"\n❌ 爬虫测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_network():
    print(f"\n{'='*60}")
    print("测试网络连接")
    print(f"{'='*60}")

    import requests

    test_urls = [
        ("链家", "https://sanya.lianjia.com"),
        ("安居客", "https://sanya.anjuke.com"),
        ("58同城", "https://sanya.58.com"),
        ("贝壳", "https://sanya.ke.com")
    ]

    for name, url in test_urls:
        try:
            print(f"\n测试 {name}: {url}")
            response = requests.get(url, timeout=10)
            print(f"  状态码: {response.status_code}")
            print(f"  响应时间: {response.elapsed.total_seconds():.2f}秒")
            if response.status_code == 200:
                print(f"  ✅ 连接正常")
            else:
                print(f"  ⚠️  状态码异常")
        except Exception as e:
            print(f"  ❌ 连接失败: {e}")


def main():
    print("\n" + "="*60)
    print("爬虫诊断测试")
    print("="*60)

    test_network()

    config_manager = ConfigManager()
    config = {
        'city': config_manager.get('city'),
        'districts': config_manager.get('districts'),
        'price_range': config_manager.get('price_range'),
        'crawl_settings': config_manager.get('crawl_settings')
    }

    print("\n" + "="*60)
    print("配置信息")
    print("="*60)
    print(f"城市: {config['city']}")
    print(f"区域: {config['districts']}")
    print(f"价格范围: {config['price_range']}")
    print(f"爬取设置: {config['crawl_settings']}")

    spider_tests = [
        (LianjiaSpider, "链家"),
        (AnjukeSpider, "安居客"),
        (WubaSpider, "58同城"),
        (BeikeSpider, "贝壳")
    ]

    results = []
    for spider_class, spider_name in spider_tests:
        time.sleep(2)
        result = test_spider(spider_class, spider_name, config)
        results.append((spider_name, result))

    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    for spider_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"  {spider_name}: {status}")

    success_count = sum(1 for _, result in results if result)
    print(f"\n总体结果: {success_count}/{len(results)} 个爬虫工作正常")


if __name__ == "__main__":
    main()
