@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 完整启动指南
echo ========================================
echo.

echo 请选择启动模式：
echo.
echo   1. 使用模拟数据测试（推荐新手）
echo   2. 启动Web界面
echo   3. 真实爬取（需要网络）
echo   4. 系统验证
echo   5. 退出
echo.

set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" goto mock
if "%choice%"=="2" goto web
if "%choice%"=="3" goto real
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto end

echo.
echo [错误] 无效选项
pause
exit /b 1

:mock
echo.
echo ========================================
echo 模拟数据测试模式
echo ========================================
echo.
python main.py --mock
pause
exit /b 0

:web
echo.
echo ========================================
echo 启动Web界面
echo ========================================
echo.
echo 访问地址: http://localhost:5000
echo.
cd web
python app.py
pause
exit /b 0

:real
echo.
echo ========================================
echo 真实爬取模式
echo ========================================
echo.
echo [提示] 需要网络连接
echo [提示] 如遇网络问题，请查看 docs/网络问题解决方案.md
echo.
pause
python main.py
pause
exit /b 0

:verify
echo.
echo ========================================
echo 系统验证
echo ========================================
echo.
python tests\comprehensive_test.py
pause
exit /b 0

:end
echo.
echo 再见！
exit /b 0
