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
        self._MultiRenderOption = ""

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

    def GetMultiRenderOption(self) -> str:
        return self._MultiRenderOption
    
    # ======= Set方法 ======= #
    def SetId(self,Id,Debug=False) -> int:
            
        # 输入检查
        # 检查id是否为字符串
        if not isinstance(Id,str):
            if Debug:
                print("Id should be a string.")
            return -1
        
        # 如果id为空，则视为用户不输入id，生成一个id
        if Id == "":
            self.SetId(generate(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",size=6))
            return 0

        # 检查id是否为6位
        if len(Id) != 6:
            if Debug:
                print("Id should be 6 characters.")
            return -1
        
        # 检查id是否全部由大写字母构成
        if not Id.isupper():
            if Debug:
                print("Id should be all uppercase.")
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
        
        # 赋值
        self._FileName = FileName.strip()

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
            
    def SetMultiRenderOption(self,MultiRenderOption,Debug=False) -> int:
            
            # 输入检查
            # 检查是否为列表
            if not isinstance(MultiRenderOption,str):
                return -1
            
            if MultiRenderOption not in ["","Us","Opponents","Courts",
                            "CourtsAndUs","CourtsAndOpponents"]:
                if Debug:
                    print("Elements in MultiRenderOption should be 'Us' or 'Opponents' or 'Courts'.")
                return -1
            
            # 经过检查后，赋值
            self._MultiRenderOption = MultiRenderOption
    
            return 0

    # ======= Input 方法 ======= #

    # 下面对于读入字典进行处理
    def InputFromDict(self,InputDict,Debug=False) -> str|dict:

        # 检查是否为字典
        if not isinstance(InputDict,dict):
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入不是字典")
            return "Error"
        
        # 错误信息字典初始化
        ErrorResult = {
            "setIdError": False,
            "setFileNameError": False,
            "setDirError": False,
            "setRenderTypeError": False,
            "setRenderStageError": False,
            "setMultiRenderOptionError": False
        }

        # 检查是否有templateFileName键
        for key,value in InputDict.items():

            if key == "id":
                if self.SetId(value) == -1:
                    ErrorResult["setIdError"] = True

            elif key == "fileName":
                if self.SetFileName(value) == -1:
                    ErrorResult["setFileNameError"] = True

            elif key == "dir":
                if self.SetDir(value) == -1:
                    ErrorResult["setDirError"] = True

            elif key == "renderType":
                if self.SetRenderType(value) == -1:
                    ErrorResult["setRenderTypeError"] = True

            elif key == "renderStage":
                if self.SetRenderStage(value) == -1:
                    ErrorResult["setRenderStageError"] = True

            elif key == "multiRenderOption":
                if self.SetMultiRenderOption(value) == -1:
                    ErrorResult["setMultiRenderOptionError"] = True
        
        # 如果经过读取字典后，id为空，则生成一个id
        if self.GetId() == "":
            self.SetId(generate(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",size=6))

        # 如果经过读取字典后，文件名为空，且路径属性不为空，则从路径中提取文件名
        if self.GetFileName() == "" and hasattr(self,"_Dir") and self._Dir != "":
                self.SetFileName(os.path.basename(self._Dir).split(".")[0])

        # 如果有错误，返回错误信息
        if True in ErrorResult.values():
            return ErrorResult
        
        else:
            # 全部正常运行，返回Success
            return "Success"

    # ======= Output方法 ======= #

    # 输出为字典，输出到前端
    def OutputToDict(self) -> dict:

        ReturnDict = { 
            "id": self.GetId(),
            "fileName": self.GetFileName(),
            "dir": self.GetDir(),
            "renderType": self.GetRenderType(),
            "renderStage": self.GetRenderStage(),
            "multiRenderOption": self.GetMultiRenderOption()
        }

        # 对key进行排序
        ReturnDict = dict(sorted(ReturnDict.items(),key=lambda x:x[0]))

        # 返回
        return ReturnDict

