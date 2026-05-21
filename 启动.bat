@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 一键启动
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)
echo [√] Python环境正常

echo.
echo [2/3] 检查依赖包...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
)
echo [√] 依赖包已就绪

echo.
echo [3/3] 启动爬虫系统...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo 任务执行完毕！
echo ========================================
echo.
echo 按任意键打开输出目录...
pause >nul
explorer output
