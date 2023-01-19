import win32api

from httpSer import http
from mainWindow import mainWindow
import os
from log import Log
import setup
import threading
import subprocess

setup.run()

is_debug = True  # set to False when release
sec = 1000

Log.Set_Debug_Mod(is_debug)

save_root = "save"
if not os.path.exists(save_root):
    print("not found")
    os.mkdir("save")
else:
    print("found")

threading.Thread(target=http.web_start, args=()).start()
try:
    subprocess.Popen("MajdataEdit.exe")
except:
    win32api.MessageBox(0, "启动Majdata异常，请勿更改文件路径！", "mai_mp3", 0)
mainWindow.show_window()