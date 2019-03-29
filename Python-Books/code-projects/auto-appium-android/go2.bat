echo ************************
REM 声明采用UTF-8编码
chcp 65001

@set PYTHONIOENCODING=utf-8
echo appium -p 4725
@python run.py --s http://127.0.0.1:4725/wd/hub --d 127.0.0.1:21533