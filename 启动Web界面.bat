@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - Web界面启动
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
pip show flask >nul 2>&1
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
echo [3/3] 启动Web服务器...
echo ========================================
echo.
echo 🌐 Web界面地址: http://localhost:5000
echo 📖 API文档: http://localhost:5000/api/docs
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

cd web
python app.py

pause
