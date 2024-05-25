from openpyxl import load_workbook

class Litigant():
    # 构造函数，在构造函数里面，先初始化各类属性，后面的添加通过后续添加函数来完成
    def __init__(self):
        # 1.姓名
        self._Name = ""
        # 2.身份证/统一社会信用代码
        self._IDCode = ""
        # 3.联系地址
        self._Location = ""
        # 4.联系方式
        self._ContactNumber = ""
        # 5.身份证照片/营业执照上传路径
        self._DocumentsPath = ""


    # 定义外部获取诉讼参与人姓名的方法
    def GetName(self):
        return self._Name
    # 定义外部获取诉讼参与人身份证/统一社会信用代码的方法
    def GetIDCode(self):
        return self._IDCode
    # 定义外部获取诉讼参与人地址的方法
    def GetLocation(self):
        return self._Location
    # 定义外部获取诉讼参与人联系方式的方法
    def GetContactNumber(self):
        return self._ContactNumber
    # 定义外部获取诉讼参与人身份证照片/营业执照上传路径的方法
    def GetDocumentsPath(self):
        return self._DocumentsPath
    # 定义外部获取诉讼代理人属性的方法
    def GetLawsuitRepresentative(self):
        if hasattr(self,"_LawsuitRepresentative"):
            return self._LawsuitRepresentative
        else:
            print("该诉讼参与人没有设置诉讼代理人属性")
            return None

    
    # 定义外部设置诉讼参与人姓名的方法
    def SetName(self,Name):
        self._Name = Name
    # 定义外部设置诉讼参与人身份证/统一社会信用代码的方法
    def SetIDCode(self,IDCode):
        self._IDCode = IDCode
    # 定义外部设置诉讼参与人地址的方法
    def SetLocation(self,Location):
        self._Location = Location
    # 定义外部设置诉讼参与人联系方式的方法
    def SetContactNumber(self,ContactNumber):
        self._ContactNumber = ContactNumber
    # 定义外部设置诉讼参与人身份证照片/营业执照上传路径的方法
    def SetDocumentsPath(self,DocumentsPath):
        self._DocumentsPath = DocumentsPath

    # 定义外部设置诉讼代理人属性的方法通过BindLawyer方法完成，因此不另外定义一个方法



    # 定义一个方法，该方法可以直接通过一个txt的方法用于输入诉讼参与人信息。
    # 该方法是一个暂时的方法接口，后续如果没有这个需要的话（比如后期都是通过excel或数据库读取，或者民事起诉状语义识别的话）
    # 该方法在后续如不需要的话，可废弃
    def UpdateLitigantInfoByTxt(self,InfoFile):
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            LitigantInfoFromTxt = f.read()
        LitigantInfoFromTxtList = LitigantInfoFromTxt.split("\n")
        for information in LitigantInfoFromTxtList:
            # 诉讼参与人的姓名属性
            if "Name" in information:
                self._Name = information.split("=")[-1]
            # 诉讼参与人的身份证号码或统一社会信用代码属性    
            if "IDCode" in information:
                self._IDCode = information.split("=")[-1]
            # 诉讼参与人的地址属性
            if "Location" in information:
                self._Location = information.split("=")[-1]
            # 诉讼参与人的联系方式属性
            if "ContactNumber" in information:
                self._ContactNumber = information.split("=")[-1]
            # 诉讼参与人的身份证明文件（身份证照片/营业执照）上传属性
            if "DocumentsPath" in information:
                self._DocumentsPath = information.split("=")[-1]
            # 诉讼参与人在诉讼中的地位（原告、被告、第三人）
            if "LitigantPosition" in information:
                try:
                    self._LitigantPosition = int(information.split("=")[-1])
                except:
                    print("诉讼参与人在诉讼中的地位输入错误，请输入整数")


    # 改变诉讼参与人各项属性的方法
    def UpdateInfo(self,**Attributes):
        for k,v in Attributes.items():
            # 改变姓名属性
            if k == "Name":
                if v is int:
                    print("姓名输入错误,不应当输入整数")
                elif v is float:
                    print("姓名输入错误,不应当输入浮点数")
                else:
                    # 赋值
                    self.Name = v
                    print("%s的姓名已更新" %(self.Name))
                    continue
            # 改变诉讼参与人身份证、统一社会信用代码的方法
            if k == "IDCode":
                if v is int:
                    print("输入错误,不应当输入整数")
                elif v is float:
                    print("输入错误,不应当输入浮点数")
                else:
                    # 赋值
                    self.IDCode = v
                    print("%s的身份证号码已更新为%s" %(self.Name,self.IDCode))
                    continue
            # 改变诉讼参与人地址的方法    
            if k == "Location":
                if v is int:
                    print("输入错误,不应当输入整数")
                elif v is float:
                    print("输入错误,不应当输入浮点数")
                else:
                    # 赋值
                    self.Location = v
                    print("%s的联系地址已更新为%s" %(self.Name,self.Location))
                    continue
            # 改变诉讼参与人联系方式的方法    
            if k == "ContactNumber":
                if v is float:
                    print("输入错误,不应当输入浮点数")
                else:
                    # 赋值
                    self.ContactNumber = v
                    print("%s的联系方式已更新为%s" %(self.Name,self.ContactNumber))
                    continue
            # 改变身份证明文件上传路径的方法 
            if k == "DocumentsPath":        
                if v is float:
                    print("输入错误,不应当输入浮点数")
                else:
                # 赋值
                    self.DocumentsPath = v 
                    print("%s的身份证明文件上传路径已更新为%s" %(self.Name,self.DocumentsPath))
                    continue

            
    # 定义打印当前诉讼参与人各项信息的方法,属于方便测试用的方法，实际上并无作用
    def PrintInfo(self):
        if self._Name is None:
            print("姓名为空，该主体根本不存在，拒绝打印")
            return
        else:
            print("该诉讼主体名称="+str(self._Name)+"\n")
            if self._IDCode is None:
                print("该诉讼主体身份证号码为空\n")
            else:
                print(str(self._Name)+"的身份证、统一社会信用代码="+str(self._IDCode)+"\n")
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
            return 0

    # 绑定代理律师的方法
    def BindLawyer(self,ALawyer):
        # 随后判断传进来的参数是不是LeadLawyer对象，如果是就可以绑定LawsuitRepresentative（诉讼代理人）属性
        if isinstance(ALawyer,LeadLawyer):
            self._LawsuitRepresentative = ALawyer
            print("%s的代理律师已绑定为%s" % (self._Name,self._LawsuitRepresentative._Name))
        else:
            print("传入的参数并非律师对象，无法绑定")

