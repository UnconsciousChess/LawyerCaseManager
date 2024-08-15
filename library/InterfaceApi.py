import os,sys
import json


# 不要生成字节码
sys.dont_write_bytecode = True

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# api类中暴露给前端的函数名称，命名保持与前端一致（小驼峰），方便前后端对接
class Api:
    def __init__(self):

        # cases属性是一个列表，用于存放案件对象
        self._cases = []
        # templateFiles属性是一个列表，用于存放模板文件对象
        self._templateFiles = []
        # 
        self._isInitial = False

    # ===== 下面是初始化函数 =====

    def appStartInit(self) -> dict|str:
        # 判断是否已经初始化
        if self._isInitial:
            return "AlreadyInitial"
        
        # 如果没有初始化才进行下面的步骤

        # 导入json模块
        import json
        # 读取配置文件
        with open(r"test\TestData\config.json","r",encoding="utf-8") as f:
            Config = json.load(f)
        # 读取案件信息路径
        CasesInputPath = Config["path"]["casesPath"]
        TemplateFilesPath = Config["path"]["templateFilesPath"]

        # 初始化本函数的变量

        Result = {
            "caseResult" : "",
            "templateFileResult" : "",
        }
        StartCaseInput = True
        StartTemplateFileInput = True

        # 判断输入的案件信息路径是否存在
        if not os.path.exists(CasesInputPath):
            print("Error: The path is not exist!")
            Result["caseResult"] = "PathNotExist"
            StartCaseInput = False

        
        # 开始预读取案件信息
        if StartCaseInput:
            # 导入案件类Case
            from library.CaseClass import Case
            
            # 打开文件
            with open(CasesInputPath,"r",encoding='utf-8') as f:
                cases = json.load(f)
                for case in cases:
                    # 实例化一个Case对象
                    caseObj = Case()
                    # 将案件信息调用case对象的InputFromDict方法，将信息导入到当前case对象中
                    caseObj.InputFromDict(case)
                    
                    self._cases.append(caseObj)
                
                Result["caseResult"] = "Success"

        # 判断输入的路径是否存在
        if not os.path.exists(TemplateFilesPath):
            print("Error: The path is not exist!")
            Result["templateFileResult"] = "PathNotExist"
            StartTemplateFileInput = False
        # 判断输入的文件是否是txt文件
        if not TemplateFilesPath.endswith(".json"):
            print("Error: The file is not a json file!")
            Result["templateFileResult"] = "NotJson"
            StartTemplateFileInput = False

        # 开始预读取模板文件信息
        if StartTemplateFileInput:
            from source.Generator import ReadTemplateList

            TemplateFileList = ReadTemplateList(TemplateFilesPath)
            self._templateFiles = TemplateFileList
            Result["templateFileResult"] = "Success"

        # 如果案件信息和模板文件信息都导入成功，则视为初始化成功
        if Result["caseResult"] == "Success" and Result["templateFileResult"] == "Success":
            self._isInitial = True
        # 返回结果
        return Result
        

    # ===== 下面是获取文件或文件夹路径的方法，方便后面的方法复用（该组方法不对接前端） =====
    def GetOpenFilepath(self,title,filetype="All") -> str:
        # 下面是用tkinter的方法获取文件的绝对路径
        from tkinter import filedialog
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

    def GetFolderpath(self,title) -> str:
        # 下面是用tkinter的方法获取文件夹的绝对路径
        from tkinter import filedialog
        # 获取文件夹路径
        SelectedFolderPath = filedialog.askdirectory(title=title)
        return SelectedFolderPath
    
    def GetSaveFilepath(self,title,filetype="All") -> str:
        # 下面是用tkinter的方法获取文件的绝对路径
        from tkinter import filedialog
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



    # ===== 下面是和 CaseInfoShowTable 组件交互的方法 =====

    # ==输入类==

    # 该方法用于根据前端输入的案件信息，生成一个新的案件
    def inputSingleCaseFromFrontEndForm(self,CaseFormDict) -> str:
        # 导入案件类Case
        from library.CaseClass import Case
        # 实例化一个Case对象
        case = Case()
        # 将CaseFormDict中的数据，调用相应方法去生成当前case对象
        case.InputFromDict(CaseFormDict)
        # 将案件对象添加到self._case中
        self._cases.append(case)

        return "Success"
    
    # 该方法用于根据前端输入的案件信息，更新一个已有的案件
    def updateSingleCaseFromFrontEndForm(self,CaseFormDict) -> str:
        # 导入案件类Case
        from library.CaseClass import Case

        # 遍历案件列表
        for case in self._cases:
            # 如果案件ID相同，则更新案件信息
            if case.GetCaseId() == CaseFormDict["caseId"]:
                # 调用Case对象的UpdateCaseInfoFromDict方法，更新案件信息
                case.InputFromDict(CaseFormDict)
                return "Success"
        # 如果遍历完，都没有找到对应的案件，则返回Fail
        return "Fail"

    def inputSingleCaseFromJson(self,JsonPath) -> str:

        # 判断输入的路径是否存在
        if not os.path.exists(JsonPath):
            print("Error: The path is not exist!")
            return "PathNotExist"
        
        # 导入案件类Case
        from library.CaseClass import Case
        import json

        # 打开文件
        with open(JsonPath,"r",encoding='utf-8') as f:
            CaseDict = json.load(f)
            # 实例化一个Case对象
            case = Case()
            # 将案件内容调用case对象的InputFromDict方法，将信息导入到当前case对象中
            case.InputFromDict(CaseDict)
            # 如果该案件的案件Id与列表中的案件均不相同，则将案件对象添加到self._case中
            if case.GetCaseId() not in [case.GetCaseId() for case in self._cases]:
                self._cases.append(case)
            else:
                print(f"编号为{case.GetCaseId()}的案件已存在，无需重复导入！")


    # 该方法用于前端输入一个json文件的路径，然后生成对应的新的案件    
    def inputAllCasesFromJson(self) -> str:
        InputPath = self.GetOpenFilepath(title="请选择案件信息输入文件",filetype="Json")
        # 判断输入的路径是否存在
        if not os.path.exists(InputPath):
            print("Error: The path is not exist!")
            return "Fail"
        # 判断输入的文件是否是json文件
        if not InputPath.endswith(".json"):
            print("Error: The file is not a json file!")
            return "Fail"
        
        # 导入案件类Case
        from library.CaseClass import Case
        import json

        # 打开文件
        with open(InputPath,"r",encoding='utf-8') as f:
            CaseList = json.load(f)
            for CaseDict in CaseList:
                # 实例化一个Case对象
                case = Case()
                # 将案件内容调用case对象的InputFromDict方法，将信息导入到当前case对象中
                case.InputFromDict(CaseDict)
                # 如果该案件的案件Id与列表中的案件均不相同，则将案件对象添加到self._case中
                if case.GetCaseId() not in [case.GetCaseId() for case in self._cases]:
                    self._cases.append(case)
                else:
                    print(f"编号为{case.GetCaseId()}的案件已存在，无需重复导入！")

        print("全部案件导入成功！")
        return "Success"


    # ==输出类==


    # 该方法用于输出指定案件的信息到txt，并保存到案件文件夹中        
    def outputSingleCaseToTxt(self,caseId) -> str:

        OutputFileName = "案件信息output.txt"

        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return "CaseListIsEmpty"
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                # 写入文件
                with open(file=os.path.join(case.GetCaseFolderPath(),OutputFileName),
                          mode="w",encoding="utf-8") as f:
                    f.write(case.OutputToStr())
                    return "Success"
        # 如果遍历完，都没有找到对应的案件，则返回Fail
        return "Fail"

    # 该方法用于输出单一案件的信息到json，并保存到案件文件夹中
    def outputSingleCaseToJson(self,caseId) -> str:

        OutputFileName = f"{caseId}案件信息.json"

        # 判断案件列表是否为空
        if len(self._cases) == 0:
            return "CaseListIsEmpty"
        # 如果案件列表不为空，则根据caseId找到对应案件
        for case in self._cases:
            if case.GetCaseId() == caseId:
                # 写入文件
                with open(file=os.path.join(case.GetCaseFolderPath(),OutputFileName),
                          mode="w",encoding='utf-8') as f:
                    json.dump(case.OutputToDict(),
                              f, 
                              ensure_ascii=False,
                              indent=4)
                    return "Success"
        # 如果遍历完，都没有找到对应的案件，则返回Fail
        return "Fail"
    
    # 该方法用于输出所有案件的信息到json，并保存到案件文件夹中
    def outputAllCasesToJson(self) -> str:
        OutputFileName = self.GetSaveFilepath(title="导出案件信息",filetype="Json")


        # 判断OutputFileName是否为空，如果空就视为取消
        if OutputFileName == "":
            return "Cancel"
        

        with open(OutputFileName,"w",encoding='utf-8') as f:
            if len(self._cases) == 0:
                return "Fail"
            else:
                CaseList = []
                for case in self._cases:
                    CaseList.append(case.OutputToDict())
                json.dump(CaseList,
                          f, 
                          ensure_ascii=False,
                          indent=4)
                print("全部案件信息输出成功！")
            return "Success"

    # 该方法用于输出当前所有案件信息成一个列表并推到前端
    def pushAllCasesToList(self) -> list:
        CaseList = []
        for case in self._cases:
            CaseList.append(case.OutputToDict())
        # 返回案件列表
        return CaseList
    

    # 该方法用于对接前端的文书生成按钮，用于生成案件文件夹及对应的文件模板
    def documentsGenerate(self,caseId,templateFilesIdList) -> str:

        # 导入自写包FolderCreator
        from source.Generator import FolderCreator,FilesGenerator

        # 先将对应caseId的案件对象对应的index找到，赋值给TargetCaseIndex
        for index,case in enumerate(self._cases):
            if case.GetCaseId() == caseId:
                TargetCaseIndex = index
                break

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

        # 如果当前案件文件夹路径为空，则获取一个文件夹路径并生成对应的文件夹信息
        if self._cases[TargetCaseIndex].GetCaseFolderPath() == "":
            OutputDir=self.GetFolderpath(title="请选择案件文件夹保存的文件夹")
            # 其中项目文件夹名称由案件的原告、被告和案由组成
            FolderName = self._cases[TargetCaseIndex].GetAllPlaintiffNames() + "诉" + self._cases[TargetCaseIndex].GetAllDefendantNames() + "-" + self._cases[TargetCaseIndex].GetCauseOfAction() + "一案"
            OutputDir = os.path.join(OutputDir,FolderName)
            # 创建案件项目文件夹
            os.makedirs(OutputDir)
            self._cases[TargetCaseIndex].SetCaseFolderPath(OutputDir)
            
        # 调用FolderCreator生成案件文件夹
        Result = FolderCreator(
                        case=self._cases[TargetCaseIndex],              
                        OutputDir= self._cases[TargetCaseIndex].GetCaseFolderPath(),   
                        )
        
        # 检查FolderCreator是否执行成功
        if Result != "Success":
            print("FolderCreator报错")
            return Result
        
        # 调用FilesGenerator生成文件
        Result = FilesGenerator(
                        case=self._cases[TargetCaseIndex],              
                        OutputDir= self._cases[TargetCaseIndex].GetCaseFolderPath(),   
                        RenderTemplatesList=TargetTemplateFiles
                        )
        
        # 检查FilesGenerator是否执行成功
        if Result != "Success":
            print("FilesGenerator报错")
            return Result      

        # 如果FolderCreator和FilesGenerator都执行成功，则返回Success
        print("案件文件夹及对应的文件模板生成成功！")
        return "Success"

    # 该方法用于打开案件的文件夹
    def openCaseFolder(self,CaseId) -> str:
        # 遍历案件列表
        for case in self._cases:
            # 如果案件ID相同，则打开案件文件夹
            if case.GetCaseId() == CaseId:
                # 判断案件文件夹的路径是否存在
                if os.path.exists(case.GetCaseFolderPath()):
                    # 调用系统的startfile方法打开文件夹
                    os.startfile(case.GetCaseFolderPath())
                    return "Success"
                else:
                    return "CaseFolderNotExist"
        # 如果遍历完，都没有找到对应的案件，则返回CaseIdNotExist
        return "CaseIdNotExist"
    
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


    # ===== 下面是和CaseInfoForm组件交互的方法 =====

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

        # 调用GetOpenFilepath方法获取txt文件路径
        TemplateFilePath = self.GetOpenFilepath(title="请选择模板列表文件",filetype="Json")
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

            # 将TemplateFile对象添加到self._templateFiles中
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
        import json
        # 调出文本框来输入文件名
        OutputPath = self.GetSaveFilepath(title="选择模板列表保存路径",filetype="Json")
        # 判断OutputPath是否存在,如果不存在则返回错误
        if OutputPath == "":
            return "Cancel" 
        templateFiles = []

        with open(OutputPath, "w" , encoding='utf-8') as f:
            for templateFile in self._templateFiles:
                templateFiles.append(templateFile.OutputTemplateFileToJsonDict())
            # 将templateFiles写入到文件中
            json.dump(templateFiles,
                      f, 
                      ensure_ascii=False,
                      indent=4)

        return "Success"
        
    # =====  下面是和TemplateFileEditForm交互的方法  =====
    def backEndChooseTemplateFile(self) -> dict:
        result = {
            "res" : "",
            "templateFileDir" : "",
            "templateFileName" : "",
        }

        # 调用GetOpenFilepath方法获取文件路径
        NewTemplateFileDir = self.GetOpenFilepath(title="请选择模板文件",filetype="Word")
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


    # ===== 下面是和 MergeFilesTable组件 交互的方法 =====
    def backEndGetCaseFolderFiles(self,CaseId) -> list|str:
        # 遍历案件列表
        for case in self._cases:
            # 如果案件ID相同，则返回案件文件夹中的文件列表
            if case.GetCaseId() == CaseId:
               
                if os.path.exists(case.GetCaseFolderPath()):
                    print(case.GetCaseFolderPath())
                    FolderFileDirs = case.GetCaseFolderFiles(CurrentPath=case.GetCaseFolderPath())
                    ResultArray = []
                    # 对文件列表进行处理，并放入ResultArray中
                    for FileDir in FolderFileDirs:
                        ResultArray.append({"name":FileDir.split("\\")[-1],"path":FileDir})
                    # 对文件列表进行处理
                    return ResultArray
                else:
                    return "CaseFolderNotExist"
        # 如果遍历完，都没有找到对应的案件，则返回CaseIdNotExist
        return "CaseIdNotExist"


    def backEndMergeFiles(self,CaseId,SelectedFiles) -> str:
        from source.MergeFiles import MergeFiles
        # 遍历案件列表
        for case in self._cases:
            # 如果案件ID相同，则调用Mergefiles执行合并文件操作
            if case.GetCaseId() == CaseId:
                # print(SelectedFiles)
                MergeFiles(MergeList=SelectedFiles, 
                           MergeOutputName=case.GetCaseId() + "合并文件" ,
                           FolderPath=case.GetCaseFolderPath())
                print("合并文件成功！")
                return "Success"
        # 如果遍历完，没有找到对应的案件，则返回CaseIdNotExist
        print("CaseIdNotExist")
        return "CaseIdNotExist"


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
            print(case.OutputToStr())
        return 
    
    def testTemplateFilesOutput(self) -> None:
        # 输出templateFiles
        for templateFile in self._templateFiles:
            print(templateFile.OutputTemplateFileToDict()) 
        return 