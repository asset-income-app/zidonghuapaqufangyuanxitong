import yaml
import os
from typing import Dict, List, Any
from datetime import datetime


class ConfigManager:
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        if not os.path.exists(self.config_path):
            print(f"[配置] 配置文件不存在: {self.config_path}")
            return self._get_default_config()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print(f"[配置] 已加载配置文件")
        return config

    def _get_default_config(self) -> Dict:
        return {
            'city': '三亚',
            'districts': ['吉阳区', '天涯区'],
            'price_range': {'min': 0, 'max': 2000000},
            'websites': {
                'lianjia': {'enabled': True, 'name': '链家网'},
                'anjuke': {'enabled': True, 'name': '安居客'},
                'wuba': {'enabled': True, 'name': '58同城'},
                'beike': {'enabled': True, 'name': '贝壳找房'}
            },
            'crawl_settings': {
                'max_pages': 50,
                'delay': 2,
                'timeout': 30,
                'retry_times': 3
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def update_price_range(self, min_price: float, max_price: float):
        self.set('price_range.min', min_price)
        self.set('price_range.max', max_price)
        self.save()

    def update_districts(self, districts: List[str]):
        self.set('districts', districts)
        self.save()

    def enable_website(self, website: str, enabled: bool = True):
        self.set(f'websites.{website}.enabled', enabled)
        self.save()

    def update_crawl_settings(self, **kwargs):
        for key, value in kwargs.items():
            self.set(f'crawl_settings.{key}', value)
        self.save()

    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        print(f"[配置] 配置已保存")

    def validate(self) -> bool:
        required_keys = ['city', 'districts', 'price_range', 'websites']
        for key in required_keys:
            if key not in self.config:
                print(f"[配置] 缺少必需配置项: {key}")
                return False

        if not self.config['districts']:
            print("[配置] 区域列表为空")
            return False

        if self.config['price_range']['min'] >= self.config['price_range']['max']:
            print("[配置] 价格范围设置错误")
            return False

        enabled_sites = [k for k, v in self.config['websites'].items() if v.get('enabled')]
        if not enabled_sites:
            print("[配置] 未启用任何网站")
            return False

        print("[配置] 配置验证通过")
        return True

    def get_enabled_websites(self) -> List[str]:
        return [k for k, v in self.config.get('websites', {}).items() if v.get('enabled')]

    def get_crawl_settings(self) -> Dict:
        return self.config.get('crawl_settings', {})

    def print_config(self):
        print("\n" + "="*60)
        print("当前配置:")
        print("="*60)
        print(f"城市: {self.get('city')}")
        print(f"区域: {', '.join(self.get('districts', []))}")
        print(f"价格范围: {self.get('price_range.min'):,} - {self.get('price_range.max'):,} 元")
        print(f"最大爬取页数: {self.get('crawl_settings.max_pages')}")
        print(f"请求间隔: {self.get('crawl_settings.delay')} 秒")
        print(f"启用的网站: {', '.join(self.get_enabled_websites())}")
        print("="*60 + "\n")
