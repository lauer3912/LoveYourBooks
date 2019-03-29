echo ************************
REM 声明采用UTF-8编码
chcp 65001

@set PYTHONIOENCODING=utf-8
echo appimu
@python run.py --s http://127.0.0.1:4723/wd/hub --d 127.0.0.1:21523