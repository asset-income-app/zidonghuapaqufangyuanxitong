# API 开发者文档

## 目录

1. [快速开始](#快速开始)
2. [核心模块](#核心模块)
3. [爬虫API](#爬虫api)
4. [数据处理API](#数据处理api)
5. [导出API](#导出api)
6. [工具类API](#工具类api)
7. [高级用法](#高级用法)

---

## 快速开始

### 基础使用

```python
from main import HouseCrawlerEngine

# 创建爬虫引擎
engine = HouseCrawlerEngine()

# 运行爬虫
result = engine.run()

# 获取结果
df = result['dataframe']
stats = result['statistics']
files = result['files']
```

### 自定义配置

```python
from utils import ConfigManager

# 加载配置
config = ConfigManager()

# 修改价格范围
config.update_price_range(min_price=500000, max_price=1500000)

# 修改区域
config.update_districts(['吉阳区'])

# 禁用某个网站
config.enable_website('wuba', enabled=False)

# 查看配置
config.print_config()
```

---

## 核心模块

### HouseCrawlerEngine

主引擎类，负责协调所有模块。

#### 初始化参数

```python
HouseCrawlerEngine(config_path: str = "config/settings.yaml")
```

- `config_path`: 配置文件路径

#### 主要方法

##### run()

执行完整的爬取流程。

```python
result = engine.run()
```

**返回值**:
```python
{
    'dataframe': pd.DataFrame,  # 处理后的数据
    'statistics': Dict,         # 统计信息
    'files': Dict[str, str]     # 导出的文件路径
}
```

##### crawl_all_sites()

爬取所有网站数据。

```python
houses = engine.crawl_all_sites()
```

**返回值**: `List[Dict]` - 房源列表

##### process_and_export(houses)

处理并导出数据。

```python
result = engine.process_and_export(houses)
```

---

## 爬虫API

### BaseSpider

所有爬虫的基类。

#### 初始化

```python
BaseSpider(config: Dict)
```

**config参数**:
- `base_url`: 网站基础URL
- `name`: 网站名称
- `delay`: 请求间隔（秒）
- `timeout`: 请求超时时间
- `retry_times`: 重试次数

#### 核心方法

##### get_page(url, params)

获取页面内容。

```python
soup = spider.get_page("https://example.com/houses", params={"page": 1})
```

**参数**:
- `url`: 请求URL
- `params`: URL参数（可选）

**返回值**: `BeautifulSoup` 对象或 `None`

##### get_house_list(district, page)

获取房源列表（抽象方法，需子类实现）。

```python
houses = spider.get_house_list("吉阳区", page=1)
```

**参数**:
- `district`: 区域名称
- `page`: 页码

**返回值**: `List[Dict]` - 房源字典列表

##### get_house_detail(house_url)

获取房源详情（抽象方法，需子类实现）。

```python
detail = spider.get_house_detail("https://example.com/house/123")
```

**返回值**: `Dict` - 房源详情

#### 工具方法

##### parse_price(price_str)

解析价格字符串。

```python
price = spider.parse_price("150万")  # 返回 150.0
```

##### parse_area(area_str)

解析面积字符串。

```python
area = spider.parse_area("120平米")  # 返回 120.0
```

##### clean_text(text)

清理文本。

```python
text = spider.clean_text("  hello\nworld  ")  # 返回 "helloworld"
```

### 具体爬虫类

#### LianjiaSpider

链家网爬虫。

```python
from spiders import LianjiaSpider

config = {
    'base_url': 'https://sanya.lianjia.com',
    'name': '链家网',
    'delay': 2
}

spider = LianjiaSpider(config)
houses = spider.get_house_list("吉阳区", page=1)
```

#### AnjukeSpider

安居客爬虫。

```python
from spiders import AnjukeSpider

spider = AnjukeSpider(config)
```

#### WubaSpider

58同城爬虫。

```python
from spiders import WubaSpider

spider = WubaSpider(config)
```

#### BeikeSpider

贝壳找房爬虫。

```python
from spiders import BeikeSpider

spider = BeikeSpider(config)
```

---

## 数据处理API

### DataProcessor

数据处理类，负责清洗、筛选、去重。

#### 初始化

```python
from core import DataProcessor

processor = DataProcessor(config)
```

#### 主要方法

##### process_houses(houses)

处理房源数据。

```python
df = processor.process_houses(houses)
```

**参数**:
- `houses`: `List[Dict]` - 原始房源列表

**返回值**: `pd.DataFrame` - 处理后的数据框

##### merge_dataframes(df_list)

合并多个数据框。

```python
merged_df = processor.merge_dataframes([df1, df2, df3])
```

##### get_statistics(df)

获取统计信息。

```python
stats = processor.get_statistics(df)
```

**返回值**:
```python
{
    '总房源数': int,
    '平均总价(万)': float,
    '最低总价(万)': float,
    '最高总价(万)': float,
    '平均面积(㎡)': float,
    '各区域房源数': Dict[str, int],
    '各网站房源数': Dict[str, int],
    '热门户型': Dict[str, int]
}
```

---

## 导出API

### Exporter

基础导出类。

#### 初始化

```python
from core import Exporter

exporter = Exporter(output_dir="output", filename_prefix="房源数据")
```

#### 主要方法

##### export_all(df, stats)

导出所有格式。

```python
files = exporter.export_all(df, stats)
```

**返回值**:
```python
{
    'excel': 'path/to/file.xlsx',
    'csv': 'path/to/file.csv',
    'pdf': 'path/to/file.pdf',
    'html': 'path/to/file.html'
}
```

##### export_excel(df, stats, timestamp)

导出Excel文件。

```python
file_path = exporter.export_excel(df, stats)
```

##### export_csv(df, timestamp)

导出CSV文件。

```python
file_path = exporter.export_csv(df)
```

##### export_pdf(df, stats, timestamp)

导出PDF文件。

```python
file_path = exporter.export_pdf(df, stats)
```

##### export_html(df, stats, timestamp)

导出HTML文件。

```python
file_path = exporter.export_html(df, stats)
```

### EnhancedExporter

增强导出类，支持更多格式和图表。

#### 初始化

```python
from core import EnhancedExporter

exporter = EnhancedExporter(output_dir="output", filename_prefix="房源数据")
```

#### 主要方法

##### export_json(df, stats, timestamp)

导出JSON文件。

```python
file_path = exporter.export_json(df, stats)
```

##### export_markdown(df, stats, timestamp)

导出Markdown文件。

```python
file_path = exporter.export_markdown(df, stats)
```

##### export_with_charts(df, stats, timestamp)

导出数据并生成图表。

```python
files = exporter.export_with_charts(df, stats)
```

**返回值**:
```python
{
    'json': 'path/to/file.json',
    'markdown': 'path/to/file.md',
    'charts': ['path/to/chart1.png', 'path/to/chart2.png', ...]
}
```

### DataVisualizer

数据可视化类。

#### 初始化

```python
from core import DataVisualizer

visualizer = DataVisualizer(output_dir="output/charts")
```

#### 主要方法

##### generate_all_charts(df)

生成所有图表。

```python
chart_files = visualizer.generate_all_charts(df)
```

**返回值**: `List[str]` - 图表文件路径列表

##### plot_price_distribution(df)

生成价格分布图。

```python
file_path = visualizer.plot_price_distribution(df)
```

##### plot_area_distribution(df)

生成面积分布图。

```python
file_path = visualizer.plot_area_distribution(df)
```

##### create_summary_report(df, stats)

创建综合报告。

```python
file_path = visualizer.create_summary_report(df, stats)
```

---

## 工具类API

### ConfigManager

配置管理类。

#### 初始化

```python
from utils import ConfigManager

config = ConfigManager(config_path="config/settings.yaml")
```

#### 主要方法

##### get(key, default)

获取配置值。

```python
city = config.get('city')  # '三亚'
max_price = config.get('price_range.max')  # 2000000
```

##### set(key, value)

设置配置值。

```python
config.set('city', '海口')
```

##### update_price_range(min_price, max_price)

更新价格范围。

```python
config.update_price_range(500000, 1500000)
```

##### update_districts(districts)

更新区域列表。

```python
config.update_districts(['吉阳区', '天涯区', '海棠区'])
```

##### enable_website(website, enabled)

启用/禁用网站。

```python
config.enable_website('lianjia', enabled=True)
```

##### validate()

验证配置。

```python
is_valid = config.validate()
```

##### save()

保存配置。

```python
config.save()
```

### Logger

日志工具。

#### 使用方法

```python
from utils import logger, setup_logger

# 使用默认logger
logger.info("这是一条信息")
logger.warning("这是一条警告")
logger.error("这是一条错误")

# 创建自定义logger
custom_logger = setup_logger("MyCrawler", log_dir="logs")
custom_logger.info("自定义日志")
```

### ProxyPool

代理池管理。

#### 初始化

```python
from utils import ProxyPool

proxy_pool = ProxyPool(proxies=[
    'http://proxy1:8080',
    'http://proxy2:8080'
])
```

#### 主要方法

##### get_proxy()

获取一个代理。

```python
proxy = proxy_pool.get_proxy()
```

##### mark_failed(proxy)

标记代理失败。

```python
proxy_pool.mark_failed('http://proxy1:8080')
```

##### mark_success(proxy)

标记代理成功。

```python
proxy_pool.mark_success('http://proxy1:8080')
```

### RetryStrategy

重试策略。

#### 初始化

```python
from utils import RetryStrategy

strategy = RetryStrategy(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0
)
```

#### 主要方法

##### get_delay(attempt)

获取重试延迟。

```python
delay = strategy.get_delay(attempt=1)
```

##### should_retry(attempt, exception)

判断是否应该重试。

```python
should_retry = strategy.should_retry(attempt=1, exception=e)
```

### RateLimiter

速率限制器。

#### 初始化

```python
from utils import RateLimiter

limiter = RateLimiter(requests_per_second=2.0)
```

#### 使用方法

```python
for url in urls:
    limiter.wait()  # 等待到合适的速率
    response = requests.get(url)
```

### ProgressBar & TaskProgress

进度显示工具。

#### ProgressBar

```python
from utils import ProgressBar

with ProgressBar(total=100, desc="爬取进度") as pbar:
    for i in range(100):
        # 执行任务
        pbar.update(1)
```

#### TaskProgress

```python
from utils import TaskProgress

progress = TaskProgress()
progress.start_task("爬取链家", total=50)

for i in range(50):
    # 执行任务
    progress.update("爬取链家", 1)

progress.complete_task("爬取链家")
```

---

## 高级用法

### 自定义爬虫

创建自定义爬虫需要继承 `BaseSpider`：

```python
from spiders.base_spider import BaseSpider
from typing import List, Dict

class MyCustomSpider(BaseSpider):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.search_url = f"{self.base_url}/search"

    def get_house_list(self, district: str, page: int = 1) -> List[Dict]:
        houses = []
        url = f"{self.search_url}/{district}/page{page}"

        soup = self.get_page(url)
        if not soup:
            return houses

        # 解析逻辑
        items = soup.select('div.house-item')
        for item in items:
            house = {
                '标题': self.clean_text(item.select_one('h2').text),
                '价格': self.parse_price(item.select_one('.price').text),
                # ... 更多字段
            }
            houses.append(house)

        return houses

    def get_house_detail(self, house_url: str) -> Dict:
        # 实现详情获取逻辑
        pass
```

### 使用代理池

```python
from utils import ProxyPool, RetryStrategy

# 创建代理池
proxy_pool = ProxyPool([
    'http://proxy1:8080',
    'http://proxy2:8080'
])

# 创建重试策略
retry_strategy = RetryStrategy(max_retries=3)

# 在爬虫中使用
for attempt in range(retry_strategy.max_retries):
    proxy = proxy_pool.get_proxy()
    try:
        response = requests.get(url, proxies={'http': proxy})
        proxy_pool.mark_success(proxy)
        break
    except Exception as e:
        proxy_pool.mark_failed(proxy)
        if retry_strategy.should_retry(attempt, e):
            time.sleep(retry_strategy.get_delay(attempt))
```

### 异步爬取

```python
import asyncio
import aiohttp
from utils import RateLimiter

async def fetch_page(session, url, limiter):
    limiter.wait()
    async with session.get(url) as response:
        return await response.text()

async def crawl_async(urls):
    limiter = RateLimiter(requests_per_second=5.0)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url, limiter) for url in urls]
        results = await asyncio.gather(*tasks)

    return results

# 运行
urls = ['http://example.com/page1', 'http://example.com/page2']
results = asyncio.run(crawl_async(urls))
```

### 数据分析示例

```python
import pandas as pd
from core import DataProcessor

# 加载数据
df = pd.read_excel('output/房源数据.xlsx')

# 价格分析
price_analysis = df['总价(万)'].describe()
print(price_analysis)

# 区域对比
district_stats = df.groupby('区域').agg({
    '总价(万)': ['mean', 'median', 'count'],
    '面积': 'mean'
})
print(district_stats)

# 性价比分析
df['性价比'] = df['面积'] / df['总价(万)']
best_deals = df.nlargest(10, '性价比')
print(best_deals[['标题', '面积', '总价(万)', '性价比']])
```

### 自定义数据处理

```python
from core import DataProcessor

class CustomProcessor(DataProcessor):
    def _add_calculated_fields(self, df):
        df = super()._add_calculated_fields(df)

        # 添加自定义字段
        df['每平米价格'] = df['总价(万)'] / df['面积'] * 10000
        df['性价比评分'] = self._calculate_score(df)

        return df

    def _calculate_score(self, df):
        # 自定义评分逻辑
        score = 0
        if df['朝向'].str.contains('南'):
            score += 10
        if df['楼层'].str.contains('中'):
            score += 5
        return score

# 使用自定义处理器
processor = CustomProcessor(config)
df = processor.process_houses(houses)
```

---

## 完整示例

### 示例1：基础爬取

```python
from main import HouseCrawlerEngine

# 创建引擎
engine = HouseCrawlerEngine()

# 运行
result = engine.run()

# 打印结果
print(f"共爬取 {len(result['dataframe'])} 条房源")
print(f"平均价格: {result['statistics']['平均总价(万)']} 万元")
print(f"文件已保存: {result['files']}")
```

### 示例2：自定义配置爬取

```python
from utils import ConfigManager
from main import HouseCrawlerEngine

# 修改配置
config = ConfigManager()
config.update_price_range(800000, 1500000)
config.update_districts(['吉阳区'])
config.enable_website('wuba', enabled=False)
config.update_crawl_settings(max_pages=20, delay=3)

# 运行
engine = HouseCrawlerEngine()
result = engine.run()
```

### 示例3：数据分析

```python
import pandas as pd
from core import DataVisualizer

# 加载数据
df = pd.read_excel('output/房源数据.xlsx')

# 生成可视化
visualizer = DataVisualizer()
chart_files = visualizer.generate_all_charts(df)

print(f"生成了 {len(chart_files)} 个图表")
```

### 示例4：增量爬取

```python
import pandas as pd
from datetime import datetime
from main import HouseCrawlerEngine

# 加载历史数据
try:
    old_df = pd.read_excel('output/最新房源.xlsx')
except:
    old_df = pd.DataFrame()

# 爬取新数据
engine = HouseCrawlerEngine()
result = engine.run()
new_df = result['dataframe']

# 合并去重
if not old_df.empty:
    combined = pd.concat([old_df, new_df]).drop_duplicates(
        subset=['标题', '小区', '户型', '面积'],
        keep='last'
    )
else:
    combined = new_df

# 保存
combined.to_excel('output/最新房源.xlsx', index=False)
print(f"更新后共 {len(combined)} 条房源")
```

---

## 错误处理

### 常见错误

#### 1. 网络错误

```python
from utils import RetryStrategy
import requests

strategy = RetryStrategy(max_retries=3)

for attempt in range(strategy.max_retries):
    try:
        response = requests.get(url, timeout=10)
        break
    except requests.RequestException as e:
        if strategy.should_retry(attempt, e):
            time.sleep(strategy.get_delay(attempt))
        else:
            raise
```

#### 2. 解析错误

```python
from utils import logger

try:
    price = spider.parse_price(price_text)
except Exception as e:
    logger.warning(f"解析价格失败: {price_text}, 错误: {e}")
    price = None
```

#### 3. 配置错误

```python
from utils import ConfigManager

config = ConfigManager()
if not config.validate():
    print("配置有误，请检查")
    exit(1)
```

---

## 性能优化

### 1. 减少请求次数

```python
# 只爬取需要的页数
config.update_crawl_settings(max_pages=10)
```

### 2. 使用并发

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(spider.get_house_list, district, page)
               for district in districts
               for page in range(1, max_pages+1)]
    results = [f.result() for f in futures]
```

### 3. 缓存数据

```python
import pickle
import os

def load_cache(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return None

def save_cache(data, cache_file):
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
```

---

## 最佳实践

1. **遵守robots.txt**: 尊重网站的爬虫协议
2. **设置合理延迟**: 避免对网站造成压力
3. **使用代理池**: 分散请求来源
4. **错误处理**: 完善的异常捕获和重试机制
5. **数据验证**: 爬取后验证数据完整性
6. **定期更新**: 定期运行以获取最新数据
7. **备份数据**: 保存历史数据用于对比分析

---

## 更新日志

### v2.0.0 (2024-01-01)
- 添加代理池支持
- 添加异步爬取
- 添加数据可视化
- 添加JSON、Markdown导出
- 完善日志系统
- 添加进度显示
- 性能优化

### v1.0.0 (2024-01-01)
- 初始版本