# ==在诉讼参与人的类的基础上，定义诉讼参与人（自然人）==
class PersonLitigant(Litigant):
    
    def __init__(self):
        # 调用父函数的构造函数
        super().__init__()

        # 自身的构造函数,初始化自己的独有特性
        # 自然人性别，默认为-1，即性别不明， 1 = 男性 0 = 女性
        self.__Sex = -1
        # 标识诉讼参与人的类型 1=自然人 2=法人 3=非法人组织
        self.__LitigantType = 1
    
    #  定义外部获取诉讼参与人性别的方法
    def GetSex(self):
        if self.__Sex == -1:
            print("该诉讼参与人性别不明")
            return
        else:
            return self.__Sex
    #  定义外部获取诉讼参与人类型的方法
    def GetLitigantType(self):
        return self.__LitigantType

    # 根据身份证性别并填入属性的方法
    def LitigantGenerateSex(self):
        if hasattr(self,"_IDCode"):
            # 判断男女, 1 = 男性 0 = 女性
            if len(self._IDCode) == 18:
                if int(self._IDCode[16]) % 2 == 1:
                    self.__Sex = 1
                else:
                    self.__Sex = 0
            else:
                print("身份证长度有误")
        else:
            print("该诉讼参与人对象还没有身份证号码，因此无法判断性别")

    # 重写该函数，主要是加上自动运行判断性别的方法LitigantGetSex
    def UpdateLitigantInfoByTxt(self,InfoFile):
        super().UpdateLitigantInfoByTxt(InfoFile)
        # 调取父函数读取完信息以后，自动运行下面的函数
        self.LitigantGenerateSex()

    # 打印当前诉讼参与人各项信息的方法
    def  PrintInfo(self):
        # 先调用继承的父类
        super().PrintInfo()
        # 加入自身的情况
        if hasattr(self,"Sex"):
            if self.__Sex == 1:
                print(str(self._Name)+"的性别为男")
            if self.Sex == 0:
                print(str(self._Name)+"的性别为女")
        else:
            print("该实例无性别属性")
        return 0

    # 定义一个从excel文件当前行获取身份信息的函数
    def GetInfoFromExcel(ExcelFilePath):
        wb = load_workbook(ExcelFilePath)
        ws = wb.active()
        # 读取表头
        

