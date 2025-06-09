@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo Running TTS bot...
python tts.py

pause
