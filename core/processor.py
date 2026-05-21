import pandas as pd
from typing import List, Dict, Optional
import re
from datetime import datetime


class DataProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.price_min = config.get('price_range', {}).get('min', 0)
        self.price_max = config.get('price_range', {}).get('max', 2000000)
        self.districts = config.get('districts', ['吉阳区', '天涯区'])

    def process_houses(self, houses: List[Dict]) -> pd.DataFrame:
        if not houses:
            return pd.DataFrame()

        df = pd.DataFrame(houses)
        df = self._clean_data(df)
        df = self._filter_data(df)
        df = self._deduplicate(df)
        df = self._sort_data(df)
        df = self._add_calculated_fields(df)

        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')
                df[col] = df[col].astype(str)
                df[col] = df[col].str.strip()

        if '总价(万)' in df.columns:
            df['总价(万)'] = pd.to_numeric(df['总价(万)'], errors='coerce')

        if '面积' in df.columns:
            df['面积'] = pd.to_numeric(df['面积'], errors='coerce')

        if '单价' in df.columns:
            df['单价_数值'] = df['单价'].apply(self._extract_unit_price)

        return df

    def _extract_unit_price(self, price_str: str) -> Optional[float]:
        if not price_str or pd.isna(price_str):
            return None
        try:
            numbers = re.findall(r'[\d.]+', str(price_str))
            if numbers:
                return float(numbers[0])
        except:
            pass
        return None

    def _filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        if '总价(万)' in df.columns:
            df = df[(df['总价(万)'] >= self.price_min / 10000) & 
                    (df['总价(万)'] <= self.price_max / 10000)]

        if '区域' in df.columns and self.districts:
            df = df[df['区域'].isin(self.districts)]

        if '标题' in df.columns:
            df = df[df['标题'] != '']
            df = df[~df['标题'].str.contains('测试|广告', na=False)]

        return df

    def _deduplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        subset = []
        for col in ['标题', '小区', '户型', '面积', '总价(万)']:
            if col in df.columns:
                subset.append(col)

        if subset:
            df = df.drop_duplicates(subset=subset, keep='first')
        else:
            df = df.drop_duplicates(keep='first')

        return df

    def _sort_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        if '总价(万)' in df.columns:
            df = df.sort_values('总价(万)', ascending=True)

        return df.reset_index(drop=True)

    def _add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df['爬取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if '面积' in df.columns and '总价(万)' in df.columns:
            df['每平米价格(万)'] = df.apply(
                lambda row: round(row['总价(万)'] / row['面积'], 2) 
                if pd.notna(row['面积']) and row['面积'] > 0 else None,
                axis=1
            )

        if '总价(万)' in df.columns:
            df['价格区间'] = df['总价(万)'].apply(self._get_price_range)

        return df

    def _get_price_range(self, price: float) -> str:
        if pd.isna(price):
            return "未知"
        if price < 50:
            return "50万以下"
        elif price < 100:
            return "50-100万"
        elif price < 150:
            return "100-150万"
        elif price < 200:
            return "150-200万"
        else:
            return "200万以上"

    def merge_dataframes(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        if not df_list:
            return pd.DataFrame()

        valid_dfs = [df for df in df_list if not df.empty]
        if not valid_dfs:
            return pd.DataFrame()

        merged = pd.concat(valid_dfs, ignore_index=True)
        merged = self._deduplicate(merged)
        merged = self._sort_data(merged)

        return merged

    def get_statistics(self, df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}

        stats = {
            '总房源数': len(df),
            '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        if '总价(万)' in df.columns:
            price_col = df['总价(万)'].dropna()
            if not price_col.empty:
                stats.update({
                    '平均总价(万)': round(price_col.mean(), 2),
                    '最低总价(万)': round(price_col.min(), 2),
                    '最高总价(万)': round(price_col.max(), 2),
                    '中位数总价(万)': round(price_col.median(), 2),
                })

        if '面积' in df.columns:
            area_col = df['面积'].dropna()
            if not area_col.empty:
                stats.update({
                    '平均面积(㎡)': round(area_col.mean(), 2),
                    '最小面积(㎡)': round(area_col.min(), 2),
                    '最大面积(㎡)': round(area_col.max(), 2),
                })

        if '区域' in df.columns:
            district_counts = df['区域'].value_counts().to_dict()
            stats['各区域房源数'] = district_counts

        if '来源' in df.columns:
            source_counts = df['来源'].value_counts().to_dict()
            stats['各网站房源数'] = source_counts

        if '户型' in df.columns:
            layout_counts = df['户型'].value_counts().head(10).to_dict()
            stats['热门户型'] = layout_counts

        return stats
