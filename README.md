# 🏠 三亚房源智能爬取系统 v2.0

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/yourusername/house-crawler)

**一个工业级的房源数据爬取、分析、可视化、管理系统**

[快速开始](#快速开始) • [功能特性](#功能特性) • [Web界面](#web界面) • [文档](#文档) • [贡献](#贡献)

</div>

---

## 📖 简介

这是一个专为三亚房产市场设计的**工业级智能爬取系统**，采用现代化架构，支持Web界面操作、数据库持久化、定时任务、邮件通知等企业级功能。

### 🎯 适用场景

- 🏠 **购房者** - 快速获取市场房源信息，对比分析
- 📊 **数据分析师** - 获取房产数据进行市场分析
- 💼 **房产从业者** - 了解市场动态和价格趋势
- 🔧 **开发者** - 学习爬虫技术，二次开发
- 🏢 **企业用户** - 部署到服务器，定时爬取，自动报告

---

## ✨ 功能特性

### 核心功能

- 🌐 **多网站支持** - 链家、安居客、58同城、贝壳找房
- 🎯 **智能筛选** - 按区域、价格、户型等条件自动筛选
- 🧹 **数据清洗** - 自动去重、格式化、数据验证
- 📊 **数据可视化** - 自动生成统计图表和分析报告
- 💾 **多格式导出** - Excel、CSV、PDF、HTML、JSON、Markdown、Word

### 🆕 v2.0 新增功能

- 🖥️ **Web界面** - 现代化的Web操作界面，支持浏览器访问
- 🗄️ **数据库支持** - SQLite数据库持久化存储
- ⏰ **定时任务** - 自动定期爬取，支持Cron表达式
- 📧 **邮件通知** - 爬取完成自动发送邮件报告
- 📈 **数据对比** - 对比不同时间段的数据变化
- 🔄 **增量更新** - 只更新新增数据，节省时间

### 高级特性

- 🚀 **性能优化** - 支持并发爬取、代理池、速率控制
- 📈 **数据分析** - 价格趋势、区域对比、性价比分析
- 🔧 **灵活配置** - YAML配置文件，支持热更新
- 📝 **完善日志** - 详细日志记录，便于调试
- 🎨 **美观报告** - 自动生成专业的数据报告
- 🔐 **安全可靠** - 反爬虫机制，智能重试

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- 网络连接

### 安装方式

#### 方式一：使用启动菜单（最推荐）

```bash
# Windows用户：双击运行
启动菜单.bat

# 然后选择：
#   1. 使用模拟数据测试（推荐新手）
#   2. 启动Web界面
#   3. 真实爬取（需要网络）
#   4. 系统验证
```

#### 方式二：模拟数据测试（推荐新手）

```bash
# Windows用户：双击运行
使用模拟数据测试.bat

# 或命令行运行
python main.py --mock
```

**优点：**
- 无需网络连接
- 快速测试所有功能
- 了解数据格式和处理流程

#### 方式三：Web界面启动

```bash
# Windows用户：双击运行
启动Web界面.bat

# 或命令行运行
pip install -r requirements.txt
cd web
python app.py

# 访问 http://localhost:5000
```

#### 方式四：命令行启动

```bash
# 安装依赖
pip install -r requirements.txt

# 运行爬虫（真实数据）
python main.py

# 运行爬虫（模拟数据）
python main.py --mock

# 或使用交互式菜单
python run.py
```

#### 方式五：高级工具

```bash
# 运行高级工具菜单
python tools/advanced_tools.py
```

---

## 🖥️ Web界面

### 功能亮点

- 📊 **实时监控** - 实时查看爬取进度和状态
- 📈 **数据可视化** - 自动生成图表和分析
- ⚙️ **在线配置** - 无需修改配置文件
- 📁 **文件管理** - 在线查看和下载文件
- 🔍 **数据搜索** - 快速搜索房源信息

### 访问方式

```bash
# 启动Web服务器
python web/app.py

# 浏览器访问
http://localhost:5000
```

### API接口

Web界面提供完整的RESTful API：

- `GET /api/config` - 获取配置
- `POST /api/config` - 更新配置
- `POST /api/start` - 启动爬虫
- `GET /api/status` - 获取状态
- `GET /api/result` - 获取结果
- `GET /api/files` - 文件列表
- `GET /api/statistics` - 统计信息

---

## 📊 使用示例

### 基础爬取

```python
from main import HouseCrawlerEngine

engine = HouseCrawlerEngine()
result = engine.run()

# 获取数据
df = result['dataframe']
stats = result['statistics']
files = result['files']
```

### 使用数据库

```python
from core.database import Database

db = Database()

# 插入数据
db.insert_houses_batch(houses)

# 查询数据
houses = db.get_houses({'district': '吉阳区', 'max_price': 150})

# 搜索
results = db.search_houses('海景')

# 统计
stats = db.get_statistics()
```

### 定时任务

```python
from core.scheduler import TaskScheduler

scheduler = TaskScheduler()

# 每天8点执行
scheduler.add_crawl_job('daily', cron_expression='0 8 * * *')

# 每6小时执行
scheduler.add_crawl_job('hourly', interval_hours=6)
```

### 邮件通知

```python
from core.notifier import EmailNotifier

notifier = EmailNotifier(
    smtp_server='smtp.qq.com',
    smtp_port=587,
    sender_email='your@email.com',
    sender_password='password'
)

# 发送报告
notifier.send_crawl_report(
    to_emails=['receiver@email.com'],
    stats=stats,
    file_path='report.xlsx'
)
```

---

## ⚙️ 配置说明

配置文件位于 `config/settings.yaml`

### 基本配置

```yaml
city: "三亚"
districts:
  - "吉阳区"
  - "天涯区"

price_range:
  min: 0
  max: 2000000  # 200万以下
```

### 网站配置

```yaml
websites:
  lianjia:
    enabled: true
    name: "链家网"
  anjuke:
    enabled: true
    name: "安居客"
  wuba:
    enabled: true
    name: "58同城"
  beike:
    enabled: true
    name: "贝壳找房"
```

### 爬取设置

```yaml
crawl_settings:
  max_pages: 50        # 每个网站每个区域最大爬取页数
  delay: 2             # 请求间隔（秒）
  timeout: 30          # 请求超时时间
  retry_times: 3       # 失败重试次数
```

---

## 📁 项目结构

```
自动化爬取房源/
├── config/                 # 配置文件
│   └── settings.yaml
├── spiders/               # 爬虫模块
│   ├── base_spider.py     # 爬虫基类
│   ├── lianjia.py         # 链家爬虫
│   ├── anjuke.py          # 安居客爬虫
│   ├── wuba.py            # 58同城爬虫
│   └── beike.py           # 贝壳爬虫
├── core/                  # 核心模块
│   ├── processor.py       # 数据处理
│   ├── exporter.py        # 导出模块
│   ├── visualizer.py      # 数据可视化
│   ├── enhanced_exporter.py # 增强导出
│   ├── database.py        # 数据库管理
│   ├── scheduler.py       # 定时任务
│   ├── notifier.py        # 邮件通知
│   └── word_exporter.py   # Word导出
├── web/                   # Web界面
│   ├── app.py             # Flask应用
│   └── templates/         # 前端模板
├── utils/                 # 工具模块
│   ├── logger.py          # 日志系统
│   ├── proxy_pool.py      # 代理池
│   ├── progress.py        # 进度显示
│   └── config_manager.py  # 配置管理
├── tools/                 # 工具脚本
│   └── advanced_tools.py  # 高级工具
├── docs/                  # 文档
│   ├── API文档.md
│   ├── 性能优化指南.md
│   ├── 常见问题.md
│   ├── 更新日志.md
│   └── 贡献指南.md
├── tests/                 # 测试
│   └── test_system.py
├── examples/              # 示例
│   └── examples.py
├── output/                # 输出目录
├── logs/                  # 日志目录
├── data/                  # 数据库目录
├── main.py                # 主程序
├── run.py                 # 交互式菜单
├── 启动.bat               # Windows一键启动
├── 启动Web界面.bat        # Web界面启动
├── requirements.txt       # Python依赖
└── README.md              # 本文件
```

---

## 📚 文档

- 📖 [API文档](docs/API文档.md) - 完整的API参考
- 🚀 [性能优化指南](docs/性能优化指南.md) - 性能调优技巧
- ❓ [常见问题](docs/常见问题.md) - 问题解答
- 📝 [更新日志](docs/更新日志.md) - 版本历史
- 🤝 [贡献指南](docs/贡献指南.md) - 如何贡献代码

---

## 🎯 使用场景

### 场景1：个人购房

```bash
# 1. 启动Web界面
启动Web界面.bat

# 2. 配置需求
价格范围: 100-150万
区域: 吉阳区

# 3. 开始爬取
点击"开始爬取"按钮

# 4. 查看分析
查看价格分布、区域对比等图表

# 5. 导出数据
下载Excel文件，进一步筛选
```

### 场景2：市场监控

```python
# 设置定时任务，每天爬取
scheduler.add_crawl_job('daily', cron_expression='0 8 * * *')

# 配置邮件通知
notifier = EmailNotifier(...)

# 自动发送报告
# 每天早上8点自动爬取并发送邮件
```

### 场景3：数据分析

```python
# 使用数据库
db = Database()

# 获取历史数据
df = db.export_to_dataframe()

# 分析价格趋势
price_trend = df.groupby('爬取时间')['总价(万)'].mean()

# 区域对比
district_stats = df.groupby('区域').agg({
    '总价(万)': 'mean',
    '面积': 'mean'
})
```

---

## 🧪 测试

运行测试脚本验证系统功能：

```bash
python tests/test_system.py
```

测试包括：
- ✅ 配置管理
- ✅ 爬虫功能
- ✅ 数据处理
- ✅ 导出功能
- ✅ 日志系统
- ✅ 数据库操作
- ✅ Web界面

---

## 🤝 贡献

欢迎贡献代码、报告Bug、提出建议！

请查看 [贡献指南](docs/贡献指南.md) 了解详情。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## ⚠️ 免责声明

本项目仅供学习和研究使用，不得用于商业用途。使用本系统时：

- ✅ 请遵守目标网站的robots.txt协议
- ✅ 设置合理的请求频率
- ✅ 尊重网站的服务条款
- ❌ 不得大规模爬取
- ❌ 不得倒卖数据
- ❌ 不得用于商业目的

使用者需自行承担法律责任。

---

## 🌟 主要特性对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 多网站爬取 | ✅ | ✅ |
| 数据清洗 | ✅ | ✅ |
| Excel导出 | ✅ | ✅ |
| PDF导出 | ✅ | ✅ |
| HTML导出 | ✅ | ✅ |
| Web界面 | ❌ | ✅ |
| 数据库存储 | ❌ | ✅ |
| 定时任务 | ❌ | ✅ |
| 邮件通知 | ❌ | ✅ |
| 数据对比 | ❌ | ✅ |
| Word导出 | ❌ | ✅ |
| 数据可视化 | ❌ | ✅ |
| 代理池 | ❌ | ✅ |
| 进度显示 | ❌ | ✅ |

---

## 📞 联系方式

- 📧 Email: your.email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/house-crawler/issues)

---

## 🌟 Star History

如果这个项目对您有帮助，请给一个 ⭐️ Star！

---

<div align="center">

**Made with ❤️ by [Your Name]**

**v2.0 - 更强大、更智能、更易用**

</div>
