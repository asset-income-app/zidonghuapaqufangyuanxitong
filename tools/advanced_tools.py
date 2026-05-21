"""
快速启动脚本 - 一键运行所有功能
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import Database
from core.scheduler import TaskScheduler
from utils import ConfigManager, logger


def show_menu():
    print("\n" + "="*60)
    print("三亚房源智能爬取系统 - 高级功能")
    print("="*60)
    print("\n  1. 🌐 启动Web界面")
    print("  2. 🗄️  数据库管理")
    print("  3. ⏰ 定时任务设置")
    print("  4. 📧 邮件通知设置")
    print("  5. 📊 数据对比分析")
    print("  6. 🔄 增量更新")
    print("  7. ❌ 退出")
    print("\n" + "-"*60)


def start_web():
    print("\n[启动] 正在启动Web界面...")
    os.system("cd web && python app.py")


def database_management():
    print("\n" + "="*60)
    print("数据库管理")
    print("="*60)

    db = Database()

    while True:
        print("\n  1. 查看统计信息")
        print("  2. 查看最近数据")
        print("  3. 搜索房源")
        print("  4. 清理旧数据")
        print("  5. 导出数据")
        print("  6. 返回主菜单")
        print("\n选择: ", end="")

        choice = input().strip()

        if choice == '1':
            stats = db.get_statistics()
            print("\n数据库统计:")
            print(f"  总房源数: {stats['total_count']}")
            print(f"  平均价格: {stats['avg_price']:.2f} 万元")
            print(f"  价格范围: {stats['min_price']:.2f} - {stats['max_price']:.2f} 万元")
            print(f"  平均面积: {stats['avg_area']:.2f} ㎡")

        elif choice == '2':
            houses = db.get_houses(limit=10)
            print(f"\n最近10条数据:")
            for i, house in enumerate(houses, 1):
                print(f"  {i}. {house['title'][:30]} - {house['price']}万")

        elif choice == '3':
            keyword = input("请输入搜索关键词: ").strip()
            houses = db.search_houses(keyword)
            print(f"\n找到 {len(houses)} 条结果:")
            for i, house in enumerate(houses[:10], 1):
                print(f"  {i}. {house['title'][:30]} - {house['price']}万")

        elif choice == '4':
            days = int(input("删除多少天前的数据? ").strip())
            deleted = db.delete_old_houses(days)
            print(f"已删除 {deleted} 条旧数据")

        elif choice == '5':
            df = db.export_to_dataframe()
            filename = f"output/数据库导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"已导出到: {filename}")

        elif choice == '6':
            break


def scheduler_management():
    print("\n" + "="*60)
    print("定时任务管理")
    print("="*60)

    scheduler = TaskScheduler()

    while True:
        print("\n  1. 添加定时任务")
        print("  2. 查看所有任务")
        print("  3. 暂停任务")
        print("  4. 恢复任务")
        print("  5. 删除任务")
        print("  6. 返回主菜单")
        print("\n选择: ", end="")

        choice = input().strip()

        if choice == '1':
            job_id = input("任务ID: ").strip()
            print("定时方式:")
            print("  1. 每天定时")
            print("  2. 间隔小时")
            mode = input("选择: ").strip()

            if mode == '1':
                time_str = input("执行时间 (HH:MM): ").strip()
                hour, minute = time_str.split(':')
                cron = f"{minute} {hour} * * *"
                scheduler.add_crawl_job(job_id, cron_expression=cron)
            elif mode == '2':
                hours = int(input("间隔小时数: ").strip())
                scheduler.add_crawl_job(job_id, interval_hours=hours)

        elif choice == '2':
            jobs = scheduler.get_jobs()
            print("\n当前任务:")
            for job in jobs:
                print(f"  ID: {job['id']}")
                print(f"  下次执行: {job['next_run_time']}")
                print()

        elif choice == '3':
            job_id = input("任务ID: ").strip()
            scheduler.pause_job(job_id)

        elif choice == '4':
            job_id = input("任务ID: ").strip()
            scheduler.resume_job(job_id)

        elif choice == '5':
            job_id = input("任务ID: ").strip()
            scheduler.remove_job(job_id)

        elif choice == '6':
            break


def email_settings():
    print("\n" + "="*60)
    print("邮件通知设置")
    print("="*60)

    print("\n请配置SMTP邮箱:")
    smtp_server = input("SMTP服务器 (如: smtp.qq.com): ").strip()
    smtp_port = int(input("SMTP端口 (如: 587): ").strip())
    sender_email = input("发件邮箱: ").strip()
    sender_password = input("邮箱授权码: ").strip()
    receiver_emails = input("收件邮箱 (多个用逗号分隔): ").strip().split(',')

    from core.notifier import EmailNotifier

    notifier = EmailNotifier(smtp_server, smtp_port, sender_email, sender_password)

    print("\n发送测试邮件...")
    success = notifier.send_notification(
        receiver_emails,
        "测试邮件",
        "这是一封测试邮件，如果您收到此邮件，说明邮件配置成功！"
    )

    if success:
        print("✅ 邮件配置成功！")
        print("\n提示: 爬取完成后会自动发送报告邮件")
    else:
        print("❌ 邮件发送失败，请检查配置")


def data_comparison():
    print("\n" + "="*60)
    print("数据对比分析")
    print("="*60)

    import pandas as pd
    import glob

    files = glob.glob("output/三亚房源_*.xlsx")
    if len(files) < 2:
        print("⚠️  需要至少2个数据文件进行对比")
        return

    print("\n可用文件:")
    for i, f in enumerate(files[-5:], 1):
        print(f"  {i}. {os.path.basename(f)}")

    print("\n选择两个文件进行对比:")
    idx1 = int(input("第一个文件编号: ").strip()) - 1
    idx2 = int(input("第二个文件编号: ").strip()) - 1

    df1 = pd.read_excel(files[-5:][idx1])
    df2 = pd.read_excel(files[-5:][idx2])

    print("\n对比结果:")
    print(f"  文件1: {len(df1)} 条房源")
    print(f"  文件2: {len(df2)} 条房源")
    print(f"  变化: {len(df2) - len(df1):+d} 条")

    if '总价(万)' in df1.columns and '总价(万)' in df2.columns:
        avg1 = df1['总价(万)'].mean()
        avg2 = df2['总价(万)'].mean()
        print(f"\n  平均价格变化: {avg2 - avg1:+.2f} 万元")


def incremental_update():
    print("\n" + "="*60)
    print("增量更新")
    print("="*60)

    from main import HouseCrawlerEngine
    from core.database import Database
    import pandas as pd

    db = Database()

    print("\n正在爬取最新数据...")
    engine = HouseCrawlerEngine()
    result = engine.run()

    if result:
        df = result['dataframe']
        houses = df.to_dict('records')

        print(f"\n爬取到 {len(houses)} 条数据")
        print("正在保存到数据库...")

        count = db.insert_houses_batch(houses)
        print(f"✅ 成功保存 {count} 条新数据")

        stats = db.get_statistics()
        print(f"\n数据库统计:")
        print(f"  总房源数: {stats['total_count']}")


def main():
    while True:
        show_menu()
        choice = input("请选择 (1-7): ").strip()

        if choice == '1':
            start_web()
        elif choice == '2':
            database_management()
        elif choice == '3':
            scheduler_management()
        elif choice == '4':
            email_settings()
        elif choice == '5':
            data_comparison()
        elif choice == '6':
            incremental_update()
        elif choice == '7':
            print("\n再见！\n")
            break
        else:
            print("\n[错误] 无效选择")


if __name__ == "__main__":
    from datetime import datetime
    main()
