from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
import sys
import threading
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import HouseCrawlerEngine
from core import DataProcessor, DataVisualizer
from utils import ConfigManager, logger

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

crawler_status = {
    'running': False,
    'progress': 0,
    'current_task': '',
    'total_houses': 0,
    'start_time': None,
    'error': None
}

crawler_result = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    config = ConfigManager()
    return jsonify({
        'city': config.get('city'),
        'districts': config.get('districts'),
        'price_range': config.get('price_range'),
        'websites': config.get('websites'),
        'crawl_settings': config.get('crawl_settings')
    })


@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    config = ConfigManager()

    if 'price_range' in data:
        config.update_price_range(
            data['price_range']['min'],
            data['price_range']['max']
        )

    if 'districts' in data:
        config.update_districts(data['districts'])

    if 'max_pages' in data:
        config.update_crawl_settings(max_pages=data['max_pages'])

    return jsonify({'success': True, 'message': '配置已更新'})


@app.route('/api/start', methods=['POST'])
def start_crawler():
    global crawler_status, crawler_result

    if crawler_status['running']:
        return jsonify({'success': False, 'message': '爬虫已在运行中'})

    use_mock = request.json.get('use_mock_data', False) if request.json else False

    def run_crawler():
        global crawler_status, crawler_result

        try:
            crawler_status['running'] = True
            crawler_status['progress'] = 0
            crawler_status['current_task'] = '初始化爬虫...'
            crawler_status['start_time'] = datetime.now()
            crawler_status['error'] = None

            engine = HouseCrawlerEngine()

            if use_mock:
                crawler_status['current_task'] = '使用模拟数据（测试模式）...'
            else:
                crawler_status['current_task'] = '开始爬取数据...'
            crawler_status['progress'] = 10

            result = engine.run(use_mock_data=use_mock)

            crawler_status['progress'] = 80
            crawler_status['current_task'] = '处理数据...'

            if result:
                crawler_result = result
                crawler_status['total_houses'] = len(result['dataframe'])
                crawler_status['progress'] = 100
                crawler_status['current_task'] = '完成！'
            else:
                crawler_status['error'] = '未获取到数据'

        except Exception as e:
            logger.error(f"爬虫运行错误: {e}")
            crawler_status['error'] = str(e)

        finally:
            crawler_status['running'] = False

    thread = threading.Thread(target=run_crawler)
    thread.daemon = True
    thread.start()

    return jsonify({'success': True, 'message': '爬虫已启动'})


@app.route('/api/status', methods=['GET'])
def get_status():
    status = crawler_status.copy()

    if status['start_time']:
        elapsed = (datetime.now() - status['start_time']).total_seconds()
        status['elapsed_time'] = elapsed

    return jsonify(status)


@app.route('/api/result', methods=['GET'])
def get_result():
    global crawler_result

    if not crawler_result:
        return jsonify({'success': False, 'message': '暂无结果'})

    df = crawler_result['dataframe']
    stats = crawler_result['statistics']

    houses = df.head(100).to_dict('records')

    return jsonify({
        'success': True,
        'total': len(df),
        'houses': houses,
        'statistics': stats,
        'files': crawler_result['files']
    })


@app.route('/api/export/<format>', methods=['POST'])
def export_data(format):
    global crawler_result

    if not crawler_result:
        return jsonify({'success': False, 'message': '暂无数据'})

    try:
        df = crawler_result['dataframe']
        stats = crawler_result['statistics']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'excel':
            filename = f"output/房源数据_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
        elif format == 'csv':
            filename = f"output/房源数据_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        elif format == 'json':
            filename = f"output/房源数据_{timestamp}.json"
            df.to_json(filename, orient='records', force_ascii=False, indent=2)
        else:
            return jsonify({'success': False, 'message': '不支持的格式'})

        return jsonify({'success': True, 'file': filename})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join('output', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'message': '文件不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/files', methods=['GET'])
def list_files():
    output_dir = 'output'
    if not os.path.exists(output_dir):
        return jsonify({'files': []})

    files = []
    for filename in os.listdir(output_dir):
        if filename.endswith(('.xlsx', '.csv', '.pdf', '.html', '.json', '.md')):
            filepath = os.path.join(output_dir, filename)
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath),
                'modified': datetime.fromtimestamp(
                    os.path.getmtime(filepath)
                ).strftime('%Y-%m-%d %H:%M:%S')
            })

    files.sort(key=lambda x: x['modified'], reverse=True)
    return jsonify({'files': files})


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    global crawler_result

    if not crawler_result:
        return jsonify({'success': False, 'message': '暂无数据'})

    df = crawler_result['dataframe']

    stats = {
        'total': len(df),
        'avg_price': df['总价(万)'].mean() if '总价(万)' in df.columns else 0,
        'median_price': df['总价(万)'].median() if '总价(万)' in df.columns else 0,
        'avg_area': df['面积'].mean() if '面积' in df.columns else 0,
        'district_distribution': df['区域'].value_counts().to_dict() if '区域' in df.columns else {},
        'source_distribution': df['来源'].value_counts().to_dict() if '来源' in df.columns else {},
        'price_distribution': df['总价(万)'].value_counts(bins=10).to_dict() if '总价(万)' in df.columns else {}
    }

    return jsonify({'success': True, 'statistics': stats})


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    print("\n" + "="*60)
    print("三亚房源爬取系统 - Web界面")
    print("="*60)
    print("\n访问地址: http://localhost:5000")
    print("API文档: http://localhost:5000/api/docs")
    print("\n按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
