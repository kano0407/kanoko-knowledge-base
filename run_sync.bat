@echo off
REM Obsidian 自動同期スクリプト起動

cd /d "%~dp0"
py -3.12 scripts\sync_monitor.py
pause
