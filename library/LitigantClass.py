import os,sys

# 导入第三方库，用于验证身份证号码的合法性
from id_validator import validator

# 导入nanoid库，用于生成唯一id
from nanoid import generate

# 导入银行账户类
from .Property import BankAccount

# 不要生成字节码
sys.dont_write_bytecode = True


# 设定诉讼参与人类
class Litigant():
    # 构造函数，在构造函数里面，先初始化各类属性
    def __init__(self):
        # 1.姓名
        self._Name = ""
        # 2.身份证/统一社会信用代码
        self._IdCode = ""
        # 3.联系地址
        self._Location = ""
        # 4.联系方式
        self._ContactNumber = ""
        # 5.身份证照片/营业执照上传路径
        self._DocumentsPath = ""
        # 6.诉讼地位（原告、被告、第三人）
        self._LitigantPosition = -1
        # 7.是否为我方当事人，默认为否
        self._OurClient = False
        # 8.性别，默认为-1，即无性别，当litigant为自然人时， 1 = 男性 0 = 女性
        self._Sex = -1
        # 9.标识诉讼参与人类型 1=自然人 2=法人 3=非法人组织
        self._LitigantType = 1
        # 10.法定代表人名称（专属于公司或非法人组织）
        self._LegalRepresentative = None
        # 11.法定代表人的身份证号码（专属于公司或非法人组织）
        self._LegalRepresentativeIdCode = None
        # 12.诉讼代理人属性（一个列表）
        self._LawsuitRepresentative = []
        # 13.id属性，用于标识该诉讼参与人的唯一性
        self._LitigantId = generate(size=10,alphabet="0123456789")

    # ===========下面是Get方法 ===========

    # 定义外部获取诉讼参与人姓名的方法
    def GetName(self):
        return self._Name
    # 定义外部获取诉讼参与人身份证/统一社会信用代码的方法
    def GetIdCode(self):
        return self._IdCode
    # 定义外部获取诉讼参与人地址的方法
    def GetLocation(self):
        return self._Location
    # 定义外部获取诉讼参与人联系方式的方法
    def GetContactNumber(self):
        return self._ContactNumber
    # 定义外部获取诉讼参与人身份证照片/营业执照上传路径的方法
    def GetDocumentsPath(self):
        return self._DocumentsPath
    # 定义外部获取诉讼参与人在诉讼中的地位（原告、被告、第三人）的方法
    def GetLitigantPosition(self):
        return self._LitigantPosition
    # 定义外部获取诉讼代理人属性的方法
    def GetLawsuitRepresentative(self):
        if hasattr(self,"_LawsuitRepresentative"):
            return self._LawsuitRepresentative
        else:
            print("该诉讼参与人没有设置诉讼代理人属性")
            return None
    # 定义外部获取银行账户属性的方法
    def GetBankAccount(self):
        if hasattr(self,"_BankAccount"):
            return self._BankAccount
        else:
            # print("该诉讼参与人没有设置银行账户属性")
            return None
    # 定义外部获取是否为我方当事人的方法
    def IsOurClient(self):
        return self._OurClient
    # 定义外部获取诉讼参与人类型的方法
    def GetLitigantType(self):
        return self._LitigantType
    # 定义外部获取诉讼参与人性别的方法
    def GetSex(self):
        return self._Sex
    # 定义外部获取法定代表人名称的方法
    def GetLegalRepresentative(self):
        return self._LegalRepresentative
    # 定义外部获取法定代表人身份证号码的方法
    def GetLegalRepresentativeIdCode(self):
        return self._LegalRepresentativeIdCode
    # 定义外部获取诉讼参与人id的方法
    def GetLitigantId(self):
        return self._LitigantId
    

    # =========== 下面是Set方法 ===========
    # 定义外部设置诉讼参与人姓名的方法
    def SetName(self,Name,debug=False):
        if isinstance(Name,str):
            if Name == "":
                if debug:
                    print("SetName方法报错：诉讼参与人姓名不能为空")
                return
            else:
                self._Name = Name

    # 定义外部设置诉讼参与人身份证/统一社会信用代码的方法
    def SetIdCode (self,IdCode,debug=False):
        if isinstance(IdCode,str):
            if IdCode == "":
                if debug:
                    print("SetIdCode 方法报错：诉讼参与人身份证号码不能为空")
                return
            # # 如果是自然人，则调用id_validator库的验证方法，判断身份证号码是否合法
            # if not validator.is_valid(IdCode):
            #     if debug:
            #         print("SetIdCode 方法报错：身份证号码有误")
            #     return
            else:
                self._IdCode = IdCode

    # 定义外部设置诉讼参与人地址的方法
    def SetLocation(self,Location):
        if isinstance(Location,str):
            self._Location = Location

    # 定义外部设置诉讼参与人联系方式的方法
    def SetContactNumber(self,ContactNumber):
        self._ContactNumber = ContactNumber

    # 定义外部设置诉讼参与人身份证扫描件/营业执照扫描件上传路径的方法
    def SetDocumentsPath(self,DocumentsPath):
        if os.path.exists(DocumentsPath):
            self._DocumentsPath = DocumentsPath

    # 定义外部设置诉讼参与人在诉讼中的地位（原告、被告、第三人）的方法
    def SetLitigantPosition(self,LitigantPosition):
        if LitigantPosition in [1,2,3]:
            self._LitigantPosition = LitigantPosition
        if LitigantPosition in ["1","2","3"]:
            self._LitigantPosition = int(LitigantPosition)
        
    # 定义外部设置是否为我方当事人的方法
    def SetOurClient(self,OurClient):
        if isinstance(OurClient,bool):
            self._OurClient = OurClient
        if isinstance(OurClient,str):
            if OurClient == "是" or OurClient == "True" or OurClient == "true" or OurClient == "TRUE" or OurClient == "Yes" or OurClient == "yes" or OurClient == "YES" :
                self._OurClient = True
            if OurClient == "否" or OurClient == "False" or OurClient == "false" or OurClient == "FALSE" or OurClient == "No" or OurClient == "no" or OurClient == "NO":
                self._OurClient = False

    # 定义外部设置诉讼参与人类型的方法
    def SetLitigantType(self,LitigantType):
        if LitigantType in [1,2,3]:
            self._LitigantType = LitigantType

    # 定义外部设置诉讼参与人性别的方法
    def SetSex(self,SexIndex):
        if SexIndex in [-1,0,1]:
            self._Sex = SexIndex

    # 定义外部设置法定代表人名称的方法
    def SetLegalRepresentative(self,LegalRepresentative):
        if isinstance(LegalRepresentative,str):
            self._LegalRepresentative = LegalRepresentative

    # 定义外部设置法定代表人身份证号码的方法
    def SetLegalRepresentativeIdCode(self,LegalRepresentativeIdCode):

        if isinstance(LegalRepresentativeIdCode,str):
            
            if LegalRepresentativeIdCode == "":
                print("SetLegalRepresentativeIdCode方法报错：法定代表人身份证号码不能为空")
                return
            
            # 如果是读入的是字符串“None”，则将值设置为None
            if LegalRepresentativeIdCode == "None":
                self._LegalRepresentativeIdCode = None
                return
            
            # 调用id_validator库的验证方法，判断身份证号码是否合法
            if not validator.is_valid(LegalRepresentativeIdCode):
                print("SetLegalRepresentativeIdCode方法报错：法定代表人身份证号码有误")
                return
            else:
                self._LegalRepresentativeIdCode = LegalRepresentativeIdCode
                return
        else:
            print("SetLegalRepresentativeIdCode方法报错：传入的参数不是字符串")
            return

    # 定义内部根据规则设置诉讼参与人性别的方法
    def SetSexByRule(self,debug=False):
        # 先看诉讼参与人的属性是什么，如果是自然人，就可以设置性别属性
        if self._LitigantType == 1:
            # 如果有身份证号码，就可以判断性别
            if hasattr(self,"_IdCode"):
                # 判断男女, 1 = 男性 0 = 女性
                if len(self._IdCode) == 18:
                    if int(self._IdCode[16]) % 2 == 1:
                        self._Sex = 1
                        return
                    else:
                        self._Sex = 0
                        return
                else:
                    if debug:
                        print("SetSexByRule报错：身份证长度有误，因此无法自动设置性别")
                        return
            else:
                if debug:
                    print("SetSexByRule报错：该诉讼参与人对象还没有身份证号码，因此无法自动设置性别")
                    return

    def SetLitigantTypeByRule(self,debug=False):
        # 如果名称大于6个字，就视为公司或非法人组织
        if len(self._Name) > 6:
            # 如果名称里面包括公司就是法人，否则就视为非法人组织
            if "公司" in self._Name:
                self._LitigantType = 2
                return 
            else:
                UnincorporatedOrganizationStr = (
                    "厂","店","馆","部","行","中心"    #《个体工商户名称登记管理办法》第十条规定的个体工商户组织形式
                    "协会","商会","学会","研究会","促进会","联合会",   #《社会团体登记管理条例》第十二条第一款规定的社会团体
                    "基金会",    #《社会团体登记管理条例》第十二条第二款规定的基金会
                    "学校","大学","学院","医院","中心","院","园","所","馆","站","社"   #《社会团体登记管理条例》第十二条第三款规定的民办非企业单位
                    )
                for str in UnincorporatedOrganizationStr:
                    if str in self._Name:
                        self._LitigantType = 3
                        return
        # 如果名称小于6个字，就视为自然人
        else:
            self._LitigantType = 1
            return


    # ===========下面是Bind方法，用于绑定其他类的主体（共计2个）============

    # 绑定代理律师的方法
    def BindLawyer(self,LawsuitRepresentative,debug=False):
        # 随后判断传进来的参数是不是Lawyer对象，如果是就可以绑定LawsuitRepresentative（诉讼代理人）属性
        if isinstance(LawsuitRepresentative,Lawyer):
            # 判断是否有2个代理人，如果有就不再绑定
            if len(self._LawsuitRepresentative) == 2:
                print("BindLawyer方法报错：%s已经有2个代理律师，无法再绑定" % self._Name)
                return
            # 如果当前诉讼参与人没有代理人，则绑定的律师不能是实习律师，必须先绑定一个非实习律师
            if len(self._LawsuitRepresentative) == 0:
                if LawsuitRepresentative.IsInternLawyer():
                    print("BindLawyer方法报错：%s不能仅绑定实习律师" % self._Name)
                    return
            # 经过前面的条件过滤后，将传进来的代理人对象绑定到诉讼参与人的属性上
            self._LawsuitRepresentative.append(LawsuitRepresentative)
            print("BindLawyer方法信息：诉讼参与人%s已增加一个代理律师：%s" % (self._Name,self._LawsuitRepresentative._Name))
            return

    # 绑定银行账户的方法
    def BindBankAccount(self,ABankAccount,debug=False):
        # 随后判断传进来的参数是不是BankAccount对象，如果是就可以绑定BankAccount（银行账户）属性
        if isinstance(ABankAccount,BankAccount):
            self._BankAccount = ABankAccount
            if debug:
                print("BindBankAccount方法信息：诉讼参与人%s已绑定银行账户%s" % (self._Name,self._BankAccount._AccountNumber))
            return
        
        else:
            if debug:
                print("传入的参数并非银行账户对象，无法绑定")
            return


    # =============== 下面是Input方法 ===============

    # 定义通过一个txt的方法用于输入诉讼参与人信息
    # 该方法在后续如不需要的话，可废弃
    def InputLitigantInfoFromTxt(self,InfoFile,LitigantPosition=""):
        # 判断路径是否存在
        if not os.path.exists(InfoFile):
            print("InputLitigantInfoFromTxt函数报错：输入的文件路径不存在")
            return
        # 读取文件到LitigantInfoLines列表中
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            LitigantInfoLines = f.readlines()
        # 去除换行符
        LitigantInfoLines = [line.strip() for line in LitigantInfoLines]
        # 遍历每一行信息
        for line in LitigantInfoLines:
            # 判断是否为空行
            if line == "":
                continue
            # 判断是否为注释行
            if line[0] == "#":
                continue
            # 判断是否为赋值行
            if "=" not in line:
                continue
            # 将赋值行按照等号分割成两部分，key和information
            key,information = line.split("=")
            # 诉讼参与人的姓名属性
            if key == "Name":
                self.SetName(Name=information)
            # 诉讼参与人的身份证号码属性
            if key == "IdCode":
                self.SetIdCode (IdCode=information)
            # 诉讼参与人的地址属性
            if key == "Location":
                self.SetLocation(Location=information)
            # 诉讼参与人的联系方式属性
            if key == "ContactNumber":
                self.SetContactNumber(ContactNumber=information)
            # 诉讼参与人在诉讼中的地位属性
            if key == "LitigantPosition":
                self.SetLitigantPosition(LitigantPosition=information)
            # 诉讼参与人是否为我方当事人
            if key == "OurClient":
                self.SetOurClient(OurClient=information)
            # 法定代表人名称
            if key == "LegalRepresentative":
                self.SetLegalRepresentative(LegalRepresentative=information)
            # 法定代表人身份证号码  
            if key == "LegalRepresentativeIdCode":
                self.SetLegalRepresentativeIdCode(LegalRepresentativeIdCode=information)

        # 如果传入了LitigantPosition参数，就直接设置诉讼参与人的地位属性，方便前端传入
        if LitigantPosition != "":
            if LitigantPosition == "plaintiff":
                self.SetLitigantPosition(1)
            elif LitigantPosition == "defendant":
                self.SetLitigantPosition(2)
        
        # 先根据规则设置诉讼参与人的类型属性
        self.SetLitigantTypeByRule()
        # 再根据规则设置诉讼参与人的性别属性
        self.SetSexByRule()

    # 定义通过前端输入的方法用于输入诉讼参与人信息
    def InputLitigantInfoFromFrontEnd(self,LitigantInfoDict):
        if LitigantInfoDict is dict:
            for key in LitigantInfoDict.keys():
                if key == "name":
                    self.SetName(LitigantInfoDict[key])
                if key == "IdCode":
                    self.SetIdCode (LitigantInfoDict[key])
                if key == "location":
                    self.SetLocation(LitigantInfoDict[key])
                if key == "contactNumber":
                    self.SetContactNumber(LitigantInfoDict[key])
                if key == "documentsPath":
                    self.SetDocumentsPath(LitigantInfoDict[key])
                if key == "litigantPosition":
                    self.SetLitigantPosition(LitigantInfoDict[key])
                if key == "ourClient":
                    self.SetOurClient(LitigantInfoDict[key])
                if key == "legalRepresentative":
                    self.SetLegalRepresentative(LitigantInfoDict[key])
                if key == "legalRepresentativeIdCode":
                    self.SetLegalRepresentativeIdCode(LitigantInfoDict[key])

       

    # ========== 下面是Output方法 ========== 

    # 定义将当前诉讼参与人各项信息输出到屏幕的方法,属于方便测试用的方法，实际上并无作用
    def OutputLitigantInfoToScreen(self):
        if self._Name is None:
            print("姓名为空，该主体不存在\n")
            return
        else:
            print("该诉讼主体名称="+str(self._Name)+"\n")
            if self._IdCode is None:
                print("该诉讼主体身份证号码为空\n")
            else:
                print(str(self._Name)+"的身份证、统一社会信用代码="+str(self._IdCode)+"\n")
            if self._Location is None:
                print("该诉讼主体地址为空\n")
            else:
                print(str(self._Name)+"的地址="+str(self._Location)+"\n")
            if self._ContactNumber is None:
                print("该诉讼主体联系方式为空\n")
            else:    
                print(str(self._Name)+"的联系方式="+str(self._ContactNumber)+"\n")
            if self._DocumentsPath is None:
                print("该诉讼主体身份证明文件上传路径为空\n")
            else:    
                print(str(self._Name)+"的身份证明文件上传路径="+str(self._DocumentsPath)+"\n")
            
            # 输出性别
            if self._Sex == 1:
                print(str(self._Name)+"的性别为男")
            elif self._Sex == 0:
                print(str(self._Name)+"的性别为女")
            elif self._Sex == -1:
                print("该诉讼参与人并非自然人，无性别属性"+"\n")

            # 输出诉讼地位
            if self._LitigantPosition == 1:
                print(str(self._Name)+"的诉讼地位为原告"+"\n")
            elif self._LitigantPosition == 2:
                print(str(self._Name)+"的诉讼地位为被告"+"\n")
            if self._LitigantPosition == 3:
                print(str(self._Name)+"的诉讼地位为第三人"+"\n")
            
            # 如果是公司或非法人组织具有法定代表人属性，则输出该属性
            if self._LitigantType == 2 or self._LitigantType == 3:
                print(str(self._Name)+"的法定代表人为"+str(self._LegalRepresentative)+"\n")
                print(str(self._Name)+"的法定代表人身份证号码为"+str(self._LegalRepresentativeIdCode)+"\n")

            # 输出是否为我方当事人
            if self._OurClient:
                print(str(self._Name)+"是我方当事人"+"\n")
            else:
                print(str(self._Name)+"不是我方当事人"+"\n")

            # 输出id
            print(str(self._Name)+"的id为"+str(self._LitigantId)+"\n")
            return 

    # 定义将当前诉讼参与人各项信息输出为字典的方法
    def OutputLitigantInfoToDict(self) -> dict:
        LitigantInfoDict = {}

        # 返回的字典中的键值对应的是前端需要的字段
        LitigantInfoDict["litigantName"] = self.GetName()
        LitigantInfoDict["litigantIdNumber"] = self.GetIdCode()
        LitigantInfoDict["litigantAddress"] = self.GetLocation()
        LitigantInfoDict["litigantPhoneNumber"] = self.GetContactNumber()
        LitigantInfoDict["litigantIsOurClient"] = self.IsOurClient()
        LitigantInfoDict["id"] = self.GetLitigantId()

        # 根据诉讼地位设置诉讼地位属性的字符串，分别为plaintiff、defendant、thirdParty
        if self.GetLitigantPosition() == 1:
            LitigantInfoDict["litigantPosition"] = "plaintiff"
        elif self.GetLitigantPosition() == 2:
            LitigantInfoDict["litigantPosition"] = "defendant"
        elif self.GetLitigantPosition() == 3:
            LitigantInfoDict["litigantPosition"] = "thirdParty"

        # 如果是公司具有法定代表人属性
        if self.GetLitigantType() == 2 or self.GetLitigantType() == 3:
            LitigantInfoDict["legalRepresentative"] = self.GetLegalRepresentative()
            LitigantInfoDict["legalRepresentativeIdNumber"] = self.GetLegalRepresentativeIdCode()

        # 对字典进行排序
        LitigantInfoDict = dict(sorted(LitigantInfoDict.items(),key=lambda x:x[0]))
        
        return LitigantInfoDict

        


# 设定律师类
class Lawyer():
    def __init__(self):
        # 1.姓名
        self._Name = ""
        # 2.身份证号码
        self._IdCode = ""
        # 3.联系地址
        self._Location = ""
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
    def GetLocation(self):
        return self._Location
    
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
    def SetLocation(self,Location):
        if isinstance(Location,str):
            self._Location = Location
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
            if "Location" in information:
                self._Location = information.split("=")[-1]
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
        print(self._Name+"律师的收件地址="+self._Location)
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
        LawyerInfoDict["lawyerIdNumber"] = self.GetIdCode()
        LawyerInfoDict["lawyerAddress"] = self.GetLocation()
        LawyerInfoDict["lawyerPhoneNumber"] = self.GetContactNumber()
        LawyerInfoDict["lawyerLicense"] = self.GetLawyerLicense()
        LawyerInfoDict["isInternLawyer"] = self.IsInternLawyer()

        # 排序
        LawyerInfoDict = dict(sorted(LawyerInfoDict.items(),key=lambda x:x[0]))
        
        return LawyerInfoDict


