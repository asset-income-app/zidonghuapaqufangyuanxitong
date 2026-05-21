import pandas as pd
from typing import Dict
import os
from datetime import datetime
import json
from core.visualizer import DataVisualizer


class EnhancedExporter:
    def __init__(self, output_dir: str = "output", filename_prefix: str = "房源数据"):
        self.output_dir = output_dir
        self.filename_prefix = filename_prefix
        self.visualizer = DataVisualizer(os.path.join(output_dir, "charts"))
        os.makedirs(output_dir, exist_ok=True)

    def export_json(self, df: pd.DataFrame, stats: Dict, timestamp: str = None) -> str:
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        filename = os.path.join(self.output_dir, f"{self.filename_prefix}_{timestamp}.json")

        export_data = {
            'metadata': {
                'total_count': len(df),
                'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city': '三亚',
                'districts': ['吉阳区', '天涯区']
            },
            'statistics': stats,
            'houses': df.to_dict('records') if not df.empty else []
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"[导出] JSON文件已保存: {filename}")
        return filename

    def export_markdown(self, df: pd.DataFrame, stats: Dict, timestamp: str = None) -> str:
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        filename = os.path.join(self.output_dir, f"{self.filename_prefix}_{timestamp}.md")

        md_content = self._generate_markdown(df, stats)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"[导出] Markdown文件已保存: {filename}")
        return filename

    def _generate_markdown(self, df: pd.DataFrame, stats: Dict) -> str:
        md = f"""# 三亚房源数据报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 数据统计

| 指标 | 数值 |
|------|------|
| 总房源数 | {stats.get('总房源数', 0)} 套 |
| 平均总价 | {stats.get('平均总价(万)', 0):.2f} 万元 |
| 最低总价 | {stats.get('最低总价(万)', 0):.2f} 万元 |
| 最高总价 | {stats.get('最高总价(万)', 0):.2f} 万元 |
| 平均面积 | {stats.get('平均面积(㎡)', 0):.2f} ㎡ |

"""

        if '各区域房源数' in stats:
            md += "### 各区域房源分布\n\n"
            md += "| 区域 | 房源数 |\n|------|--------|\n"
            for district, count in stats['各区域房源数'].items():
                md += f"| {district} | {count} |\n"
            md += "\n"

        if '各网站房源数' in stats:
            md += "### 各网站房源来源\n\n"
            md += "| 网站 | 房源数 |\n|------|--------|\n"
            for source, count in stats['各网站房源数'].items():
                md += f"| {source} | {count} |\n"
            md += "\n"

        if not df.empty:
            md += "## 🏠 房源列表\n\n"
            md += "| 标题 | 区域 | 户型 | 面积 | 总价(万) | 来源 |\n"
            md += "|------|------|------|------|----------|------|\n"

            display_cols = ['标题', '区域', '户型', '面积', '总价(万)', '来源']
            available_cols = [col for col in display_cols if col in df.columns]

            for _, row in df.head(100).iterrows():
                values = []
                for col in available_cols:
                    value = row.get(col, '')
                    if pd.isna(value):
                        value = ''
                    else:
                        value = str(value)[:30]
                    values.append(value)
                md += "| " + " | ".join(values) + " |\n"

            if len(df) > 100:
                md += f"\n*注：仅显示前100条，共{len(df)}条数据*\n"

        md += "\n---\n\n"
        md += "*本报告由三亚房源智能爬取系统自动生成*\n"

        return md

    def export_with_charts(self, df: pd.DataFrame, stats: Dict, timestamp: str = None) -> Dict:
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        exported_files = {}

        exported_files['json'] = self.export_json(df, stats, timestamp)
        exported_files['markdown'] = self.export_markdown(df, stats, timestamp)

        if not df.empty:
            chart_files = self.visualizer.generate_all_charts(df)
            summary_chart = self.visualizer.create_summary_report(df, stats)
            if summary_chart:
                chart_files.append(summary_chart)
            exported_files['charts'] = chart_files

        return exported_files
