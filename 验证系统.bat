@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 快速验证
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境
    pause
    exit /b 1
)
echo [√] Python环境正常

echo.
echo [2/3] 运行系统测试...
python tests\comprehensive_test.py
if errorlevel 1 (
    echo.
    echo [错误] 系统测试失败
    pause
    exit /b 1
)

echo.
echo [3/3] 验证完成！
echo ========================================
echo.
echo 系统已准备就绪，您可以：
echo   1. 双击 "启动Web界面.bat" 启动Web界面
echo   2. 双击 "启动.bat" 启动命令行版本
echo   3. 运行 "python tools/advanced_tools.py" 使用高级功能
echo.
echo ========================================
pause