# ==在诉讼参与人的类的基础上，定义诉讼参与人（公司或非法人组织）==
class CompanyLitigant(Litigant):
    
    def __init__(self):
        # 调用父函数的构造函数
        super().__init__()

        # 自身的构造函数
        # 法定代表人名称
        self.__LegalRepresentative = ""
        # 法定代表人的身份证号码
        self.__LegalRepresentativeIDCode = ""
    
    # 定义外部获取法定代表人名称的方法
    def GetLegalRepresentative(self):
        return self.__LegalRepresentative
    # 定义外部获取法定代表人身份证号码的方法
    def GetLegalRepresentativeIDCode(self):
        return self.__LegalRepresentativeIDCode
    #  定义外部获取诉讼参与人类型的方法
    def GetLitigantType(self):
        return self.__LitigantType

    # 定义外部设置法定代表人名称的方法
    def SetLegalRepresentative(self,LegalRepresentative):
        self.__LegalRepresentative = LegalRepresentative
    # 定义外部设置法定代表人身份证号码的方法
    def SetLegalRepresentativeIDCode(self,LegalRepresentativeIDCode):
        # 后续可能要在这里加上判断身份证号码合法性的代码，暂时先跳过，加快开发速度
        self.__LegalRepresentativeIDCode = LegalRepresentativeIDCode



    #定义一个方法，判断该诉讼参与人是法人还是非法人组织 2=法人 3=非法人组织
    def GetCompanyLitigantType(self):
        # 标识诉讼参与人的类型 1=自然人 2=法人 3=非法人组织
        # 如果名称里面包括公司就是法人，否则就视为非法人组织
        if "公司" in self._Name:
            self.__LitigantType = 2
            print("该诉讼参与人为法人")
        else:
            self.__LitigantType = 3
            print("该诉讼参与人为非法人组织")
        return 

    

    # 定义一个方法，该方法可以直接通过一个txt的方法用于输入诉讼参与人信息。
    # 该方法是一个暂时的方法接口，后续如果没有这个需要的话（比如后期都是通过excel或数据库读取，或者民事起诉状语义识别的话）
    # 该方法在后续如不需要的话，可废弃
    def UpdateLitigantInfoByTxt(self,InfoFile):
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            LitigantInfoFromTxt = f.read()
        LitigantInfoFromTxtList = LitigantInfoFromTxt.split("\n")
        for information in LitigantInfoFromTxtList:
            if "Name" in information:
                self.Name = information.split("=")[-1]
            if "IDCode" in information:
                self.IDCode = information.split("=")[-1]
            if "Location" in information:
                self.Location = information.split("=")[-1]
            if "ContactNumber" in information:
                self.ContactNumber = information.split("=")[-1]
            if "DocumentsPath" in information:
                self.DocumentsPath = information.split("=")[-1]
            if "LegalRepresentative" in information:
                self.LegalRepresentative = information.split("=")[-1]
            if "LegalRepresentativeIDCode" in information:
                self.LegalRepresentativeIDCode = information.split("=")[-1]
        # 在读取完材料以后，直接调用GetCompanyLitigantType判断类型
        self.GetCompanyLitigantType()

    def UpdateInfo(self, **Attributes):
        # 执行一次父函数
        super().UpdateInfo(**Attributes)
        # 下面是当对象类型为公司时增加检测的部分
        for k,v in Attributes.items():
            # 改变法定代表人名称
            if k == "LegalRepresentative":
                if isinstance(v,str):
                    # 赋值
                    self.LawsuitRepresentative = v
                    print("%s的法定代表人已更新为%s" %(self.Name,self.LawsuitRepresentative))
            # 改变法定代表人身份证号码
            if k == "LegalRepresentativeIDCode":
                if isinstance(v,str):
                    # 赋值
                    self.LegalRepresentativeIDCode = v
                    print("%s的法定代表人身份证号码已更新为%s" %(self.Name,self.LegalRepresentativeIDCode))
        return 

    def PrintInfo(self):
        super().PrintInfo()
        if hasattr(self,"LegalRepresentative"):
            print(str(self._Name)+"的法定代表人="+str(self._LegalRepresentative)+"\n")
        else:
            print("该实例缺少法定代表人属性")
        return 0
    


