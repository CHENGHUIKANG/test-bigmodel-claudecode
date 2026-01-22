@echo off
chcp 65001 >nul
echo ====================================
echo    用户管理系统 - 快速启动
echo ====================================
echo.
echo 正在启动API服务...
echo.
echo 服务地址: http://localhost:8000
echo 按 Ctrl+C 停止服务
echo.
echo ====================================
echo.

python mini_api.py

pause