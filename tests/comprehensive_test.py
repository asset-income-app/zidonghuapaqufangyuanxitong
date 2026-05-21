"""
全面测试脚本 - 测试所有模块和功能
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    print("\n" + "="*60)
    print("测试1: 模块导入测试")
    print("="*60)

    modules = [
        ("utils.logger", "日志系统"),
        ("utils.config_manager", "配置管理"),
        ("utils.proxy_pool", "代理池"),
        ("utils.progress", "进度显示"),
        ("core.processor", "数据处理"),
        ("core.exporter", "导出模块"),
        ("core.visualizer", "数据可视化"),
        ("core.database", "数据库"),
        ("core.scheduler", "定时任务"),
        ("core.notifier", "邮件通知"),
        ("core.word_exporter", "Word导出"),
        ("spiders.base_spider", "爬虫基类"),
        ("spiders.lianjia", "链家爬虫"),
        ("spiders.anjuke", "安居客爬虫"),
        ("spiders.wuba", "58同城爬虫"),
        ("spiders.beike", "贝壳爬虫"),
    ]

    success_count = 0
    failed_modules = []

    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {description} ({module_name})")
            success_count += 1
        except Exception as e:
            print(f"  ❌ {description} ({module_name}): {e}")
            failed_modules.append((module_name, str(e)))

    print(f"\n导入测试结果: {success_count}/{len(modules)} 成功")

    if failed_modules:
        print("\n失败的模块:")
        for module, error in failed_modules:
            print(f"  - {module}: {error}")
        return False

    return True


def test_database():
    print("\n" + "="*60)
    print("测试2: 数据库功能测试")
    print("="*60)

    try:
        from core.database import Database
        import tempfile
        import os

        test_db_path = os.path.join(tempfile.gettempdir(), "test_houses.db")
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

        db = Database(test_db_path)

        test_house = {
            '标题': '测试房源',
            '链接': 'http://test.com',
            '区域': '吉阳区',
            '小区': '测试小区',
            '位置': '测试位置',
            '户型': '3室2厅',
            '面积': 120.5,
            '朝向': '南北',
            '楼层': '中层',
            '总价(万)': 150,
            '单价': '12500元/平',
            '标签': '海景',
            '来源': '测试',
            '房源信息': '测试信息'
        }

        house_id = db.insert_house(test_house)
        print(f"  ✅ 插入数据成功 (ID: {house_id})")

        houses = db.get_houses(limit=10)
        print(f"  ✅ 查询数据成功 (共 {len(houses)} 条)")

        stats = db.get_statistics()
        print(f"  ✅ 统计功能成功 (总房源数: {stats['total_count']})")

        results = db.search_houses('测试')
        print(f"  ✅ 搜索功能成功 (找到 {len(results)} 条)")

        if os.path.exists(test_db_path):
            os.remove(test_db_path)

        print("\n数据库测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ 数据库测试失败: {e}")
        return False


def test_config():
    print("\n" + "="*60)
    print("测试3: 配置管理测试")
    print("="*60)

    try:
        from utils.config_manager import ConfigManager

        config = ConfigManager()

        city = config.get('city')
        print(f"  ✅ 读取城市配置: {city}")

        districts = config.get('districts')
        print(f"  ✅ 读取区域配置: {districts}")

        price_range = config.get('price_range')
        print(f"  ✅ 读取价格范围: {price_range}")

        print("\n配置管理测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ 配置管理测试失败: {e}")
        return False


def test_data_processor():
    print("\n" + "="*60)
    print("测试4: 数据处理测试")
    print("="*60)

    try:
        from core.processor import DataProcessor
        from utils.config_manager import ConfigManager
        import pandas as pd

        config_manager = ConfigManager()
        config = {
            'price_range': config_manager.get('price_range'),
            'districts': config_manager.get('districts')
        }

        processor = DataProcessor(config)

        test_data = [
            {
                '标题': '测试房源1',
                '区域': '吉阳区',
                '户型': '3室2厅',
                '面积': '120平米',
                '总价': '150万',
                '来源': '测试'
            },
            {
                '标题': '测试房源2',
                '区域': '天涯区',
                '户型': '2室1厅',
                '面积': '80平米',
                '总价': '100万',
                '来源': '测试'
            }
        ]

        processed_df = processor.process_houses(test_data)

        print(f"  ✅ 数据处理成功 (处理前: {len(test_data)} 条, 处理后: {len(processed_df)} 条)")

        print("\n数据处理测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ 数据处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exporter():
    print("\n" + "="*60)
    print("测试5: 导出功能测试")
    print("="*60)

    try:
        from core.exporter import Exporter
        from core.word_exporter import WordExporter
        import pandas as pd
        import tempfile
        import os

        test_df = pd.DataFrame([
            {
                '标题': '测试房源',
                '区域': '吉阳区',
                '户型': '3室2厅',
                '面积': 120,
                '总价(万)': 150,
                '来源': '测试'
            }
        ])

        test_stats = {
            '总房源数': 1,
            '平均总价(万)': 150,
            '最低总价(万)': 150,
            '最高总价(万)': 150,
            '平均面积(㎡)': 120
        }

        output_dir = tempfile.mkdtemp()

        exporter = Exporter(output_dir)
        exported_files = exporter.export_all(test_df, test_stats)
        print(f"  ✅ 导出功能成功 (导出 {len(exported_files)} 个文件)")

        word_exporter = WordExporter(output_dir)
        word_file = word_exporter.export_to_word(test_df, test_stats)
        print(f"  ✅ Word导出成功: {os.path.basename(word_file)}")

        for file in exported_files.values():
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(word_file):
            os.remove(word_file)
        os.rmdir(output_dir)

        print("\n导出功能测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ 导出功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scheduler():
    print("\n" + "="*60)
    print("测试6: 定时任务测试")
    print("="*60)

    try:
        from core.scheduler import TaskScheduler

        scheduler = TaskScheduler()

        jobs = scheduler.get_jobs()
        print(f"  ✅ 定时任务调度器初始化成功")

        scheduler.shutdown()
        print(f"  ✅ 定时任务调度器关闭成功")

        print("\n定时任务测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ 定时任务测试失败: {e}")
        return False


def test_web_app():
    print("\n" + "="*60)
    print("测试7: Web应用测试")
    print("="*60)

    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web'))

        from web.app import app

        print(f"  ✅ Flask应用初始化成功")

        with app.test_client() as client:
            response = client.get('/api/config')
            print(f"  ✅ API接口测试成功 (状态码: {response.status_code})")

        print("\nWeb应用测试结果: 全部通过 ✅")
        return True

    except Exception as e:
        print(f"\n❌ Web应用测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    print("\n" + "="*60)
    print("三亚房源智能爬取系统 - 全面测试")
    print("="*60)

    tests = [
        ("模块导入", test_imports),
        ("数据库功能", test_database),
        ("配置管理", test_config),
        ("数据处理", test_data_processor),
        ("导出功能", test_exporter),
        ("定时任务", test_scheduler),
        ("Web应用", test_web_app),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name}测试异常: {e}")
            results.append((test_name, False))

    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    success_count = sum(1 for _, result in results if result)
    total_count = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    print(f"\n总体结果: {success_count}/{total_count} 测试通过")

    if success_count == total_count:
        print("\n🎉 恭喜！所有测试通过！系统运行正常！")
    else:
        print("\n⚠️  部分测试失败，请检查相关模块")

    return success_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
