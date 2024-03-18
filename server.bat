@echo off
chcp 65001

cd C:\Users\%username%\Desktop\Work\Other\socket_pattern
start cmd /k python server.py
echo Server has started.

if "%1" == "" (
    echo empty parameter.
) else (
    call .\client.bat %1
)