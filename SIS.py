import os
import tkinter as tk
from tkinter import filedialog, simpledialog

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="请选择下载并解压后的sis文件夹")
    if not directory:  # 检查用户是否点击了取消
        return None
    return directory

def process_ics_file(file_path, compositeICS, is_header=False):
    with open(file_path, "r", encoding="utf-8") as ics_file:
        flag = False
        for line in ics_file:
            line = line.strip()
            if is_header:
                if line == "X-MS-OLK-FORCEINSPECTOROPEN:TRUE":
                    compositeICS.write("X-MS-OLK-FORCEINSPECTOROPEN:FALSE" + "\n")
                else:
                    compositeICS.write(line + "\n")
                if line == "END:VEVENT":
                    break
            else:
                if line == "BEGIN:VEVENT":
                    flag = True
                if flag:
                    compositeICS.write(line + "\n")
                if line == "END:VEVENT":
                    flag = False

def select_output_filename():
    root = tk.Tk()
    root.withdraw()
    filename = simpledialog.askstring("输入自定义的ICS文件名", "请给 ICS 文件命个名吧 QWQ （不包含扩展名哦）：")
    if filename is None:  # 检查用户是否点击了取消
        return None
    return filename + ".ICS"

def merge_ics_files():
    while True:
        try:
            targetDir = select_directory()
            if targetDir is None:
                print("操作已取消，程序退出。")
                return

            if not os.path.isdir(targetDir):
                print("选择的路径不存在，请重新选择。")
                continue

            icsFiles = [name for name in os.listdir(targetDir) if name.upper().endswith(".ICS")]

            if not icsFiles:
                print("抹茶并没有在文件夹内找到任何 ICS 文件 QAQ。")
                continue

            output_filename = select_output_filename()
            if output_filename is None:
                print("操作已取消，程序退出。")
                return

            desktop_path = os.path.expanduser("~/Desktop")
            composite_path = os.path.join(desktop_path, output_filename)
            
            if os.path.exists(composite_path):
                print("桌面存在同名文件了哦，请删除后再运行")
                continue

            with open(composite_path, "w", encoding="utf-8") as compositeICS:
                head_file = icsFiles[0]
                process_ics_file(os.path.join(targetDir, head_file), compositeICS, is_header=True)

                for name in icsFiles[1:]:
                    process_ics_file(os.path.join(targetDir, name), compositeICS)

                compositeICS.write("END:VCALENDAR")
            
            print("ICS 文件合并成功！")
            break  # 如果成功，就退出循环
        
        except Exception as e:
            print(f"发生错误: {e}。请重新尝试。")

if __name__ == "__main__":
    merge_ics_files()
