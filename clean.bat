@echo off
chcp 65001 >nul
echo ====================================
echo    清理项目文件
echo ====================================
echo.

echo 正在删除数据库文件...
if exist user_system.db (
    del user_system.db
    echo [OK] 数据库文件已删除
) else (
    echo [INFO] 数据库文件不存在
)

echo.
echo 正在清理临时文件...
if exist __pycache__ (
    rd /s /q __pycache__
    echo [OK] __pycache__ 已清理
)

if exist api\__pycache__ (
    rd /s /q api\__pycache__
    echo [OK] api\__pycache__ 已清理
)

if exist models\__pycache__ (
    rd /s /q models\__pycache__
    echo [OK] models\__pycache__ 已清理
)

if exist schemas\__pycache__ (
    rd /s /q schemas\__pycache__
    echo [OK] schemas\__pycache__ 已清理
)

echo.
echo ====================================
echo    清理完成！
echo ====================================
echo.
pause