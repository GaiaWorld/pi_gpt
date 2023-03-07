@echo off

if not exist config\config.json (
    copy config\config_default.json config\config.json
)

python ./src/bot.py

pause