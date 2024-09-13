# 导入自带库
import sys,os
from tkinter import filedialog

# 不要生成字节码
sys.dont_write_bytecode = True

# ===== 下面是获取文件或文件夹路径的方法，方便后面的方法复用（该组方法不对接前端） =====
def GetOpenFilepath(title,filetype="All") -> str:
    # 下面是用tkinter的方法获取文件的绝对路径
    # 根据读入的filetype参数，选择不同的文件类型
    filetypes = []

    # filetype用逗号进行分割，然后根据不同的文件类型添加到filetypes中,默认值为All
    filetypeList = filetype.split(",")
    for type in filetypeList:
        if type == "All":
            filetypes.append(("All files", "*.*"))
        elif type == "Text":
            filetypes.append(("Text files", "*.txt"))
        elif type == "Excel":
            filetypes.append(("Excel files", "*.xlsx"))
        elif type == "Word":
            filetypes.append(("Word files", "*.docx"))
        elif type == "Json":
            filetypes.append(("Json files", "*.json"))

    # #  获取文件路径
    SelectedFilePath = filedialog.askopenfilename(title=title,filetypes=filetypes)
    return SelectedFilePath


def GetFolderpath(title) -> str:
    # 下面是用tkinter的方法获取文件夹的绝对路径
    # 获取文件夹路径
    SelectedFolderPath = filedialog.askdirectory(title=title)
    return SelectedFolderPath


def GetSaveFilepath(title,filetype="All") -> str:
    # 根据读入的filetype参数，选择不同的文件类型
    filetypes = []

    # filetype用逗号进行分割，然后根据不同的文件类型添加到filetypes中,默认值为All
    filetypeList = filetype.split(",")
    for type in filetypeList:
        if type == "All":
            filetypes.append(("All files", "*.*"))
        elif type == "Text":
            filetypes.append(("Text files", "*.txt"))
            defaultextension = ".txt"
        elif type == "Excel":
            filetypes.append(("Excel files", "*.xlsx"))
            defaultextension = ".xlsx"
        elif type == "Word":
            filetypes.append(("Word files", "*.docx"))
            defaultextension = ".docx"
        elif type == "Json":
            filetypes.append(("Json files", "*.json"))
            defaultextension = ".json"

    #  获取文件路径
    SelectedFilePath = filedialog.asksaveasfilename(title=title,
                                                    filetypes=filetypes,
                                                    confirmoverwrite=True,
                                                    defaultextension=defaultextension)
    return SelectedFilePath
