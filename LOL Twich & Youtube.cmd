@echo off
IF EXIST "LOL-Stream-API" (
  cd LOL-Stream-API
  git restore .> log.txt 2>&1
  git pull > log.txt 2>&1
) ELSE (    
    echo "== Installing set up=="
  git clone https://github.com/piriyaraj/LOL-Stream-API.git > log.txt 2>&1
  cd LOL-Stream-API
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

call python main.py --yt True

pause
