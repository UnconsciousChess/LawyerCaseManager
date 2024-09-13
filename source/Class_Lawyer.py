
import os,sys

# 导入nanoid库，用于生成唯一id
from nanoid import generate

# 导入第三方库，用于验证身份证号码的合法性
from id_validator import validator

# 不要生成字节码
sys.dont_write_bytecode = True

# 设定律师类
class Lawyer():
    def __init__(self):
        # 1.姓名
        self._Name = ""
        # 2.身份证号码
        self._IdCode = ""
        # 3.联系地址
        self._Address = ""
        # 4.联系方式
        self._ContactNumber = ""
        # 5.律师执业证号
        self._LawyerLicense = ""
        # 6.律师证上传路径数组
        self._DeligationFiles = []
        # 7.是否为实习律师
        self._InternLawyer = False

    # ========== 下面是Get方法 ==========
    # 定义外部获取律师姓名的方法
    def GetName(self):
        return self._Name
    
    # 定义外部获取律师身份证号的方法
    def GetIdCode(self):
        return self._IdCode
    
    # 定义外部获取律师地址的方法
    def GetAddress(self):
        return self._Address
    
    # 定义外部获取律师联系方式的方法
    def GetContactNumber(self):
        return self._ContactNumber

    # 定义外部获取律师执业证号的方法
    def GetLawyerLicense(self):
        return self._LawyerLicense
    
    # 定义外部获取委托代理材料路径数组的方法
    def GetDeligationFiles(self):
        return self._DeligationFiles
    
    # 定义外部获取是否为实习律师的方法
    def IsInternLawyer(self):
        return self._InternLawyer


    # ========== 下面是Set方法 ==========
    # 定义外部设置律师姓名的方法
    def SetName(self,Name):
        if isinstance(Name,str):
            self._Name = Name
            return
    
    # 定义外部设置律师身份证号的方法
    def SetIdCode (self,IdCode):
        if isinstance(IdCode,str):
            # 调用validator库，判断身份证号码是否合法
            if validator.is_valid(IdCode):
                self._IdCode = IdCode
                return

    # 定义外部设置律师地址的方法
    def SetAddress(self,Address):
        if isinstance(Address,str):
            self._Address = Address
            return
    
    # 定义外部设置律师联系方式的方法
    def SetContactNumber(self,ContactNumber):
        if isinstance(ContactNumber,str):
            # 判断是否全部为数字
            if ContactNumber.isdigit():
                self._ContactNumber = ContactNumber
                return
    
    # 定义外部设置律师执业证号的方法
    def SetLawyerLicense(self,LawyerLicense):
        if isinstance(LawyerLicense,str):
            # 判断是否全部为数字
            if LawyerLicense.isdigit():
                self._LawyerLicense = LawyerLicense
                return
    
    # 定义外部设置委托代理材料路径数组的方法
    def SetDeligationFiles(self,DeligationFiles):
        if isinstance(DeligationFiles,list):
            self._DeligationFiles = DeligationFiles
            return

    # 定义外部设置是否为实习律师的方法
    def SetInternLawyer(self,TrueOrFalse):
        if isinstance(TrueOrFalse,bool):
            self._InternLawyer = TrueOrFalse
            return

    # ========== 下面是Input方法 ==========
    # 从txt读入的函数
    def InputLawyerInfoFromTxt(self,InfoFile) -> str:
        # 先对传入的路径进行判断
        if not os.path.exists(InfoFile):
            return "PathNotExists"
        if not os.path.isfile(InfoFile):
            return "NotFile"
        if InfoFile.endswith(".txt") == False:
            return "NotTxtFile"
        
        # 读取文件到LitigantInfoFromTxt列表中
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            LitigantInfoFromTxt = f.readlines()

        # 去除换行符
        LitigantInfoFromTxtList = LitigantInfoFromTxt.split("\n")

        # 遍历每一行信息
        for information in LitigantInfoFromTxtList:
            if "Name" in information:
                self._Name = information.split("=")[-1]
            if "IdCode" in information:
                self._IdCode = information.split("=")[-1]
            if "Address" in information:
                self._Address = information.split("=")[-1]
            if "ContactNumber" in information:
                self._ContactNumber = information.split("=")[-1]
            if "DocumentsPath" in information:
                self._DocumentsPath = information.split("=")[-1]
            if "LawyerLicense" in information:
                self._LawyerLicense = information.split("=")[-1]
            if "InternLawyer" in information:
                if information.split("=")[-1] == "True":
                    self._InternLawyer = True
                elif information.split("=")[-1] == "False":
                    self._InternLawyer = False
                    
        return "Success"

    # ========== 下面是Output方法 ==========
    # 输出律师信息到屏幕
    def OutputLawyerInfoToScreen(self)  -> None:
        print(self._Name+"律师的执业证号="+self._LawyerLicense)
        print(self._Name+"律师的身份证号="+self._IdCode)
        print(self._Name+"律师的联系方式="+self._ContactNumber)
        print(self._Name+"律师的收件地址="+self._Address)
        print(self._Name+"律师的律师证上传路径="+self._DocumentsPath)
        if self._InternLawyer:
            print(self._Name+"律师是实习律师")
        else:
            print(self._Name+"律师不是实习律师")
        return 

    # 输出律师信息成字典格式
    def OutputLawyerInfoToDict(self) -> dict:
        LawyerInfoDict = {}
        LawyerInfoDict["lawyerName"] = self.GetName()
        LawyerInfoDict["lawyerIdCode"] = self.GetIdCode()
        LawyerInfoDict["lawyerAddress"] = self.GetAddress()
        LawyerInfoDict["lawyerPhoneNumber"] = self.GetContactNumber()
        LawyerInfoDict["lawyerLicense"] = self.GetLawyerLicense()
        LawyerInfoDict["isInternLawyer"] = self.IsInternLawyer()

        # 排序
        LawyerInfoDict = dict(sorted(LawyerInfoDict.items(),key=lambda x:x[0]))
        
        return LawyerInfoDict


