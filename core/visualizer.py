import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List
import os
import seaborn as sns
from datetime import datetime

matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class DataVisualizer:
    def __init__(self, output_dir: str = "output/charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def generate_all_charts(self, df: pd.DataFrame) -> List[str]:
        if df.empty:
            print("[可视化] 数据为空，跳过图表生成")
            return []

        chart_files = []

        chart_files.append(self.plot_price_distribution(df))
        chart_files.append(self.plot_area_distribution(df))
        chart_files.append(self.plot_district_comparison(df))
        chart_files.append(self.plot_price_by_area(df))
        chart_files.append(self.plot_source_comparison(df))
        chart_files.append(self.plot_layout_distribution(df))

        chart_files = [f for f in chart_files if f]

        print(f"[可视化] 已生成 {len(chart_files)} 个图表")
        return chart_files

    def plot_price_distribution(self, df: pd.DataFrame) -> str:
        if '总价(万)' not in df.columns:
            return ""

        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            prices = df['总价(万)'].dropna()

            axes[0].hist(prices, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            axes[0].set_xlabel('总价（万元）', fontsize=12)
            axes[0].set_ylabel('房源数量', fontsize=12)
            axes[0].set_title('房价分布直方图', fontsize=14, fontweight='bold')
            axes[0].grid(axis='y', alpha=0.3)

            axes[1].boxplot(prices, vert=True, patch_artist=True,
                           boxprops=dict(facecolor='lightblue', color='blue'),
                           medianprops=dict(color='red', linewidth=2))
            axes[1].set_ylabel('总价（万元）', fontsize=12)
            axes[1].set_title('房价箱线图', fontsize=14, fontweight='bold')
            axes[1].grid(axis='y', alpha=0.3)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'price_distribution_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 价格分布图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成价格分布图失败: {e}")
            return ""

    def plot_area_distribution(self, df: pd.DataFrame) -> str:
        if '面积' not in df.columns:
            return ""

        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            areas = df['面积'].dropna()

            ax.hist(areas, bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
            ax.set_xlabel('面积（㎡）', fontsize=12)
            ax.set_ylabel('房源数量', fontsize=12)
            ax.set_title('房源面积分布', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)

            mean_area = areas.mean()
            median_area = areas.median()
            ax.axvline(mean_area, color='red', linestyle='--', linewidth=2, label=f'平均值: {mean_area:.1f}㎡')
            ax.axvline(median_area, color='blue', linestyle='--', linewidth=2, label=f'中位数: {median_area:.1f}㎡')
            ax.legend(fontsize=10)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'area_distribution_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 面积分布图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成面积分布图失败: {e}")
            return ""

    def plot_district_comparison(self, df: pd.DataFrame) -> str:
        if '区域' not in df.columns or '总价(万)' not in df.columns:
            return ""

        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            district_counts = df['区域'].value_counts()
            colors = plt.cm.Set3(range(len(district_counts)))

            axes[0].pie(district_counts.values, labels=district_counts.index, autopct='%1.1f%%',
                       colors=colors, startangle=90)
            axes[0].set_title('各区域房源数量占比', fontsize=14, fontweight='bold')

            district_prices = df.groupby('区域')['总价(万)'].agg(['mean', 'median', 'min', 'max'])
            district_prices.plot(kind='bar', ax=axes[1], width=0.8, colormap='Set2')
            axes[1].set_xlabel('区域', fontsize=12)
            axes[1].set_ylabel('价格（万元）', fontsize=12)
            axes[1].set_title('各区域房价统计', fontsize=14, fontweight='bold')
            axes[1].legend(['平均价', '中位数', '最低价', '最高价'], loc='upper right')
            axes[1].grid(axis='y', alpha=0.3)
            plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=0)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'district_comparison_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 区域对比图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成区域对比图失败: {e}")
            return ""

    def plot_price_by_area(self, df: pd.DataFrame) -> str:
        if '面积' not in df.columns or '总价(万)' not in df.columns:
            return ""

        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            data = df[['面积', '总价(万)']].dropna()

            scatter = ax.scatter(data['面积'], data['总价(万)'],
                               alpha=0.5, c=data['总价(万)'],
                               cmap='viridis', s=50, edgecolors='black', linewidth=0.5)

            z = np.polyfit(data['面积'], data['总价(万)'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(data['面积'].min(), data['面积'].max(), 100)
            ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='趋势线')

            ax.set_xlabel('面积（㎡）', fontsize=12)
            ax.set_ylabel('总价（万元）', fontsize=12)
            ax.set_title('面积与价格关系', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)

            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('总价（万元）', fontsize=10)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'price_by_area_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 面积价格关系图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成面积价格关系图失败: {e}")
            return ""

    def plot_source_comparison(self, df: pd.DataFrame) -> str:
        if '来源' not in df.columns:
            return ""

        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            source_counts = df['来源'].value_counts()
            colors = plt.cm.Spectral(range(len(source_counts)))

            axes[0].barh(source_counts.index, source_counts.values, color=colors)
            axes[0].set_xlabel('房源数量', fontsize=12)
            axes[0].set_title('各网站房源数量', fontsize=14, fontweight='bold')
            axes[0].grid(axis='x', alpha=0.3)

            for i, v in enumerate(source_counts.values):
                axes[0].text(v + 0.5, i, str(v), va='center', fontsize=10)

            if '总价(万)' in df.columns:
                source_prices = df.groupby('来源')['总价(万)'].mean().sort_values(ascending=True)
                axes[1].barh(source_prices.index, source_prices.values,
                            color=plt.cm.Spectral(range(len(source_prices))))
                axes[1].set_xlabel('平均价格（万元）', fontsize=12)
                axes[1].set_title('各网站平均房价', fontsize=14, fontweight='bold')
                axes[1].grid(axis='x', alpha=0.3)

                for i, v in enumerate(source_prices.values):
                    axes[1].text(v + 0.5, i, f'{v:.1f}', va='center', fontsize=10)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'source_comparison_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 网站对比图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成网站对比图失败: {e}")
            return ""

    def plot_layout_distribution(self, df: pd.DataFrame) -> str:
        if '户型' not in df.columns:
            return ""

        try:
            fig, ax = plt.subplots(figsize=(12, 6))

            layout_counts = df['户型'].value_counts().head(10)

            colors = plt.cm.Pastel1(range(len(layout_counts)))
            bars = ax.bar(range(len(layout_counts)), layout_counts.values, color=colors, edgecolor='black')

            ax.set_xlabel('户型', fontsize=12)
            ax.set_ylabel('房源数量', fontsize=12)
            ax.set_title('热门户型分布（Top 10）', fontsize=14, fontweight='bold')
            ax.set_xticks(range(len(layout_counts)))
            ax.set_xticklabels(layout_counts.index, rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            filename = os.path.join(self.output_dir, f'layout_distribution_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 户型分布图已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成户型分布图失败: {e}")
            return ""

    def create_summary_report(self, df: pd.DataFrame, stats: Dict) -> str:
        try:
            fig = plt.figure(figsize=(16, 12))

            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

            ax1 = fig.add_subplot(gs[0, :])
            ax1.axis('off')
            title_text = "三亚房源数据分析报告"
            ax1.text(0.5, 0.7, title_text, ha='center', va='center',
                    fontsize=24, fontweight='bold', transform=ax1.transAxes)

            stats_text = f"""
总房源数: {stats.get('总房源数', 0)} 套
平均总价: {stats.get('平均总价(万)', 0):.2f} 万元
平均面积: {stats.get('平均面积(㎡)', 0):.2f} ㎡
数据来源: 链家、安居客、58同城、贝壳
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            ax1.text(0.5, 0.3, stats_text, ha='center', va='center',
                    fontsize=14, transform=ax1.transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

            ax2 = fig.add_subplot(gs[1, 0])
            if '总价(万)' in df.columns:
                df['总价(万)'].dropna().hist(bins=20, ax=ax2, color='skyblue', edgecolor='black')
                ax2.set_title('价格分布', fontweight='bold')
                ax2.set_xlabel('总价（万元）')

            ax3 = fig.add_subplot(gs[1, 1])
            if '面积' in df.columns:
                df['面积'].dropna().hist(bins=20, ax=ax3, color='lightcoral', edgecolor='black')
                ax3.set_title('面积分布', fontweight='bold')
                ax3.set_xlabel('面积（㎡）')

            ax4 = fig.add_subplot(gs[1, 2])
            if '区域' in df.columns:
                df['区域'].value_counts().plot(kind='pie', ax=ax4, autopct='%1.1f%%')
                ax4.set_title('区域分布', fontweight='bold')
                ax4.set_ylabel('')

            ax5 = fig.add_subplot(gs[2, :])
            if '来源' in df.columns:
                source_counts = df['来源'].value_counts()
                ax5.bar(source_counts.index, source_counts.values, color='lightgreen', edgecolor='black')
                ax5.set_title('各网站房源数量', fontweight='bold')
                ax5.set_xlabel('数据来源')
                ax5.set_ylabel('房源数量')

            plt.suptitle('', fontsize=16, y=0.98)

            filename = os.path.join(self.output_dir, f'summary_report_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[可视化] 综合报告已生成: {filename}")
            return filename

        except Exception as e:
            print(f"[可视化] 生成综合报告失败: {e}")
            return ""


import numpy as np
