import os,sys

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 该类为模板文件类，每一个对象都对应一个模板文件
class TemplateFile():

    def __init__(self):
        self._TemplateFileName = ""
        self._TemplateFileDir = ""
        self._TemplateFileType = ""
        self._TemplateFileStage = ""

    # ======= Get方法 ======= #
    def GetTemplateFileName(self):
        return self._TemplateFileName

    def GetTemplateFileDir(self):
        return self._TemplateFileDir
    
    def GetTemplateFileType(self):
        return self._TemplateFileType
    
    def GetTemplateFileStage(self):
        return self._TemplateFileStage
    
    # ======= Set方法 ======= #
    def SetTemplateFileName(self,TemplateFileName,Debug=False) -> int:

        # 输入检查
        # 检查文件名是否为字符串
        if not isinstance(TemplateFileName,str):
            if Debug:
                print("TemplateFileName should be a string.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileName = TemplateFileName
        return 0
 
    
    def SetTemplateFileDir(self,TemplateFileDir,Debug=False) -> int:

        # 输入检查
        # 检查路径是否为字符串
        if not isinstance(TemplateFileDir,str):
            if Debug:
                print("TemplateFileDir should be a string.") 
            return -1
        # 检查路径是否存在
        if not os.path.exists(TemplateFileDir):
            if Debug:
                print("TemplateFileDir does not exist.")
            return -1
        # 检查路径是否为文件
        if not os.path.isfile(TemplateFileDir):
            if Debug:
                print("TemplateFileDir should be a file.")
            return -1
        # 检查文件是否为docx文件
        if TemplateFileDir.split(".")[-1] != "docx":
            if Debug:
                print("TemplateFileDir should be a docx file.")
            return -1

        # 经过检查后，赋值
        self._TemplateFileDir = TemplateFileDir
        return 0
    
    def SetTemplateFileType(self,TemplateFileType,Debug=False) -> int:

        # 输入检查
        # 检查文件类型是否为字符串
        if not isinstance(TemplateFileType,str):
            if Debug:
                print("TemplateFileType should be a string.")
            return -1
        
        # 检查文件类型是否为directCopy或docxtpl
        if TemplateFileType != "directCopy" and TemplateFileType != "docxtpl":
            if Debug:
                print("TemplateFileType should be 'directCopy' or 'docxtpl'.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileType = TemplateFileType

        return 0

    def SetTemplateFileStage(self,TemplateFileStage,Debug=False) -> int:

        # 输入检查
        # 检查阶段是否为字符串
        if not isinstance(TemplateFileStage,str):
            if Debug:
                print("TemplateFileStage should be a string.")
            return -1
        
        # 检查阶段是否为委托、立案、审理、执行、归档 这五个阶段之一
        if TemplateFileStage != "委托" and TemplateFileStage != "立案" and TemplateFileStage != "审理" and TemplateFileStage != "执行" and TemplateFileStage != "归档":
            if Debug:
                print("TemplateFileStage should be '委托' or '立案' or '审理' or '执行' or '归档'.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileStage = TemplateFileStage

        return 0 
            

    # ======= 更抽象一些的Set方法 ======= #

    # 下面是对于读入文件中的每一行进行处理
    def SetTemplateFileFromString(self,InputString,Debug=False) -> str:
        
        # 每一个合法的字符串格式应当为：TemplateFileStage|TemplateFileDir@TemplateFileType


        # 去除首尾空格
        InputString = InputString.strip()

        # 检查字符串是否符合规则
        if "|" not in InputString:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s缺少字符【|】，不符合规则" % InputString)
                return "Error"
        if "@" not in InputString:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s缺少字符【@】，不符合规则" % InputString)
                return "Error"
        
        # 将字符串按照|分割
        FileStage,FiledirAndFileType = InputString.split("|")
        # 将剩下的字符串按照@分割
        Filedir,FileType = FiledirAndFileType.split("@")
        # 调用Set方法分别赋值
        if self.SetTemplateFileStage(FileStage) == -1:
            return "Error"
        if self.SetTemplateFileDir(Filedir) == -1:
            return "Error"
        if self.SetTemplateFileType(FileType) == -1:
            return "Error"
        # 将文件名从路径中提取出来
        if self.SetTemplateFileName(Filedir.split("\\")[-1]) == -1: 
            return "Error"

        # 全部正常运行，返回Success
        return "Success"


    # ======= Output方法 ======= #

    # 输出为该模板文件的字符串，方便写入txt文件
    def OutputTemplateFileToString(self) -> str:
        return self.GetTemplateFileStage() + "|" + self.GetTemplateFileDir() + "@" + self.GetTemplateFileType()

    # 输出为字典，方便写入json文件或输出到前端
    def OutputTemplateFileToDict(self) -> dict:
        return {"templateFileName":self.GetTemplateFileName(),
                "templateFileDir":self.GetTemplateFileDir(),
                "templateFileType":self.GetTemplateFileType(),
                "templateFileStage":self.GetTemplateFileStage()
                }