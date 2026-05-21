import yaml
import os
import sys
from datetime import datetime


def quick_setup():
    print("\n" + "="*60)
    print("三亚房源爬取系统 - 快速配置向导")
    print("="*60 + "\n")

    config_path = "config/settings.yaml"

    if not os.path.exists(config_path):
        print("[错误] 配置文件不存在")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print("当前配置:")
    print(f"  城市: {config.get('city', '三亚')}")
    print(f"  区域: {', '.join(config.get('districts', []))}")
    print(f"  预算范围: {config['price_range']['min']} - {config['price_range']['max']} 元")
    print(f"  最大爬取页数: {config['crawl_settings']['max_pages']}")
    print(f"  导出格式: {', '.join(config.get('export_formats', []))}")

    print("\n" + "-"*60)
    print("是否修改配置？(y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        print("\n请输入新的配置（直接回车保持原值）:")

        print(f"预算上限（万元，当前: {config['price_range']['max']/10000}）: ", end="")
        max_price = input().strip()
        if max_price:
            config['price_range']['max'] = int(float(max_price) * 10000)

        print(f"最大爬取页数（当前: {config['crawl_settings']['max_pages']}）: ", end="")
        max_pages = input().strip()
        if max_pages:
            config['crawl_settings']['max_pages'] = int(max_pages)

        print("是否启用所有网站？(y/n，当前: 全部启用): ", end="")
        enable_all = input().strip().lower()
        if enable_all == 'n':
            print("请选择要启用的网站（输入编号，用逗号分隔）:")
            sites = list(config['websites'].keys())
            for i, site in enumerate(sites, 1):
                print(f"  {i}. {config['websites'][site]['name']}")
            print("选择: ", end="")
            selected = input().strip()
            if selected:
                selected_indices = [int(x.strip()) - 1 for x in selected.split(',')]
                for i, site in enumerate(sites):
                    config['websites'][site]['enabled'] = i in selected_indices

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

        print("\n[√] 配置已更新")

    print("\n" + "="*60)
    print("配置完成！")
    print("="*60 + "\n")


def view_results():
    output_dir = "output"

    if not os.path.exists(output_dir):
        print("\n[提示] 输出目录不存在，请先运行爬虫")
        return

    files = os.listdir(output_dir)
    if not files:
        print("\n[提示] 输出目录为空，请先运行爬虫")
        return

    print("\n" + "="*60)
    print("已生成的文件:")
    print("="*60)

    for file in sorted(files, reverse=True):
        file_path = os.path.join(output_dir, file)
        size = os.path.getsize(file_path) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"  {file}")
        print(f"    大小: {size:.2f} KB | 时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n")


def main():
    while True:
        print("\n" + "="*60)
        print("三亚房源爬取系统 - 主菜单")
        print("="*60)
        print("\n  1. 🚀 一键爬取（使用当前配置）")
        print("  2. ⚙️  修改配置")
        print("  3. 📊 查看结果")
        print("  4. ❌ 退出")
        print("\n" + "-"*60)
        print("请选择 (1-4): ", end="")

        choice = input().strip()

        if choice == '1':
            print("\n开始爬取...")
            os.system("python main.py")
        elif choice == '2':
            quick_setup()
        elif choice == '3':
            view_results()
        elif choice == '4':
            print("\n再见！\n")
            break
        else:
            print("\n[错误] 无效选择，请重新输入")


if __name__ == "__main__":
    main()
