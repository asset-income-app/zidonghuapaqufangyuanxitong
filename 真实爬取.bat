@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 真实爬取模式
echo ========================================
echo.

echo [提示] 开始爬取真实房源数据
echo [提示] 这可能需要几分钟时间，请耐心等待...
echo.

echo [1/2] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境
    pause
    exit /b 1
)
echo [√] Python环境正常

echo.
echo [2/2] 开始爬取真实数据...
echo ========================================
python main.py

echo.
echo ========================================
echo 爬取完成！
echo.
echo 您现在可以：
echo   1. 查看 output 目录中的文件
echo   2. 运行 启动Web界面.bat 查看数据
echo ========================================
pause
