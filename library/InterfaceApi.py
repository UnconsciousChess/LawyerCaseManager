import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

# 定义一个Api类，用于与前端交互 
class Api:
    def __init__(self):

        # case属性是一个列表，用于存放案件对象
        self._case = []

    # ===== 下面是获取文件或文件夹路径的方法 =====
    def GetFilepath(self) -> str:
        # 下面是用tkinter的方法获取文件的绝对路径
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
                if case.GetCaseId() not in [case.GetCaseId() for case in self._case]:
                    self._case.append(case)
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
        GetInputPath = self.GetFilepath()
        # 调用inputAllCaseFromTxt方法将txt导入
        self.inputAllCaseFromTxt(InputPath=GetInputPath)
        return 0


    # ===== 下面是output方法 =====
    def OutputCaseInfoToExcel(self,caseId):
        # 判断案件列表是否为空
        if len(self._case) == 0:
            return 1
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._case:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToExcel()
                return 0
            
    def OutputCaseInfoToTxt(self,caseId):
        # 判断案件列表是否为空
        if len(self._case) == 0:
            return 1
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._case:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToTxt()
                return 0

    def OutputAllCaseInfoToFrontEnd(self):

        # 如果案件列表为空，则生成案件对象，测试阶段使用
        # if len(self._case) == 0:
        #     # 生成测试案件对象
        #     self.test()
        Result = []
        for case in self._case:
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
            for case in self._case:
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
    




    # ===== 下面是删除方法 =====
    def BackEndDeleteCase(self,CaseId):
        # 测试是否收到了前端传来的案件ID
        print(CaseId)
        # 在案件列表中删除指定案件
        for case in self._case:
            # 判断案件ID是否相同,如果相同则在后端也删除并返回
            if case.GetCaseId() == CaseId:
                self._case.remove(case)
                return 
    
    # ===== 下面是测试方法 =====
    def test(self):
        # 直接先调用input方法，生成案件对象
        self.inputCaseFromTxt(r"test\TestData\测试案件信息输入.txt")
        self.inputCaseFromTxt(r"test\TestData\测试案件信息输入2.txt")
