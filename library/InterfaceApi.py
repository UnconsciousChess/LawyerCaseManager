import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

# 定义一个Api类，用于与前端交互 
class Api:
    def __init__(self):

        # case属性是一个列表，用于存放案件对象
        self._case = []
  
    # ===== 下面是input方法 =====
    # 该方法用于生成案件文件夹及依据模板生成对应的文件
    def inputCaseFromFrontEndForm(self,CaseFormDict):
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
        # 将CaseFormDict中的数据，调用InputCaseInfoFromFrontEnd方法导入到当前case对象中
        case.InputCaseInfoFromFrontEnd(CaseFormDict)
        # 将案件对象添加到案件列表中
        self._case.append(case)

        return 0
    
    # 该方法用于前端输入一个txt文件的路径，然后生成案件文件夹及依据模板生成对应的文件
    def inputCaseFromTxt(self,TxtPath):
        # 判断输入的两个路径是否存在
        if not os.path.exists(TxtPath):
            print("Error: The path is not exist!")
            return 1
        # 判断输入的文件是否是txt文件
        if not TxtPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return 2
        
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
        # 将CaseFormDict中的数据，调用InputCaseInfoFromTxt方法将txt导入到当前case对象中
        case.InputCaseInfoFromTxt(TxtPath)
        # 将案件对象添加到案件列表中
        self._case.append(case)
        print("案件导入成功！")

        return 0
    


    def inputLitigantFromTxt(self,TxtPath,LitigantType):
        # 判断输入的路径是否存在
        if not os.path.exists(TxtPath):
            print("Error: The path is not exist!")
            return 1
        # 判断输入的文件是否是txt文件
        if not TxtPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return 2
        
        # 导入案件类litigant
        from library.LitigantClass import Litigant

        # 实例化一个Litigant对象
        litigant = Litigant()

        # 调用InputLitigantInfoFromTxt方法将txt导入到当前litigant对象中
        litigant.InputLitigantInfoFromTxt(TxtPath,LitigantType)

        # 将当事人信息调用OutputLitigantInfoToFrontEnd方法输出到前端
        # 返回值原本为字典，会被自动pywebview自动转化为js对象
        print(litigant.OutputLitigantInfoToFrontEnd())
        return litigant.OutputLitigantInfoToFrontEnd()
        


        return 0
    # ===== 下面是output方法 =====
    def OutputCaseInfoToExcel(self,OutputFilePath):
        # 判断案件列表是否为空
        if len(self._case) == 0:
            # print("Error: The case is empty!")
            return 1
        # 判断输出路径是否存在
        if not os.path.exists(OutputFilePath):
            # print("Error: The path is not exist!")
            return 2
        # 判断输出路径是否是文件
        if os.path.isfile(OutputFilePath):
            return 3
        # 判断该路径是否以'/'结尾，如果不是则加上
        if not OutputFilePath.endswith("\\"):
            OutputFilePath += "\\"        

        self._case[0].OutputCaseInfoToExcel(OutputFilePath=OutputFilePath)
  
    def OutputCaseInfoToTxt(self,OutputFilePath):

        # 判断案件列表是否为空
        if len(self._case) == 0:
            # print("Error: The case is empty!")
            return 1
        # 判断输出路径是否存在
        if not os.path.exists(OutputFilePath):
            # print("Error: The path is not exist!")
            return 2
        # 判断输出路径是否是文件
        if os.path.isfile(OutputFilePath):
            # print("Error: The path is a file!")
            return 3
        
        # 判断该路径是否以'/'结尾，如果不是则加上
        if not OutputFilePath.endswith("\\"):
            OutputFilePath += "\\"        
        
        self._case[0].OutputCaseInfoToTxt(OutputFilePath=OutputFilePath)


    # ===== 下面是其他方法 =====
    # 该方法未完善
    def FolderCreator(self):
        # 导入自写包FolderCreator
        from source.Generator import FolderCreator

        # 进行检验后面再写

        # 检验无误后，执行案件文件夹生成的操作
        FolderCreator(case=self._case[0],              
                      OutputDir=self._case[0].GetCaseFolderPath(),   
                      TemplateListDir=r"test\TestData\TemplateFilesList.txt")
        

    # 该方法用于生成案件归档目录
    def generateArchiveDirectoryDocument(self,TemplateFilePath,SavedPath):
        # 导入自写包RenderFile中的RenderArchiveDirectory函数（生成归档目录）
        from source.RenderFile import RenderArchiveDirectory
        # 判断输入的路径是否存在
        if not os.path.exists(SavedPath):
            return "Error: The path is not exist!"
        else:
            # 执行归档目录生成
            RenderDict = {}      # 用于渲染的字典,格式为{key:(True/False,str)  
            RenderArchiveDirectory(TemplateFilePath,RenderDict,SavedPath)

        return f"归档目录生成成功,保存路径为{SavedPath}"
    


    def GetFilepath(self) -> str:

        # 下面是用tkinter的方法获取文件的绝对路径
        # 导入tkinter包
        from tkinter import filedialog
        # #  获取文件路径
        SelectedFilePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),("Excel files", "*.xlsx")])
        return SelectedFilePath

        # 下面用webview的方法获取文件的绝对路径
        # import webview
        # FileTypes = [("Text files", "*.txt"),("Excel files", "*.xlsx")]
        # result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=FileTypes)
        # print(result)
        # return result