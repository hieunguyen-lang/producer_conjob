@echo off
REM Chuyển đến thư mục dự án
cd C:/Users/hieunk/Documents/hieunk-project/AI_spam_models/

REM Kích hoạt môi trường ảo .venv
call .venv/Scripts/activate.bat

REM Chạy file Python
python modelfaster.py

REM Deactivate môi trường ảo khi kết thúc
deactivate
