import os,sys

# 导入nanoid模块
from nanoid import generate

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 该类为模板文件类，每一个对象都对应一个模板文件
class TemplateFile():

    def __init__(self):
        # 模板文件的id
        self._Id = ""
        # 模板文件的名称
        self._FileName = ""
        # 模板文件的路径
        self._Dir = ""
        # 模板文件的类型（直接复制或者docxtpl）
        self._RenderType = ""
        # 模板文件的阶段（委托、立案、审理、执行、归档）
        self._RenderStage = ""
        # 需要根据某个选项进行多次渲染的属性
        self._MultiRenderList = []

    # ======= Get方法 ======= #
    def GetId(self) -> str:
        return self._Id
    
    def GetFileName(self) -> str:
        return self._FileName

    def GetDir(self) -> str:
        return self._Dir
    
    def GetRenderType(self) -> str:
        return self._RenderType
    
    def GetRenderStage(self)  -> str:
        return self._RenderStage

    def GetMultiRenderList(self) -> list:
        return self._MultiRenderList
    
    # ======= Set方法 ======= #
    def SetId(self,Id,Debug=False) -> int:
            
        # 输入检查
        # 检查id是否为字符串
        if not isinstance(Id,str):
            if Debug:
                print("Id should be a string.")
            return -1
        
        # 经过检查后，赋值
        self._Id = Id
        return 0
    
    def SetFileName(self,FileName,Debug=False) -> int:

        # 输入检查
        # 检查文件名是否为字符串
        if not isinstance(FileName,str):
            if Debug:
                print("FileName should be a string.")
            return -1
        
        # 经过检查后，赋值
        self._FileName = FileName
        return 0
    
    def SetDir(self,Dir,Debug=False) -> int:

        # 输入检查
        # 检查路径是否为字符串
        if not isinstance(Dir,str):
            if Debug:
                print("Dir should be a string.") 
            return -1
        # 检查路径是否存在
        if not os.path.exists(Dir):
            if Debug:
                print("Dir does not exist.")
            return -1
        # 检查路径是否为文件
        if not os.path.isfile(Dir):
            if Debug:
                print("Dir should be a file.")
            return -1
        # 检查文件是否为docx文件
        if Dir.split(".")[-1] != "docx":
            if Debug:
                print("Dir should be a docx file.")
            return -1

        # 经过检查后，赋值
        self._Dir = Dir
        return 0
    
    def SetRenderType(self,RenderType,Debug=False) -> int:

        # 输入检查
        # 检查文件类型是否为字符串
        if not isinstance(RenderType,str):
            if Debug:
                print("RenderType should be a string.")
            return -1
        
        # 检查文件类型是否为directCopy或docxtpl
        if RenderType != "directCopy" and RenderType != "docxtpl":
            if Debug:
                print("RenderType should be 'directCopy' or 'docxtpl'.")
            return -1
        
        # 经过检查后，赋值
        self._RenderType = RenderType

        return 0

    def SetRenderStage(self,RenderStage,Debug=False) -> int:

        # 输入检查
        # 检查阶段是否为字符串
        if not isinstance(RenderStage,str):
            if Debug:
                print("RenderStage should be a string.")
            return -1
        
        # 检查阶段是否为委托、立案、审理、执行、归档 这五个阶段之一
        if RenderStage != "委托" and RenderStage != "立案" and RenderStage != "审理" and RenderStage != "执行" and RenderStage != "归档":
            if Debug:
                print("RenderStage should be '委托' or '立案' or '审理' or '执行' or '归档'.")
            return -1
        
        # 经过检查后，赋值
        self._RenderStage = RenderStage

        return 0 
            
    def SetMultiRenderList(self,MultiRenderList,Debug=False) -> int:
        pass

    # ======= 更抽象一些的Set方法 ======= #

    # 下面是对于读入文件中的每一行进行处理
    def SetTemplateFileFromJsonDict(self,InputDict,Debug=False) -> str:
        
        # 检查是否为字典
        if not isinstance(InputDict,dict):
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入不是字典")
            return "Error"
        
        # 检查是否有stage键
        if "stage" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【stage】")
            return "Error"
        # 检查是否有path键
        if "dir" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【path】")
            return "Error"
        # 检查是否有type键
        if "type" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【type】")
            return "Error"
        

        # 从字典中提取出stage、path、type
        FileStage = InputDict["stage"]
        Filedir = InputDict["dir"]
        FileType = InputDict["type"]

        # 调用Set方法分别赋值
        if self.SetRenderStage(FileStage) == -1:
            return "Error"
        if self.SetDir(Filedir) == -1:
            return "Error"
        if self.SetRenderType(FileType) == -1:
            return "Error"
        # 将文件名从路径中提取出来
        FileName = Filedir.split("\\")[-1]
        # 去掉后缀名
        FileName = FileName.split(".")[0]
        if self.SetFileName(FileName) == -1:     
            return "Error"
        # 生成id
        if self.SetId(generate(alphabet='ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnpqrstuvwxyz', size=8)) == -1:
            return "Error"

        # 全部正常运行，返回Success
        return "Success"

    # 下面对于读入字典进行处理
    def SetTemplateFileFromDict(self,InputDict,Debug=False) -> str:
        # 检查是否为字典
        if not isinstance(InputDict,dict):
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入不是字典")
            return "Error"
        
        # 检查是否有templateFileName键
        if "templateFileName" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileName】")
            return "Error"
        # 检查是否有templateFileDir键
        if "templateFileDir" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileDir】")
            return "Error"
        # 检查是否有templateFileType键
        if "templateFileType" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileType】")
            return "Error"
        # 检查是否有templateFileStage键
        if "templateFileStage" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileStage】")
            return "Error"
        # 检查是否有templateFileId键
        if "templateFileId" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileId】")
            return "Error"
        
        # 调用Set方法分别赋值
        if self.SetFileName(InputDict["templateFileName"]) == -1:
            return "Error"
        if self.SetDir(InputDict["templateFileDir"]) == -1:
            return "Error"
        if self.SetRenderType(InputDict["templateFileType"]) == -1:
            return "Error"
        if self.SetRenderStage(InputDict["templateFileStage"]) == -1:
            return "Error"
        if self.SetId(InputDict["templateFileId"]) == -1:
            return "Error"
        
        # 全部正常运行，返回Success
        return "Success"

    # ======= Output方法 ======= #

    # 输出为字典，输出到前端
    def OutputTemplateFileToDict(self) -> dict:
        return {"templateFileName":self.GetFileName(),
                "templateFileDir":self.GetDir(),
                "templateFileType":self.GetRenderType(),
                "templateFileStage":self.GetRenderStage(),
                "templateFileId":self.GetId()
                }

    # 输出为字典，输出到json文件
    def OutputTemplateFileToJsonDict(self) -> dict:
        return { 
                "stage":self.GetRenderStage(),
                "dir":self.GetDir(),
                "type":self.GetRenderType()
                }