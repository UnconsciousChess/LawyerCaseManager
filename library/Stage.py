import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

class Stage:
    
    def __init__(self) -> None:
        # 审理的阶段名称
        self._StageName = None
        # 审理的法院名称
        self._CourtName = None
        # 该阶段的案号
        self._CaseNumber = None

        with open(r"Data\PublicInfomationList\CourtNameList.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
        # 去除每个法院名称的换行符,并将其赋值给全局 StandardCourtList
        global StandardCourtNamesList 
        StandardCourtNamesList = [i.strip() for i in lines]

    #  === Get方法 ===    
    def GetStageName(self):
        return self._StageName
    def GetCourtName(self):
        return self._CourtName
    def GetCaseNumber(self):
        return self._CaseNumber
    

    #  === Set方法 ===
    def SetStageName(self, Stage) -> str:
        if Stage not in ['一审', '二审', '再审', '执行','仲裁']:
           print("应输入一审、二审、再审、执行、仲裁中的一个")
           return "Error"
        self._StageName = Stage
        return "Success"
    
    def SetCourtName(self, CourtName) -> str:
        # 判断输入的法院名称是否在标准法院名称列表中
        if CourtName not in StandardCourtNamesList:
            print("输入的法院名称不在标准法院名称列表中")
            return "Error"
        
        # 如果在标准法院名称列表中，则赋值给全局变量 Name
        self._CourtName = CourtName
        return "Success"
    
    def SetCaseNumber(self, CaseNumber) -> str:
        # 去掉空格后赋值
        self._CaseNumber = CaseNumber.strip()
        return "Success"
    

    # === input方法 ===
    def InputStageByString(self, InfoString) -> str:
        # 通过字符串输入阶段信息
        # 例：阶段,法院名称,案号

        # 通过逗号分隔字符串
        try:
            StageName,CourtName,CaseNumber = InfoString.split(",")
        except:
            return "Error"
        
        # 赋值
        if self.SetStageName(StageName) == "Error":
            return "Error"
        if self.SetCourtName(CourtName) == "Error":
            return "Error"
        if self.SetCaseNumber(CaseNumber) == "Error":
            return "Error"
        
        # 返回成功
        return "Success"
    
    def InputStageByDict(self, InfoDict) -> str:
        # 通过字典输入阶段信息
        # 例：{"stage":"一审","courtName":"北京市第一中级人民法院","caseNumber":"（2019）京01民初100号"}

        # 赋值
        if self.SetStageName(InfoDict["stageName"]) == "Error":
            return "Error"
        if self.SetCourtName(InfoDict["courtName"]) == "Error":
            return "Error"
        if self.SetCaseNumber(InfoDict["caseNumber"]) == "Error":
            return "Error"
        
        # 返回成功
        return "Success"


    # === output方法 ===

    def OutputToString(self) -> str:
        # 通过字符串输出阶段信息
        return self._StageName + "," + self._CourtName + "," + self._CaseNumber + ";"
    
    def OutputToDict(self) -> dict:
        # 通过字典输出阶段信息
        OutputDict =  {"stageName":self._StageName,
                "courtName":self._CourtName,
                "caseNumber":self._CaseNumber}
        # 排序
        OutputDict = dict(sorted(OutputDict.items(), key=lambda item: item[0]))

        return OutputDict

    



    