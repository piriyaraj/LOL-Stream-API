@echo off
IF EXIST "LOL-Stream" (
  cd LOL-Stream
  git restore .> log.txt 2>&1
  git pull > log.txt 2>&1
) ELSE (    
    echo "== Installing set up=="
  git clone https://github.com/piriyaraj/LOL-Stream.git > log.txt 2>&1
  cd LOL-Stream
)
if not exist venv (
    echo "    * Creating environment=="
    python -m venv venv
)
call venv\Scripts\activate
git restore .> log.txt 2>&1
git pull> log.txt 2>&1
@echo off
pip install -r requirements.txt > log.txt 2>&1

call python video_maker/main.py

pause
