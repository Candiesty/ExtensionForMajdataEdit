import os
import win32api,win32con

def get_windows_user_path() -> str:
    t = os.popen("reg query \"HKEY_CURRENT_USER\\Environment\" -v path")
    t = t.read()
    t = t.split()  # 以不可见字符为分隔符拆分字符串
    t = t[3:]  # 前3个元素不要
    t = " ".join(t)  # 如果path中有空格的话会被split掉，所有需要用join合并回来。以空格连接各个部分。
    return t


def add_windows_user_path(path_handle: str,path_need_add: str):
    org = get_windows_user_path()
    org_list = org.split(";")
    print(org_list)
    for aorg in org_list:
        if path_handle == aorg:
            re = os.system("ffmpeg -version")
            print(re)
            if re == 1:
                os.popen("setx ffm \"{}\"".format(path_need_add))
                win32api.MessageBox(0,"配置环境变量，请重新启动软件！","mai_mp3",0)
                exit(0)
            return

    if org[-1:] == ";":  # 判断原来的path末尾是否有,如果没有则需要加上;再拼接待加的path
        org += path_handle
    else:
        org += ";" + path_handle
    print(org)
    print(path_need_add)
    print("请稍后，正在配置系统环境变量...")
    os.popen("setx Path \"{}\"".format(org))
    os.popen("setx ffm \"{}\"".format(path_need_add))
    win32api.MessageBox(0, "安装ffmpeg目录成功!请重新启动程序", "mai_mp3", win32con.MB_OK)
    exit()
    return


def set_windows_user_env(key: str, value: str) -> int:
    return os.system("setx \"{}\" \"{}\"".format(key, value))


def run():
    print("test env")
    now_path = os.popen("echo %cd%").read()
    now_path = now_path[:-1]
    print(now_path)
    now_path += r"\ffmpeg-master-latest-win64-gpl\bin"
    add_windows_user_path(r"%ffm%", now_path)
    return now_path
