@echo off
chcp 65001 >nul 2>&1
setlocal

cd /d "%~dp0"

echo ============================================================
echo   Evidence Records Prompt Generator
echo ============================================================
echo.

set /p COUNT=请输入要生成的提示词数量: 

if "%COUNT%"=="" (
    echo.
    echo [ERROR] 数量不能为空。
    pause
    exit /b 1
)

echo.
set /p OUTPUT=请输入输出文件名（例如 prompts_100.txt）:
    
if "%OUTPUT%"=="" (
    set OUTPUT=prompts_%COUNT%.txt
)

echo.
set /p SLEEP=请输入每次 API 调用间隔秒数（直接回车默认为 0）:

if "%SLEEP%"=="" (
    set SLEEP=0
)

echo.
echo ============================================================
echo   即将开始生成
echo ============================================================
echo.
echo 数量: %COUNT%
echo 输出文件: outputs\%OUTPUT%
echo API 间隔: %SLEEP% 秒
echo.
echo ============================================================
echo.

python generate_prompts.py batch --count %COUNT% --output "%OUTPUT%" --sleep %SLEEP%

echo.
echo ============================================================
echo   任务结束
echo ============================================================
echo.

pause