import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import json


class Database:
    def __init__(self, db_path: str = "data/houses.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS houses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT,
                district TEXT,
                community TEXT,
                location TEXT,
                layout TEXT,
                area REAL,
                orientation TEXT,
                floor TEXT,
                price REAL,
                unit_price TEXT,
                tags TEXT,
                source TEXT,
                house_info TEXT,
                crawl_time TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, community, layout, area)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawl_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                end_time TEXT,
                total_houses INTEGER,
                avg_price REAL,
                status TEXT,
                error TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_district ON houses(district)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_price ON houses(price)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_source ON houses(source)
        ''')

        conn.commit()
        conn.close()

    def insert_house(self, house: Dict) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO houses 
                (title, link, district, community, location, layout, area, 
                 orientation, floor, price, unit_price, tags, source, 
                 house_info, crawl_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                house.get('标题', ''),
                house.get('链接', ''),
                house.get('区域', ''),
                house.get('小区', ''),
                house.get('位置', ''),
                house.get('户型', ''),
                house.get('面积'),
                house.get('朝向', ''),
                house.get('楼层', ''),
                house.get('总价(万)'),
                house.get('单价', ''),
                house.get('标签', ''),
                house.get('来源', ''),
                house.get('房源信息', ''),
                house.get('爬取时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ))

            house_id = cursor.lastrowid
            conn.commit()
            return house_id

        except Exception as e:
            print(f"[数据库] 插入数据失败: {e}")
            return -1

        finally:
            conn.close()

    def insert_houses_batch(self, houses: List[Dict]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        success_count = 0

        try:
            for house in houses:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO houses 
                        (title, link, district, community, location, layout, area, 
                         orientation, floor, price, unit_price, tags, source, 
                         house_info, crawl_time)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        house.get('标题', ''),
                        house.get('链接', ''),
                        house.get('区域', ''),
                        house.get('小区', ''),
                        house.get('位置', ''),
                        house.get('户型', ''),
                        house.get('面积'),
                        house.get('朝向', ''),
                        house.get('楼层', ''),
                        house.get('总价(万)'),
                        house.get('单价', ''),
                        house.get('标签', ''),
                        house.get('来源', ''),
                        house.get('房源信息', ''),
                        house.get('爬取时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    ))
                    success_count += 1
                except:
                    continue

            conn.commit()
            return success_count

        except Exception as e:
            print(f"[数据库] 批量插入失败: {e}")
            return success_count

        finally:
            conn.close()

    def get_houses(self, filters: Dict = None, limit: int = 100) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM houses WHERE 1=1"
            params = []

            if filters:
                if 'district' in filters:
                    query += " AND district = ?"
                    params.append(filters['district'])

                if 'min_price' in filters:
                    query += " AND price >= ?"
                    params.append(filters['min_price'])

                if 'max_price' in filters:
                    query += " AND price <= ?"
                    params.append(filters['max_price'])

                if 'source' in filters:
                    query += " AND source = ?"
                    params.append(filters['source'])

            query += f" ORDER BY created_at DESC LIMIT {limit}"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            columns = [description[0] for description in cursor.description]
            houses = [dict(zip(columns, row)) for row in rows]

            return houses

        finally:
            conn.close()

    def get_statistics(self) -> Dict:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            stats = {}

            cursor.execute("SELECT COUNT(*) FROM houses")
            stats['total_count'] = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(price) FROM houses WHERE price IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['avg_price'] = round(result, 2) if result else 0

            cursor.execute("SELECT MIN(price) FROM houses WHERE price IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['min_price'] = result if result else 0

            cursor.execute("SELECT MAX(price) FROM houses WHERE price IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['max_price'] = result if result else 0

            cursor.execute("SELECT AVG(area) FROM houses WHERE area IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['avg_area'] = round(result, 2) if result else 0

            cursor.execute("SELECT district, COUNT(*) FROM houses GROUP BY district")
            stats['district_distribution'] = dict(cursor.fetchall())

            cursor.execute("SELECT source, COUNT(*) FROM houses GROUP BY source")
            stats['source_distribution'] = dict(cursor.fetchall())

            return stats

        finally:
            conn.close()

    def search_houses(self, keyword: str, limit: int = 50) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT * FROM houses 
                WHERE title LIKE ? OR community LIKE ? OR location LIKE ?
                ORDER BY created_at DESC 
                LIMIT ?
            """
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term, search_term, search_term, limit))

            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            houses = [dict(zip(columns, row)) for row in rows]

            return houses

        finally:
            conn.close()

    def delete_old_houses(self, days: int = 30):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM houses 
                WHERE created_at < datetime('now', ?)
            ''', (f'-{days} days',))

            deleted_count = cursor.rowcount
            conn.commit()

            return deleted_count

        finally:
            conn.close()

    def add_crawl_history(self, start_time: str, end_time: str, 
                         total_houses: int, avg_price: float, 
                         status: str, error: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO crawl_history 
                (start_time, end_time, total_houses, avg_price, status, error)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (start_time, end_time, total_houses, avg_price, status, error))

            conn.commit()

        finally:
            conn.close()

    def get_crawl_history(self, limit: int = 10) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(f'''
                SELECT * FROM crawl_history 
                ORDER BY created_at DESC 
                LIMIT {limit}
            ''')

            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            history = [dict(zip(columns, row)) for row in rows]

            return history

        finally:
            conn.close()

    def export_to_dataframe(self, filters: Dict = None) -> pd.DataFrame:
        houses = self.get_houses(filters, limit=10000)

        if not houses:
            return pd.DataFrame()

        df = pd.DataFrame(houses)

        column_mapping = {
            'title': '标题',
            'link': '链接',
            'district': '区域',
            'community': '小区',
            'location': '位置',
            'layout': '户型',
            'area': '面积',
            'orientation': '朝向',
            'floor': '楼层',
            'price': '总价(万)',
            'unit_price': '单价',
            'tags': '标签',
            'source': '来源',
            'house_info': '房源信息',
            'crawl_time': '爬取时间'
        }

        df = df.rename(columns=column_mapping)

        return df
