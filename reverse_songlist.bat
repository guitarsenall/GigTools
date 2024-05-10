ECHO OFF
REM ECHO file received:
REM ECHO %1
ECHO calling python312 reverse_songlist.py on %1

REM @START C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe "%1"
C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe reverse_songlist.py %1
pause
