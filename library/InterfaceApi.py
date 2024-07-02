import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True


# 定义一个Api类，用于与前端交互 
class Api:
    def __init__(self):

        # cases属性是一个列表，用于存放案件对象
        self._cases = []
        # templateFiles属性是一个列表，用于存放模板文件对象
        self._templateFiles = []

    # ===== 下面是获取文件或文件夹路径的方法 =====
    def GetFilepath(self,title) -> str:
        # 下面是用tkinter的方法获取文件的绝对路径
        from tkinter import filedialog
        # #  获取文件路径
        SelectedFilePath = filedialog.askopenfilename(title=title,filetypes=[("Text files", "*.txt"),("Excel files", "*.xlsx")])
        return SelectedFilePath

        # 下面用webview的方法获取文件的绝对路径
        # import webview
        # FileTypes = [("Text files", "*.txt"),("Excel files", "*.xlsx")]
        # result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=FileTypes)
        # print(result)
        # return result

    def GetFolderpath(self) -> str:
        # 下面是用tkinter的方法获取文件夹的绝对路径
        from tkinter import filedialog
        # 获取文件夹路径
        SelectedFolderPath = filedialog.askdirectory()
        return SelectedFolderPath

        # 下面用webview的方法获取文件夹的绝对路径
        # import webview
        # result = window.create_file_dialog(webview.FOLDER_DIALOG)
        # print(result)
        # return result


    # ===== 下面是input方法 =====
    # 该方法用于生成案件文件夹及依据模板生成对应的文件
    def inputCaseFromFrontEndForm(self,CaseFormDict):
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
        # 将CaseFormDict中的数据，调用InputCaseInfoFromFrontEnd方法导入到当前case对象中
        case.InputCaseInfoFromFrontEnd(CaseFormDict)
        # 将案件对象添加到案件列表中
        self._cases.append(case)

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
        self._cases.append(case)
        print("案件导入成功！")

        return 0
    
    def inputAllCaseFromTxt(self,InputPath):
        # 判断输入的路径是否存在
        if not os.path.exists(InputPath):
            print("Error: The path is not exist!")
            return 1
        # 判断输入的文件是否是txt文件
        if not InputPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return 2
        
        # 导入案件类Case
        from library.CaseClass import Case

        # 打开文件
        with open(InputPath,"r",encoding='utf-8') as f:
            CaseContentList = []
            CurrentCaseContent = []
            # 读取文件内容
            Content = f.readlines()
            # 将文件内容分成不同的CaseContent，并放入CaseContentList中
            for line in Content:
                # 如果读取到案件开始符，则跳过
                if "$CaseStart$" in line:
                    continue
                # 如果当前行以#开头，则跳过
                elif line.startswith("#"):
                    continue
                # 如果当前行为空行，则跳过
                elif line == "\n":
                    continue
                # 如果读取到案件结束符，则将当前案件内容添加到CaseContentList中，同时清空当前案件内容
                elif "$CaseEnd$" in line:
                    CaseContentList.append(CurrentCaseContent)
                    CurrentCaseContent = []
                    continue
                # 如果当前行不为空，则将当前行添加到当前案件内容中
                else:
                    # 去掉当前行的换行符
                    line = line.strip("\n")
                    CurrentCaseContent.append(line)

            # 循环读取每个案件的CaseContent，注意CaseContent也是一个列表
            for CaseContent in CaseContentList:
                # 如果案件内容为空，则跳过
                if CaseContent == "": 
                    continue
                # 实例化一个Case对象
                case = Case()
                # 将案件内容调用InputCaseInfoFromTxt方法导入到当前case对象中
                case.InputCaseInfoFromStringList(CaseContent)
                # 如果该案件的案件Id与列表中的案件均不相同，则将案件对象添加到self._case中
                if case.GetCaseId() not in [case.GetCaseId() for case in self._cases]:
                    self._cases.append(case)
                else:
                    print(f"编号为{case.GetCaseId()}的案件已存在，无需重复导入！")

        print("全部案件导入成功！")
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
        return litigant.OutputLitigantInfoToFrontEnd()
        
    def bulkInputCaseFromTxt(self):
        GetInputPath = self.GetFilepath(title="请选择案件信息输入文件")
        # 调用inputAllCaseFromTxt方法将txt导入
        self.inputAllCaseFromTxt(InputPath=GetInputPath)
        return 0


    # ===== 下面是output方法 =====
    def OutputCaseInfoToExcel(self,caseId):
        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return 1
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToExcel()
                return 0
            
    def OutputCaseInfoToTxt(self,caseId):
        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return 1
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToTxt()
                return 0

    def OutputAllCaseInfoToFrontEnd(self):

        # 如果案件列表为空，则生成案件对象，测试阶段使用
        # if len(self._cases) == 0:
        #     # 生成测试案件对象
        #     self.test()
        Result = []
        for case in self._cases:
            Result.append(case.OutputCaseInfoToFrontEnd())
        # 返回案件列表
        return Result
    
    def OutputAllCaseInfoToTxt(self,OutputFolderPath):
        print(OutputFolderPath)
        # 判断OutputPath是否存在
        if not os.path.exists(OutputFolderPath):
            print("Error: The path is not exist!")
            return 1
        # 判断OutputPath是否是文件夹
        if not os.path.isdir(OutputFolderPath):
            print("Error: The path is not a directory!")
            return 2
        OutputFolderPath = OutputFolderPath + "\\"
        OutputName = "所有案件信息输出.txt"
        with open(OutputFolderPath+OutputName,"w",encoding='utf-8') as f:
            for case in self._cases:
                f.write("$CaseStart$\n")
                f.write(case.OutputCaseInfoToStr())
                f.write("$CaseEnd$\n\n")
            print("全部案件信息输出成功！")
            return 0

    def bulkOutputCaseInfoToTxt(self):
        GetOutputFolderPath = self.GetFolderpath()
        # 调用OutputAllCaseInfoToTxt方法输出
        self.OutputAllCaseInfoToTxt(OutputFolderPath=GetOutputFolderPath)
    

    # ===== 下面是其他方法 =====
    # 该方法未完善
    def DocumentsGenerate(self,caseId):
        # 先将对应caseId的案件对象找到，赋值给TargetCase
        for case in self._cases:
            if case.GetCaseId() == caseId:
                TargetCase = case
                break

        # 导入自写包FolderCreator
        from source.Generator import FolderCreator
        # 读取模板列表文件
        TemplateListDir = self.GetFilepath(title="请选择模板列表文件")
        # 检验无误后，执行案件文件夹生成的操作
        Result = FolderCreator(case=TargetCase,              
                      OutputDir=TargetCase.GetCaseFolderPath(),   
                      TemplateListDir=TemplateListDir)
        if Result == -1:
            print("Generator报错")
            return -1
        
        print("案件文件夹及对应的文件模板生成成功！")
        # 返回值为0代表生成成功
        return 0
        



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
    

    # ===== 下面是删除方法 =====
    def BackEndDeleteCase(self,CaseId):
        # 测试是否收到了前端传来的案件ID
        print(CaseId)
        # 在案件列表中删除指定案件
        for case in self._cases:
            # 判断案件ID是否相同,如果相同则在后端也删除对应id的案件并返回
            if case.GetCaseId() == CaseId:
                self._cases.remove(case)
                return 
    


    # =====  下面是与 TemplateFileForm组件交互的方法  =====
    def BackEndAddTemplateFileData(self) -> str:

        # 调用GetFilepath方法获取文件路径
        TemplateFilePath = self.GetFilepath(title="请选择模板列表文件")
        # 导入模板文件类TemplateFile
        from source.Generator import ReadTemplateList

        if TemplateFilePath == "":
            return "Cancel"
        else:
            TemplateFileList = ReadTemplateList(TemplateFilePath)

        # 如果没有重复的模板文件，则将模板文件添加到self._templateFiles中
        for templateFile in TemplateFileList:
            if templateFile.GetTemplateFileId() not in [File.GetTemplateFileId() for File in self._templateFiles]:
                # 将TemplateFile对象添加到self._templateFiles中
                self._templateFiles.append(templateFile)

        return "Success"


    def BackEndGetTemplateFileData(self) -> list:
        # 如果self._templateFiles为空，则返回空
        if len(self._templateFiles) == 0:
            return []

        # 如果self._templateFiles不为空，则将模板文件列表返回
        templateFiles = []
        for templateFile in self._templateFiles:
            templateFiles.append(templateFile.OutputTemplateFileToDict())

        return templateFiles

    def BackEndDeleteTemplateFileData(self,TemplateFileId) -> str:
        # 测试是否收到了前端传来的案件ID
        print(TemplateFileId)
        # 在案件列表中删除指定模板文件
        for templateFile in self._templateFiles:
            # 判断模板文件ID是否相同,如果相同则在后端也删除对应id的模板文件并返回
            if templateFile.GetTemplateFileId() == TemplateFileId:
                self._templateFiles.remove(templateFile)
                return "Success"
            
        # 如果遍历完，没有找到对应的模板文件，则返回Fail
        return "Fail"

    def BackEndOutputTemplateFileData(self) -> str:
        import time
        # 调用GetFolderpath方法获取文件夹路径
        OutputFolderPath = self.GetFolderpath()
        # 判断OutputPath是否存在,如果不存在则返回错误
        if OutputFolderPath == "":
            return "Cancel"
        # 写入模板列表文件，名字为“模板列表+当前时间.txt”
        FileName = "模板列表"+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+".txt"  
        with open(OutputFolderPath + "\\" + FileName, "w" , encoding='utf-8') as f:
            for templateFile in self._templateFiles:
                f.write(templateFile.OutputTemplateFileToString())
                f.write("\n")
            return "Success"