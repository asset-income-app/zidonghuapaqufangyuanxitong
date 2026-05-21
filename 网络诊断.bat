@echo off
chcp 65001 >nul
echo ========================================
echo 三亚房源爬取系统 - 网络诊断
echo ========================================
echo.

echo [诊断] 正在检查网络连接...
echo.

echo [1] 测试DNS解析
echo ----------------------------------------
nslookup sanya.lianjia.com >nul 2>&1
if errorlevel 1 (
    echo [×] 链家网 DNS解析失败
) else (
    echo [√] 链家网 DNS解析成功
)

nslookup sanya.anjuke.com >nul 2>&1
if errorlevel 1 (
    echo [×] 安居客 DNS解析失败
) else (
    echo [√] 安居客 DNS解析成功
)

echo.
echo [2] 测试网络连接
echo ----------------------------------------
ping -n 1 sanya.lianjia.com >nul 2>&1
if errorlevel 1 (
    echo [×] 链家网 无法连接
) else (
    echo [√] 链家网 可以连接
)

ping -n 1 sanya.anjuke.com >nul 2>&1
if errorlevel 1 (
    echo [×] 安居客 无法连接
) else (
    echo [√] 安居客 可以连接
)

echo.
echo [3] 测试Python环境
echo ----------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [×] Python未安装
) else (
    echo [√] Python已安装
    python --version
)

echo.
echo ========================================
echo 诊断完成
echo ========================================
echo.
echo 如果DNS解析失败，请尝试：
echo   1. 更换DNS服务器（推荐：223.5.5.5）
echo   2. 刷新DNS缓存：ipconfig /flushdns
echo   3. 检查防火墙设置
echo   4. 使用VPN或代理
echo.
echo 详细说明请查看：docs\真实爬取问题说明.md
echo ========================================
pause
