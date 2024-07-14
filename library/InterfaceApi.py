import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

# api类中暴露给前端的函数名称，命名保持与前端一致（小驼峰），方便前后端对接

# 定义一个Api类，用于与前端交互 
class Api:
    def __init__(self):

        # cases属性是一个列表，用于存放案件对象
        self._cases = []
        # templateFiles属性是一个列表，用于存放模板文件对象
        self._templateFiles = []

    # ===== 下面是获取文件或文件夹路径的方法，方便后面的方法复用（该组方法不对接前端） =====
    def GetFilepath(self,title) -> str:
        # 下面是用tkinter的方法获取文件的绝对路径
        from tkinter import filedialog
        # #  获取文件路径
        SelectedFilePath = filedialog.askopenfilename(title=title,filetypes=[
            ("Text files", "*.txt"),
            ("Excel files", "*.xlsx"),
            ("Word files", "*.docx"),
            ("All files", "*.*")])
        return SelectedFilePath

        # 下面用webview的方法获取文件的绝对路径
        # import webview
        # FileTypes = [("Text files", "*.txt"),("Excel files", "*.xlsx")]
        # result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=FileTypes)
        # print(result)
        # return result

    def GetFolderpath(self,title) -> str:
        # 下面是用tkinter的方法获取文件夹的绝对路径
        from tkinter import filedialog
        # 获取文件夹路径
        SelectedFolderPath = filedialog.askdirectory(title=title)
        return SelectedFolderPath

        # 下面用webview的方法获取文件夹的绝对路径
        # import webview
        # result = window.create_file_dialog(webview.FOLDER_DIALOG)
        # print(result)
        # return result


    # ===== 下面是和 CaseInfoForm 组件交互的方法 =====

    # ==输入类==

    # 该方法用于根据前端输入的案件信息，生成一个新的案件
    def inputCaseFromFrontEndForm(self,CaseFormDict) -> str:
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
        # 将CaseFormDict中的数据，调用InputCaseInfoFromFrontEnd方法导入到当前case对象中
        case.InputCaseInfoFromFrontEnd(CaseFormDict)
        # 将案件对象添加到案件列表中
        self._cases.append(case)

        return "Success"
    
    # 该方法用于前端输入一个txt文件的路径，然后生成对应的新的案件
    def inputCaseFromTxt(self,TxtPath) -> str:

        # 判断输入的两个路径是否存在
        if not os.path.exists(TxtPath):
            print("Error: The path is not exist!")
            return "PathNotExist"
        
        # 判断输入的文件是否是txt文件
        if not TxtPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return "NotTxtFile"
        
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
        # 将CaseFormDict中的数据，调用InputCaseInfoFromTxt方法将txt导入到当前case对象中
        case.InputCaseInfoFromTxt(TxtPath)
        # 将案件对象添加到案件列表中
        self._cases.append(case)
        print("案件导入成功！")

        return "Success"
    
    # 该方法用于读入一个包含多个案件信息的txt文件，批量生成新的案件信息
    def inputAllCasesFromTxt(self) -> str:
        InputPath = self.GetFilepath(title="请选择案件信息输入文件")
        # 判断输入的路径是否存在
        if not os.path.exists(InputPath):
            print("Error: The path is not exist!")
            return "Fail"
        # 判断输入的文件是否是txt文件
        if not InputPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return "Fail"
        
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
                # 将案件内容调用case对象的InputCaseInfoFromStringList方法，将信息导入到当前case对象中
                case.InputCaseInfoFromStringList(CaseContent)
                # 如果该案件的案件Id与列表中的案件均不相同，则将案件对象添加到self._case中
                if case.GetCaseId() not in [case.GetCaseId() for case in self._cases]:
                    self._cases.append(case)
                else:
                    print(f"编号为{case.GetCaseId()}的案件已存在，无需重复导入！")

        print("全部案件导入成功！")
        return "Success"


    # ==输出类==

    # 该方法用于输出指定案件的信息到Excel，并保存到案件文件夹中
    def outputCaseInfoToExcel(self,caseId) -> str:
        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return "CaseListIsEmpty"
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToExcel()
                return "Success"

    # 该方法用于输出指定案件的信息到txt，并保存到案件文件夹中        
    def outputCaseInfoToTxt(self,caseId) -> str:
        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return "CaseListIsEmpty"
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                case.OutputCaseInfoToTxt()
                return "Success"

    # 该方法用于输出所有案件的信息到一个txt
    def outputAllCasesInfoToTxt(self) -> str:
        OutputFolderPath = self.GetFolderpath(title="请选择案件信息保存的文件夹")
        print(OutputFolderPath)
        # 判断OutputPath是否存在
        if not os.path.exists(OutputFolderPath):
            print("Error: The path is not exist!")
            return "PathNotExist"
        # 判断OutputPath是否是文件夹
        if not os.path.isdir(OutputFolderPath):
            print("Error: The path is not a directory!")
            return "NotDirectory"
        OutputFolderPath = OutputFolderPath + "\\"
        OutputName = "所有案件信息输出.txt"
        with open(OutputFolderPath+OutputName,"w",encoding='utf-8') as f:
            for case in self._cases:
                f.write("$CaseStart$\n")
                f.write(case.OutputCaseInfoToStr())
                f.write("$CaseEnd$\n\n")
            print("全部案件信息输出成功！")
            return "Success"

    # 该方法用于输出当前所有案件信息成一个列表并推送到前端
    def outputAllCaseInfoToFrontEnd(self) -> list:
        Result = []
        for case in self._cases:
            Result.append(case.OutputCaseInfoToFrontEnd())
        # 返回案件列表
        return Result
    
    # 该方法用于对接前端的文书生成按钮，用于生成案件文件夹及对应的文件模板
    def documentsGenerate(self,caseId,templateFilesIdList) -> str:
        # 先将对应caseId的案件对象找到，赋值给TargetCase
        for case in self._cases:
            if case.GetCaseId() == caseId:
                TargetCase = case
                break

        # 导入自写包FolderCreator
        from source.Generator import FolderCreator

        # 检查templateFiles是否为空
        if len(self._templateFiles) == 0:
            print("Error: The templateFiles is empty!")
            return "TemplateFilesIsEmpty"
        
        # 根据templateFilesIdList找到对应的模板文件对象，赋值给TargetTemplateFiles
        TargetTemplateFiles = []
        for templateFileId in templateFilesIdList:
            for templateFile in self._templateFiles:
                if templateFile.GetTemplateFileId() == templateFileId:
                    TargetTemplateFiles.append(templateFile)
                    break
        
        # 检验无误后，执行案件文件夹生成的操作
        Result = FolderCreator(case=TargetCase,              
                      OutputDir=TargetCase.GetCaseFolderPath(),   
                      TemplateListOrTemplateListDir=TargetTemplateFiles)
        
        # 检查FolderCreator是否执行成功
        if Result != "Success":
            print("Generator报错")
            return "GeneratorError"
        else:
            print("案件文件夹及对应的文件模板生成成功！")
            # 返回值为0代表生成成功
            return "Success"
    
    # ==删除类==
    # 该方法用于后端的数据中删除指定案件
    def backEndDeleteCase(self,CaseId) -> str:
        # 测试是否收到了前端传来的案件ID
        print(CaseId)
        # 在案件列表中删除指定案件
        for case in self._cases:
            # 判断案件ID是否相同,如果相同则在后端也删除对应id的案件并返回
            if case.GetCaseId() == CaseId:
                self._cases.remove(case)
                return "Success"
        else:
            # 如果遍历完，没有找到对应的案件，则返回Fail
            return "Fail"


    # ===== 下面是和CaseInfoEditForm组件交互的方法 =====

    # ==输入类==
    # 该方法用于从一个txt中读取当事人信息，然后生成对应的新的当事人
    def inputLitigantFromTxt(self,TxtPath,LitigantType) -> str|dict:
        # 判断输入的路径是否存在
        if not os.path.exists(TxtPath):
            print("Error: The path is not exist!")
            return "PathNotExist"
        # 判断输入的文件是否是txt文件
        if not TxtPath.endswith(".txt"):
            print("Error: The file is not a txt file!")
            return "NotTxtFile"
        
        # 导入案件类litigant
        from library.LitigantClass import Litigant

        # 实例化一个Litigant对象
        litigant = Litigant()

        # 调用InputLitigantInfoFromTxt方法将txt导入到当前litigant对象中
        litigant.InputLitigantInfoFromTxt(TxtPath,LitigantType)

        # 将当事人信息调用OutputLitigantInfoToFrontEnd方法输出到前端
        # 返回值原本为字典，会被自动pywebview自动转化为js对象
        return litigant.OutputLitigantInfoToFrontEnd()


    # =====  下面是与 TemplateFileForm组件交互的方法  =====
    
    def backEndAddTemplateFileData(self) -> str:

        # 调用GetFilepath方法获取文件路径
        TemplateFilePath = self.GetFilepath(title="请选择模板列表文件")
        # 导入模板文件类TemplateFile
        from source.Generator import ReadTemplateList

        if TemplateFilePath == "":
            return "Cancel"
        else:
            TemplateFileList = ReadTemplateList(TemplateFilePath)
        
        # 如果没有重复的模板文件，则将模板文件添加到self._templateFiles中

        # 遍历模板文件列表
        for templateFile in TemplateFileList:
            # 如果模板文件ID相同，则跳过
            if templateFile.GetTemplateFileId() in [File.GetTemplateFileId() for File in self._templateFiles]:
                continue
            # 如果模板文件名相同，则跳过
            if templateFile.GetTemplateFileName() in [File.GetTemplateFileName() for File in self._templateFiles]:
                continue

            # 如果文件ID相同，则将TemplateFile对象添加到self._templateFiles中
            self._templateFiles.append(templateFile)

        return "Success"

    def backEndPushTemplateFileDataToFrontEnd(self) -> list:
        # 如果self._templateFiles为空，则返回空列表给前端
        if len(self._templateFiles) == 0:
            return []

        # 如果self._templateFiles不为空，则将模板文件列表返回
        templateFiles = []
        for templateFile in self._templateFiles:
            templateFiles.append(templateFile.OutputTemplateFileToDict())

        return templateFiles

    def backEndUpdateTemplateFileData(self,TemplateFileId,data) -> str:
        # 遍历模板文件列表
        for templateFile in self._templateFiles:
            # 如果模板文件ID相同，则更新模板文件信息
            if templateFile.GetTemplateFileId() == TemplateFileId:
                # 如果赋值成功，则返回Success
                if templateFile.SetTemplateFileFromDict(data) == "Success":
                    return "Success"
        return "Fail"

    def backEndDeleteTemplateFileData(self,TemplateFileId) -> str:
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

    def backEndOutputTemplateFileData(self) -> str:
        import time
        # 调用GetFolderpath方法获取文件夹路径
        OutputFolderPath = self.GetFolderpath(title="请选择模板文件保存的文件夹")
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
        
    # =====  下面是和TemplateFileEditForm交互的方法  =====
    def backEndChooseTemplateFile(self) -> dict:
        result = {
            "res" : "",
            "templateFileDir" : "",
            "templateFileName" : "",
        }

        # 调用GetFilepath方法获取文件路径
        NewTemplateFileDir = self.GetFilepath(title="请选择新的模板文件")
        # 如果NewTemplateFile为空，则返回Cancel
        if NewTemplateFileDir == "":
            result["res"] = "Cancel"
            return result
        else:
            result["templateFileDir"] = NewTemplateFileDir
            # 将文件名从路径中提取出来
            FileName = os.path.basename(NewTemplateFileDir)
            # 去掉后缀名后，赋值给templateFileName
            result["templateFileName"] = FileName.split(".")[0]
            # 全部正常运行，返回Success
            result["res"] = "Success"
            return result


    # =====  下面是和其他未开发完成的组件交互的方法  =====

        # 该方法用于生成案件归档目录
    def generateArchiveDirectoryDocument(self,TemplateFilePath,SavedPath) -> str:
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
    
    #  =====  下面是测试输出方法  =====

    def testCasesOutput(self) -> None:
        # 输出案件信息
        for case in self._cases:
            print(case.OutputCaseInfoToStr())
        return 
    
    def testTemplateFilesOutput(self) -> None:
        # 输出templateFiles
        for templateFile in self._templateFiles:
            print(templateFile.OutputTemplateFileToDict()) 
        return 