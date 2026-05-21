@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 模拟数据模式
echo ========================================
echo.

echo [提示] 使用模拟数据测试系统功能
echo [提示] 如需真实爬取，请运行 启动.bat
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
echo [2/2] 运行模拟数据测试...
python main.py --mock

echo.
echo ========================================
echo 测试完成！
echo.
echo 您现在可以：
echo   1. 查看 output 目录中的文件
echo   2. 运行 启动Web界面.bat 查看数据
echo   3. 运行 启动.bat 进行真实爬取
echo ========================================
pause