# ==在诉讼参与人（自然人）的类的基础上，定义主办律师的类LeadLawyer==
class LeadLawyer(PersonLitigant):

    def __init__(self):
        super().__init__()
        # 加入律师自身的属性初始化
        self._LawyerLicense = ""
        self.LawsuitPartner = None
        self._DeligationFiles = []
        return

    # 定义外部获取律师执业证号的方法
    def GetLawyerLicense(self):
        return self._LawyerLicense
    # 定义外部获取委托代理材料的方法
    def GetDeligationFiles(self):
        return self._DeligationFiles

    # 重写律师的printinfo函数
    def PrintInfo(self):
        print(self._Name+"律师的执业证号="+self._LawyerLicense)
        print(self._Name+"律师的身份证号="+self._IDCode)
        print(self._Name+"律师的联系方式="+self._ContactNumber)
        print(self._Name+"律师的收件地址="+self._Location)
        print(self._Name+"律师的律师证上传路径="+self._DocumentsPath)
        return 
    
    # 重写从txt读入的函数
    def UpdateLitigantInfoByTxt(self,InfoFile):
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            LitigantInfoFromTxt = f.read()
        LitigantInfoFromTxtList = LitigantInfoFromTxt.split("\n")
        for information in LitigantInfoFromTxtList:
            if "Name" in information:
                self._Name = information.split("=")[-1]
            if "IDCode" in information:
                self._IDCode = information.split("=")[-1]
            if "Location" in information:
                self._Location = information.split("=")[-1]
            if "ContactNumber" in information:
                self._ContactNumber = information.split("=")[-1]
            if "DocumentsPath" in information:
                self._DocumentsPath = information.split("=")[-1]
            if "LawyerLicense" in information:
                self._LawyerLicense = information.split("=")[-1]


    # 重写UpdateInfo函数
    def UpdateInfo(self, **Attributes):
        # 执行一次父函数
        super().UpdateInfo(**Attributes)
        # 下面是当对象类型为主办律师时增加检测的部分
        for k, v  in Attributes.items():
            # 改变律师执业证号
            if k == "LawyerLicense":
                if isinstance(v,str):
                    # 赋值
                    self.LawyerLicense = v
                    print("%s律师的律师执业证号已更新为%s" %(self.Name,self.LawyerLicense))  
            # 改变委托授权材料的上传列表
            if k == "DeligationFiles":
                if isinstance(v,list):
                    # 赋值
                    self.DeligationFiles = v
                    print("%s律师的委托授权材料列表已更新" %(self.Name)) 
            # 禁止通过该方法进行协办律师的绑定，特别写这一段提醒自己
            if k == "LawsuitPartner":
                print("禁止通过该方法进行协办律师的绑定,r如需要绑定协办律师应当使用BindLawyer方法")


    # 将bindlawyer方法重写为绑定协办律师的方法(但禁止主办律师再绑定主办律师)
    def BindLawyer(self,ALawyer):
        # 随后判断传进来的参数是不是辅办律师AssistLawyer对象，如果是就可以绑定LawsuitPartner（协办律师）属性
        if isinstance(ALawyer,AssistLawyer):
            self.LawsuitPartner = ALawyer
            print("%s的协办律师已绑定为%s" % (self.Name,self.LawsuitPartner.Name))
        else:
            if isinstance(ALawyer,LeadLawyer):
                print("禁止主办律师再绑定主办律师")
                return
            else:
                print("传入的参数并非协办律师对象，无法绑定")
        return


# ==在主办律师类的基础上，定义协办律师（实习人员）的类AssistLawyer==
class AssistLawyer(LeadLawyer):
    
    def __init__(self):
        super().__init__()
        # 删除AssistLawyer的Lawsuitpartner属性,因为协办律师不能再绑定其他协办律师了
        delattr(self,"LawsuitPartner")
        return

    # 协办律师重写BindLawyer方法，禁止再绑定
    def BindLawyer(self, ALawyer):
        print("禁止协办律师再绑定其他对象")
        return

