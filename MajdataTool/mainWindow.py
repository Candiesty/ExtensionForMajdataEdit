import tkinter
import tkinter.filedialog
from pydub import AudioSegment
import os
from log import Log
import tkinter as tk
import threading
import re
import win32api, win32con
import time


class mainWindow:
    # base window head
    is_debug = True  # set to False when release
    sec = 1000
    Log.Set_Debug_Mod(is_debug)
    save_root = "save"
    if not os.path.exists(save_root):
        print("not found")
        os.mkdir("save")
    else:
        print("found")

    # window response
    @classmethod
    def read_file(cls):
        cls.select_path.set(tkinter.filedialog.askopenfilename(title="请选择乐曲文件"))
        if os.path.exists(cls.select_path.get()):
            try:
                song = AudioSegment.from_mp3(cls.select_path.get())
                cls.max_end_time.set(len(song) / 1000)
            except:
                win32api.MessageBox(0, "导入歌曲出错！", "mai_mp3", win32con.MB_OK)
                cls.select_path.set("")
                cls.max_end_time.set(0)

    @classmethod
    def select_file(cls, fileroot):
        cls.select_path.set(fileroot)
        if os.path.exists(cls.select_path.get()):
            try:
                song = AudioSegment.from_mp3(cls.select_path.get())
                cls.max_end_time.set(len(song) / 1000)
            except:
                win32api.MessageBox(0, "导入歌曲出错！", "mai_mp3", win32con.MB_OK)
                cls.select_path.set("")
                cls.max_end_time.set(0)

    @classmethod
    def create_song(cls):
        song = AudioSegment.from_mp3(cls.select_path.get())
        print(song)
        print(cls.start_time.get() * cls.sec)
        print(cls.end_time.get() * cls.sec)
        pre_time = int(60.0 / float(cls.start_bpm) * cls.pre_beat.get() * 1000)
        print(pre_time)
        song_split = AudioSegment.silent(duration=pre_time)
        song = song[int(cls.start_time.get() * cls.sec): int(cls.end_time.get() * cls.sec)]
        song = song_split + song
        song.frame_rate = song.frame_rate * cls.play_speed.get() / 100
        song = song*cls.play_times.get()
        file_name = cls.output_name.get()
        cls.listb.insert(tk.END, file_name)
        file_name = cls.save_root + "/" + file_name
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        song.export(file_name + "/track.mp3")
        mainWindow.save_score(file_name)
        while True:
            time.sleep(1)
            if os.path.exists(file_name + "/track.mp3"):
                num = 0
                for each in cls.listb.get(0, tk.END):
                    print(each)
                    if each == file_name:
                        break
                    num = num + 1
                cls.listb.delete(num)
                win32api.MessageBox(0, "导出成功！", "mai_mp3", win32con.MB_OK)
                return

    @classmethod
    def create_song_thread(cls):
        for each in cls.listb.get(0, tk.END):
            if each == cls.output_name.get():
                win32api.MessageBox(0, "项目正在生成中请勿重复操作！", "mai_mp3", 0)
                return
        if cls.start_time.get() == cls.end_time.get() or cls.end_time.get() > cls.max_end_time.get() or cls.start_time.get() > cls.end_time.get():
            win32api.MessageBox(0, "歌曲时长存在问题！", "mai_mp3", 0)
            return
        if os.path.exists("save/" + cls.output_name.get()):
            res = win32api.MessageBox(0, "已经存在对应项目，要进行覆盖吗?", "mai_mp3", 4)
            if res == 7:
                return
        if cls.play_times.get() < 0 or cls.play_times.get() >= 39:
            win32api.MessageBox(0, "播放次数异常，最多支持39次重播！", "mai_mp3", 0)
            return
        if cls.play_speed.get() < 0:
            win32api.MessageBox(0, "播放速度异常！", "mai_mp3", 0)
            return

        thread = threading.Thread(target=cls.create_song)
        thread.start()

    @classmethod
    def show_window(cls):
        cls.root.config(menu=cls.menu_bar)
        cls.root.mainloop()
        return

    @classmethod
    def get_data_from_edit(cls, start, end,startsig,startbpm,head,note,):
        cls.start_time.set(start)
        cls.end_time.set(end)
        cls.note.delete('1.0',tk.END)
        cls.score_head = head
        cls.score_note = note
        cls.note.insert('end',note)
        cls.start_bpm = startbpm
        cls.start_signature = startsig

    @classmethod
    def save_score(cls,filename):
        result = cls.score_head
        bpm = cls.start_bpm
        result += "\r\n"+"&lv_1=15"
        result += "\r\n"+"&inote_1="
        for i in range(0,cls.play_times.get()):
            result += "(" + bpm + ")"
            result += "{4}" + ","*cls.pre_beat.get() + "\r\n"
            result += "{" + cls.start_signature + "}"
            result += cls.score_note
            result += "\r\n"
        score_root = filename + "/maidata.txt"
        with open(score_root ,'w') as file:
            file.write(result)
        return



    # main_ui
    # base attr
    root = tk.Tk()
    root.title = "mai_mp3"
    select_path = tk.StringVar()
    start_time = tk.DoubleVar()
    end_time = tk.DoubleVar()
    max_end_time = tk.IntVar()
    play_speed = tk.IntVar()
    play_speed.set(100)
    play_times = tk.IntVar()
    play_times.set(5)
    output_name = tk.StringVar()
    output_name.set("default")
    score_note = ""
    score_head = ""
    start_bpm = ""
    start_signature = ""
    pre_beat = tk.IntVar()
    pre_beat.set(4)

    # menu ui
    menu_bar = tk.Menu(root)
    filemenu = tk.Menu(menu_bar, tearoff=False)
    filemenu.add_command(label="打开")
    filemenu.add_command(label="保存")
    menu_bar.add_cascade(label="文件", menu=filemenu)

    # base ui

    listb = tk.Listbox(root, height=4, width=28)
    note = tk.Text(root, height=8, width=40,font="size:10")
    scroll = tk.Scrollbar(root,width=16)
    scroll.config(command=note.yview)
    note.config(yscrollcommand=scroll.set)

    root.geometry('660x320')
    line = 0
    tk.Label(root, text="文件路径：").grid(column=0, row=line)
    tk.Entry(root, textvariable=select_path).grid(column=1, row=line)
    tk.Button(root, text="选择单个文件", command=lambda: mainWindow.read_file()).grid(row=line, column=2)
    line = line + 1
    tk.Label(root, text="输出项目文件名称：").grid(column=0, row=line)
    tk.Entry(root, textvariable=output_name).grid(row=line, column=1)
    tk.Label(root, text="铺面预览：").grid(column=2, row=line)
    line = line + 1
    tk.Label(root, text="开始时间(s)：").grid(column=0, row=line)
    tk.Entry(root, textvariable=start_time, width=8).grid(row=line, column=1, stick="w")
    note.grid(rowspan=5, row=line, column=2, columnspan=4)
    scroll.grid(rowspan=5,row=line,column=6,sticky="ns")
    line = line + 1
    tk.Label(root, text="结束时间(s)：").grid(column=0, row=line)
    tk.Entry(root, textvariable=end_time, width=8).grid(column=1, row=line, stick="w")
    line = line + 1
    tk.Label(root, text="歌曲时长(s)：").grid(column=0, row=line)
    tk.Label(root, textvariable=max_end_time, width=8, anchor="w").grid(column=1, row=line, stick="w")
    line = line + 1
    tk.Label(root, text="播放速度(百分比)：").grid(column=0, row=line)
    tk.Label(root, textvariable=play_speed, width=8, anchor="w").grid(column=1, row=line, stick="w")
    line = line + 1
    tk.Label(root, text="重复次数：").grid(column=0, row=line)
    tk.Entry(root, textvariable=play_times, width=8).grid(column=1, row=line, stick="w")
    line = line + 1
    tk.Label(root, text="谱间预留拍数：").grid(column=0, row=line)
    tk.Entry(root, textvariable=pre_beat, width=8).grid(column=1, row=line, stick="w")
    line = line + 1
    tk.Button(root, text="创建", command=lambda: mainWindow.create_song_thread(), width=6).grid(row=line, column=0)
    listb.grid(row=line, column=1,rowspan=2,columnspan=2)
    line = line + 1


