import os,sys

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 导入nanoid模块
from nanoid import generate

# 导入json模块
import json

# 导入诉讼参与人类
from .LitigantClass import *
from .Stage import *

import json
class Case():

    def __init__(self) -> None:
        # 初始化案件类的各项属性，均设为初始值
        # 案件类型
        self._CaseType = 0
        # 诉讼标的额
        self._LitigationAmount = 0
        # 案由
        self._CauseOfAction = ""      
        # 案件阶段(列表，每个元素为一个阶段对象)
        self._Stages = []
        # 上传文件列表
        self._UploadFilesList = {}
        # 诉讼请求（上诉请求）
        self._ClaimText = ""
        # 事实与理由
        self._FactAndReasonText = ""
        # 案件文件所在文件夹路径
        self._CaseFolderPath = ""
        # 原告主体列表,如原告[0]（原告一）、原告[1]（原告二）...
        self._PlaintiffList = []
        # 被告主体列表,如被告[0]（被告一）、被告[1]（被告二）...
        self._DefendantList = []
        # 第三人主体列表,如第三人[0]（第三人一）、第三人[1]（第三人二）...
        self._ThirdPartyList = []
        # 调解意向
        self._MediationIntention = False
        # 拒绝调解理由
        self._RejectMediationReasonText = ""
        # 案件代理的阶段
        self._CaseAgentStage = []
        # 风险代理情况
        self._RiskAgentStatus = None
        # 风险代理前期费用
        self._RiskAgentUpfrontFee = 0
        # 风险代理后期比例
        self._RiskAgentPostFeeRate = 0
        # 非风险代理的固定费用(是一个列表，第一个元素对应第一个阶段的费用，第二个元素对应第二个阶段的费用...)
        self._AgentFixedFeeList = []
        # 案件id（实例化案件时自动生成，用于前后端交互时识别）
        self._CaseId = "Case-" + generate(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', size=16)


        # 下面通过读取文件得到一些通用列表,并作为类的属性

        # 准备所有合法案由的列表，方便进行对比，以防止输入的案由有误
        with open(r"Data\PublicInfomationList\CauseOfActions-China.json","r",encoding="utf-8") as f:
            self._CauseOfActionList = json.load(f)


    # 下面是案件类的外部方法,包括:
    # a.获取各属性的方法（Get-xxxx)
    # b.设定各属性的方法(Set-xxxx、Append-xxx)
    # c.输入案件信息的方法(Input-xxx)
    # d.输出案件信息的方法(Output-xxx)

    # ==================Get方法：下面定义外部直接获取各属性的方法====================

    # 案件类型
    def GetCaseType(self):
        return self._CaseType
    # 诉讼标的额
    def GetLitigationAmount(self):
        return self._LitigationAmount
    # 案由
    def GetCauseOfAction(self):
        return self._CauseOfAction
    # 案件阶段
    def GetStages(self):
        return self._Stages
    # 上传文件列表
    def GetUploadFilesList(self):
        return self._UploadFilesList
    # 诉讼请求
    def GetClaimText(self):
        return self._ClaimText
    # 事实与理由
    def GetFactAndReasonText(self):
        return self._FactAndReasonText
    # 案件文件所在文件夹路径
    def GetCaseFolderPath(self):
        return self._CaseFolderPath
    # 原告主体列表
    def GetPlaintiffList(self):
        return self._PlaintiffList
    # 被告主体列表
    def GetDefendantList(self):
        return self._DefendantList
    # 第三人主体列表
    def GetThirdPartyList(self):
        return self._ThirdPartyList
    # 调解意愿
    def GetMediationIntention(self):
        return self._MediationIntention
    # 拒绝调解理由
    def GetRejectMediationReasonText(self):
        return self._RejectMediationReasonText
    # 案件代理的阶段
    def GetCaseAgentStage(self):
        return self._CaseAgentStage
    # 风险代理情况
    def GetRiskAgentStatus(self):
        return self._RiskAgentStatus
    # 风险代理前期费用
    def GetRiskAgentUpfrontFee(self):
        return self._RiskAgentUpfrontFee
    # 风险代理后期比例
    def GetRiskAgentPostFeeRate(self):
        return self._RiskAgentPostFeeRate
    # 非风险代理的固定费用数组
    def GetAgentFixedFee(self):
        return self._AgentFixedFeeList
    # 案件id
    def GetCaseId(self):
        return self._CaseId
    

    # ===== Get方法：下面定义外部获取各属性的一些进阶方法（主要涉及输出一些常用字符串）=====

    # 返回所有原告的名称字符串的函数
    def GetAllPlaintiffNames(self) -> str:
        Plaintiffs = ""
        for litigant in self._PlaintiffList:
            Plaintiffs += litigant.GetName() + "、"
        Plaintiffs = Plaintiffs[:-1]
        return Plaintiffs
    
    # 返回所有被告的名称字符串的函数
    def GetAllDefendantNames(self) -> str:
        Defendants = ""
        for litigant in self._DefendantList:
            Defendants += litigant.GetName() + "、"
        Defendants = Defendants[:-1]
        return Defendants
    
    # 返回代理阶段代码对应的中文字符串
    def GetCaseAgentStageStr(self) -> str:
        CaseAgentStageOutputString = ""
        if self._CaseAgentStage == []:
            return CaseAgentStageOutputString
        for i in self._CaseAgentStage:
            if i == 1:
                CaseAgentStageOutputString += "一审立案阶段,"
            elif i == 2:
                CaseAgentStageOutputString += "一审开庭阶段,"
            elif i == 3:
                CaseAgentStageOutputString += "二审阶段,"
            elif i == 4:
                CaseAgentStageOutputString += "执行阶段,"
            elif i == 5:
                CaseAgentStageOutputString += "再审阶段,"
        # 去掉最后一个顿号
        CaseAgentStageOutputString = CaseAgentStageOutputString[:-1]
        return CaseAgentStageOutputString        
    
    # 返回我方当事人列表及代理方向
    def GetOurClientListAndSide(self) -> list:
        OurClientList = []
        OurClientSide = ""
        for plaintiff in self.GetPlaintiffList():
            if plaintiff.IsOurClient():
                OurClientList.append(plaintiff)
                OurClientSide = "p"
        # 如果我方不是代理原告，则为代理被告
        if OurClientSide != "p" :
            for defendant in self.GetDefendantList():
                if defendant.IsOurClient():
                    OurClientList.append(defendant)
                    OurClientSide = "d"

        return OurClientList,OurClientSide

    def GetOurClientNames(self) -> str:
        OurClientList,OurClientSide = self.GetOurClientListAndSide()
        OurClientNames = ""
        for litigant in OurClientList:
            OurClientNames += litigant.GetName() + "、"
        OurClientNames = OurClientNames[:-1]
        return OurClientNames
    
    def GetCourtNameStr(self) -> str:
        CourtNameStr = ""
        for stage in self._Stages:
            if stage.GetCourtName() != "":
                CourtNameStr += stage.GetStageName() + ":" + stage.GetCourtName() + "、"  
        CourtNameStr = CourtNameStr[:-1]

        return CourtNameStr
    
    # 递归获取当前案件文件夹中的所有文件，返回一个文件列表FilesList
    def GetCaseFolderFiles(self, CurrentPath) -> list:

        FilesList = []
        for item in os.scandir(CurrentPath):
            if item.is_file():
                FilesList.append(item.path)
            elif item.is_dir():
                FilesList.extend(self.GetCaseFolderFiles(item.path))

        return FilesList


    # ============Set和Append方法：下面定义设定各属性的方法（含输入值校验）=============

    # 案件类型设定方法，1为民事案件，2为行政案件，3为执行案件
    def SetCaseType(self,CaseType,debugmode=False):
        if isinstance(CaseType,int):
            if CaseType == 1 or CaseType == 2 or CaseType == 3:
                self._CaseType = CaseType
            else:
                if debugmode:
                    print("SetCaseType报错：参数只能为1 2 3 ")
        else:
            if debugmode:
                print("SetCaseType报错：参数必须为整型") 
    
    # 诉讼标的额设定方法
    def SetLitigationAmount(self,LitigationAmount,debugmode=False):
        # 尝试将输入值转换为浮点数
        try:
            LitigationAmount = float(LitigationAmount)
        except:
            if debugmode:
                print("SetLitigationAmount报错：输入值并非浮点数")
            return
        # 诉讼标的额不能小于零
        if LitigationAmount >= 0:
            self._LitigationAmount = LitigationAmount
        else:
            if debugmode:
                print("SetLitigationAmount报错：诉讼标的不能小于零")
            return

    # 案由设定方法
    def SetCauseOfAction(self,CauseOfAction,debugmode=False):

        if (CauseOfAction in self._CauseOfActionList):
            self._CauseOfAction = CauseOfAction
            if debugmode:
                print("输入的案由【%s】添加成功" % CauseOfAction)
        else:
            if debugmode:
                print(" SetCauseOfActionb报错：输入的【%s】名称不符合现有民事、行政、执行案由规定,请重新输入" % CauseOfAction)
    


    def SetStage(self,StageInfo):
        # 如果输入的是一个Stage对象，就直接赋值
        if isinstance(StageInfo,Stage):
            # 如原本已存在该阶段的，直接更新
            for stage in self._Stages:
                if stage.GetStageName() == StageInfo.GetStageName():
                    stage = StageInfo
                    return
            
            # 如不存在该阶段的，则将该阶段添加到案件中
            self._Stages.append(StageInfo)
            return


        # 如果输入的是一个字典，就调用InputStageByDict方法
        elif isinstance(StageInfo,dict):
            # 如原本已存在该阶段的，直接更新
            for stage in self._Stages:
                if stage.GetStageName() == StageInfo["stageName"]:
                    stage.InputStageByDict(StageInfo)
                    return
                                
            # 如不存在该阶段的，则新建一个阶段对象
            stage = Stage()
            # 调用阶段对象的读取方法
            if stage.InputStageByDict(StageInfo) == "Success":
                # 调用添加阶段的方法，将该阶段添加到案件中
                self._Stages.append(stage)
            else:
                print("输入的阶段信息【%s】不符合规范" % StageInfo)  

        # 如果输入的是一个列表，就逐个调用InputStageByDict方法
        elif isinstance(StageInfo,list):
            StageInfoList = StageInfo

            for info in StageInfoList:
                # 如原本已存在该阶段的，直接更新
                for stage in self._Stages:
                    if stage.GetStageName() == info["stageName"]:
                        stage.InputStageByDict(info)
                        break
                else:
                    # 如原本不存在该阶段的，实例化一个阶段对象
                    stage = Stage()
                    # 调用阶段对象的读取方法
                    if stage.InputStageByDict(info) == "Success":
                        # 调用添加阶段的方法，将该阶段添加到案件中
                        self._Stages.append(stage)
                    else:
                        print("输入的阶段信息【%s】不符合规范" % info)  
        else:
            print("输入的阶段信息类型错误，请输入stage对象、字典或列表")


    # 诉讼请求设定方法
    def SetClaimText(self,ClaimText,debugmode=False) -> None:
        if isinstance(ClaimText,str):
            self._ClaimText = ClaimText
        else:
            if debugmode:
                print("SetClaimText报错：该输入对象的类型与属性不匹配,诉讼请求输入值为字符串")

    # 事实与理由设定方法
    def SetFactAndReasonText(self,FactAndReasonText,debugmode=False):
        if isinstance(FactAndReasonText,str):
            self._FactAndReasonText = FactAndReasonText
        else:
            if debugmode:
                print("SetFactAndReasonText报错：该输入对象的类型与属性不匹配,事实与理由输入值为字符串")

    # 案件案件生成文件夹路径设定方法
    def SetCaseFolderPath(self,CaseFolderPath,debugmode=False):
        if isinstance(CaseFolderPath,str):
            if os.path.exists(CaseFolderPath):
                # 判断输入的路径是否为文件路径
                if os.path.isfile(CaseFolderPath) == False:
                    self._CaseFolderPath = CaseFolderPath
                    if debugmode:
                        print("SetCaseFolderPath报错：案件文件所在文件夹路径设定成功")
                else:
                    if debugmode:
                        print("SetCaseFolderPath报错：输入的路径为文件路径，请重新输入")
            else:
                if debugmode:
                    print("SetCaseFolderPath报错：文件夹不存在，请重新输入")
        else:
            if debugmode:
                print("SetCaseFolderPath报错：该输入对象的类型与属性不匹配,案件文件所在文件夹路径输入值为字符串")
    
    # 备注设定方法
    def SetCommentText(self,Comment,debugmode=False):
        if isinstance(Comment,str):
            self._Comment = Comment
        else:
            if debugmode:
                print("SetCommentText报错：该输入对象的类型与属性不匹配,备注输入值为字符串")

    # 调解意愿设定方法
    def SetMediationIntention(self,MediationIntention,debugmode=False):
        if isinstance(MediationIntention,bool):
            self._MediationIntention = MediationIntention
        elif isinstance(MediationIntention,str):
            if MediationIntention == "True" or MediationIntention == "true" or MediationIntention == "TRUE" or MediationIntention == "1":
                MediationIntention = True
            elif MediationIntention == "False" or MediationIntention == "false" or MediationIntention == "FALSE" or MediationIntention == "0":
                MediationIntention = False
            self._MediationIntention = MediationIntention
        else:
            if debugmode:
                print("SetMediationIntention报错：该输入对象的类型与属性不匹配,调解意愿输入值为布尔值或字符串")

    # 拒绝理由设定方法
    def SetRejectMediationReasonText(self,RejectReason,DebugMode=False):
        if isinstance(RejectReason,str):
            self._RejectMediationReasonText = RejectReason
        else:
            if DebugMode:
                print("SetRejectMediationReasonText报错：该输入对象的类型与属性不匹配,拒绝理由输入值为字符串")

    # 案件代理阶段设定方法
    def SetCaseAgentStage(self,CaseAgentStage,DebugMode=False):
        if isinstance(CaseAgentStage,list):
            # 对比新列表的数字是否与现有的列表重复
            for i in CaseAgentStage:
                if i not in self._CaseAgentStage and i in [1,2,3,4,5]:
                    self._CaseAgentStage.append(i)
        elif isinstance(CaseAgentStage,int):
            if CaseAgentStage not in self._CaseAgentStage and CaseAgentStage in [1,2,3,4,5]:
                self._CaseAgentStage.append(CaseAgentStage)
        else:
            if DebugMode:
                print("SetCaseAgentStage报错：该输入对象的类型与属性不匹配,案件代理阶段输入值为列表或1-5的整数")

    # 风险代理情况设定方法
    def SetRiskAgentStatus(self,RiskAgentStatus,DebugMode=False):
        if isinstance(RiskAgentStatus,bool):
            self._RiskAgentStatus = RiskAgentStatus
        elif isinstance(RiskAgentStatus,str):
            if RiskAgentStatus == "True" or RiskAgentStatus == "true" or RiskAgentStatus == "TRUE" or RiskAgentStatus == "1":
                self._RiskAgentStatus = True
            elif RiskAgentStatus == "False" or RiskAgentStatus == "false" or RiskAgentStatus == "FALSE" or RiskAgentStatus == "0":
                self._RiskAgentStatus = False
        else:
            if DebugMode:
                print("SetRiskAgentStatus报错：该输入对象的类型与属性不匹配,风险代理情况输入值为布尔值或字符串")
    
    # 风险代理前期费用设定方法
    def SetRiskAgentUpfrontFee(self,RiskAgentUpfrontFee,DebugMode=False):
        # 尝试将输入值转换为浮点数
        try:
            RiskAgentUpfrontFee = float(RiskAgentUpfrontFee)
        except:
            if DebugMode:
                print("输入值并非浮点数")
            return
        # 诉讼标的额不能小于零
        if RiskAgentUpfrontFee >= 0:
            self._RiskAgentUpfrontFee = RiskAgentUpfrontFee
        else:
            if DebugMode:
                print("风险代理前期费用不能小于零")
            return
        
    # 风险代理后期比例设定方法
    def SetRiskAgentPostFeeRate(self,RiskAgentPostFeeRate,DebugMode=False):
        # 尝试将输入值转换为浮点数
        try:
            RiskAgentPostFeeRate = float(RiskAgentPostFeeRate)
        except:
            if DebugMode:
                print("SetRiskAgentPostFeeRate报错：输入值并非浮点数")
            return
        # 诉讼标的额不能小于零
        if RiskAgentPostFeeRate >= 0:
            self._RiskAgentPostFeeRate = RiskAgentPostFeeRate
        else:
            if DebugMode:
                print("SetRiskAgentPostFeeRate报错：风险代理后期比例不能小于零")
            return

    # 非风险代理的固定费用设定方法（方法一直接输入列表）
    def SetAgentFixedFeeByList(self,AgentFixedFeeList,DebugMode=False):
        # 判断是否原本列表式否非空
        if self._AgentFixedFeeList == []:
            # 判断输入值是否为列表
            if isinstance(AgentFixedFeeList,list):
                # 再次判断列表的数量是否小于等于代理阶段的数量
                if len(AgentFixedFeeList) <= len(self.GetCaseAgentStage()):
                    self._AgentFixedFeeList = AgentFixedFeeList
                else:
                    if DebugMode:
                        print("SetAgentFixedFee报错：输入的固定费用列表数量超出已有的代理阶段数量")
            else:
                if DebugMode:
                    print("SetAgentFixedFee报错：该输入对象的类型与属性不匹配,非风险代理的固定费用输入值为列表或整数")
        else:
            if DebugMode:
                print("SetAgentFixedFee报错：非风险代理的固定费用列表已经存在，无法再次设定")
    
    # 非风险代理的固定费用设定方法（方法二直接输入代理费用和代理阶段）
    def SetAgentFixedFeeByAdd(self,AgentFixedFee,Stage,DebugMode=False):
        # 判断输入值是否为整数
        if isinstance(AgentFixedFee,float) and isinstance(Stage,int):
            if Stage <= len(self.GetCaseAgentStage()-1):
                self._AgentFixedFeeList[Stage] = AgentFixedFee
            else:
                if DebugMode:
                    print("SetAgentFixedFee报错：输入的阶段序号超出已有的阶段序号")
        else:
            if DebugMode:
                print("SetAgentFixedFee报错：输入对象的类型与属性不匹配,非风险代理的固定费用输入值为列表或整数")
        


    # 添加诉讼参与人的方法
    def AppendLitigant(self,ALitigant) -> bool:
        # 先判断添加进来的东西是什么
        if isinstance(ALitigant,Litigant):
            # 判断诉讼地位是原告、被告还是第三人
            # 原告1  被告2  第三人3

            # 如果是原告
            if ALitigant.GetLitigantPosition() == "plaintiff":
                for index , plaintiff in enumerate(self._PlaintiffList):
                    if plaintiff.GetId() == ALitigant.GetId():
                        # 将PlaintiffList里面该原告的信息更新,即用新的Litigant对象替换掉原来的
                        self._PlaintiffList[index] = ALitigant
                        break
                # 如果PlaintiffList里面没有该原告的信息，则认为该litigant是新的原告，添加到PlaintiffList里面
                else:
                    self._PlaintiffList.append(ALitigant)

                return True
            
            # 如果是被告
            elif ALitigant.GetLitigantPosition()  == "defendant":
                for index , defendant in enumerate(self._DefendantList):
                    if defendant.GetId() == ALitigant.GetId():
                        # 将DefendantList里面该被告的信息更新,即用新的Litigant对象替换掉原来的
                        self._DefendantList[index] = ALitigant
                        break
                # 如果DefendantList里面没有该被告的信息，则认为该litigant是新的被告，添加到DefendantList里面
                else:
                    self._DefendantList.append(ALitigant)

                return True

            # 如果是第三人
            elif ALitigant.GetLitigantPosition() == "thirdParty":
                for index , thirdparty in enumerate(self._ThirdPartyList):
                    if thirdparty.GetId() == ALitigant.GetId():
                        # 将ThirdPartyList里面该第三人的信息更新,即用新的Litigant对象替换掉原来的
                        self._ThirdPartyList[index] = ALitigant
                        break
                # 如果ThirdPartyList里面没有该第三人的信息，则认为该litigant是新的第三人，添加到ThirdPartyList里面
                else:
                    self._ThirdPartyList.append(ALitigant)

                return True
            
            # 如果诉讼地位不是"plaintiff"、"defendant"、"thirdParty"，则返回False
            else:
                return False
            

    # 设定一个类的综合内部方法，对于参数键名和键值，分别进行处理
    def SetByKeyAndValue(self,Key,Value):
        # 根据Key的不同，调用不同的设定方法
        if Key == 'caseId' :
            # 如果案件Id为空，则自动生成一个
            if Value == "":
                self._CaseId = "Case-" + generate(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', size=16)
            # 如果案件Id不为空，则检验是否符合规范
            else:
                if Value[:5] == "Case-":
                    self._CaseId = Value
                else:
                    print("案件Id不符合规范，自动生成一个")
                    self._CaseId = "Case-" + generate(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', size=16)

        elif Key == 'caseType':
            self.SetCaseType(int(Value))

        elif Key == 'litigationAmount':
            self.SetLitigationAmount(float(Value))

        elif Key == 'causeOfAction':
            self.SetCauseOfAction(str(Value))
        
        elif Key == 'stages':
            self.SetStage(Value)

        elif Key == 'claimText':
            self.SetClaimText(str(Value))

        elif Key == 'factAndReason':
            self.SetFactAndReasonText(str(Value))

        elif Key == 'caseFolderGeneratedPath':
            self.SetCaseFolderPath(Value)

        elif Key == 'mediationIntention':
            self.SetMediationIntention(Value)
            
        elif Key == 'rejectMediationReasonText':
            self.SetRejectMediationReasonText(Value)

        elif Key == 'caseAgentStage':
            for stage in Value:
                self.SetCaseAgentStage(stage)

        elif Key == 'riskAgentStatus':
            self.SetRiskAgentStatus(Value)

        elif Key == 'riskAgentUpfrontFee':
            self.SetRiskAgentUpfrontFee(float(Value))

        elif Key == 'riskAgentPostFeeRate':
            self.SetRiskAgentPostFeeRate(float(Value))

        # elif Key == 'agentFixedFee':
        #     # 将Value转换为列表
        #     # 以逗号分割字符串,分割出各阶段的字符串列表
        #     FixedFeeList = Value.split(",")
        #     # 将字符串列表转换为浮点数列表
        #     FixedFeeList = [float(i) for i in FixedFeeList]
        #     self.SetAgentFixedFeeByList(FixedFeeList)
        
        elif Key == 'plaintiffs' or Key == 'defendants' or Key == 'legalThirdParties':
            for LitigantDict in Value:
                # 实例化一个诉讼参与人对象
                litigant = Litigant()
                # 调用诉讼参与人的读取方法
                litigant.InputFromDict(LitigantDict)
                # 调用AppendLitigant方法，添加该诉讼参与人到对应的列表中
                self.AppendLitigant(litigant)
   
    # ===========Input方法：下面定义批量输入案件信息的方法=============


    # 定义一个从字典中批量输入案件信息的方法
    def InputFromDict(self,CaseInfoDict,DebugMode=False) -> str:
        # 判断传入的参数是否为字典
        if not isinstance(CaseInfoDict,dict):
            if DebugMode:
                print("输入的案件信息不是字典")
            return "Error"
        # 对于字典中的逐个键值对读取，并调用SetCaseInfoWithKeyAndValue方法对键值对进行处理
        for Key,Value in CaseInfoDict.items():
            self.SetByKeyAndValue(Key,Value)

        return "Success"


    # ===========Output方法：下面定义输出案件信息的方法=============


    # 输出案件信息为字符串
    def OutputToStr(self) -> str:
        # 初始化输出字符串
        OutputStr = ""

        # 逐个输出案件信息
        OutputStr += "案件Id：%s\n" % self.GetCaseId()

        OutputStr += "案件文件夹路径：%s\n" % self.GetCaseFolderPath()

        if self.GetCaseType() == 1:
            OutputStr += "案件类型：民事案件\n"
        elif self.GetCaseType() == 2:
            OutputStr += "案件类型：行政案件\n"
        elif self.GetCaseType() == 3:
            OutputStr += "案件类型：执行案件\n"

        OutputStr += "诉讼标的：%s\n" % self.GetLitigationAmount()

        OutputStr += "案由：%s\n" % self.GetCauseOfAction()

        OutputStr += "各阶段信息：\n"
        for stage in self.GetStages():
            OutputStr += "%s" % stage.OutputToString()
        OutputStr += "\n"

        OutputStr += "诉讼请求：%s\n" % self.GetClaimText()

        OutputStr += "事实与理由：%s\n" % self.GetFactAndReasonText()

        if self.GetMediationIntention() == True:
            OutputStr += "调解意愿：愿意调解\n"
        else:
            OutputStr += "调解意愿：不愿意调解\n"

        OutputStr += "拒绝调解理由：%s\n" % self.GetRejectMediationReasonText()

        OutputStr += "案件代理阶段：%s\n" % self.GetCaseAgentStageStr()

        if self.GetRiskAgentStatus() == True:
            OutputStr += "采取风险收费\n"
            OutputStr += "风险代理前期费用：%s\n" % self.GetRiskAgentUpfrontFee()
            OutputStr += "风险代理后期比例：%s%%\n" % self.GetRiskAgentPostFeeRate()
        elif self.GetRiskAgentStatus() == False:
            OutputStr += "采取固定收费\n"
            OutputStr += "非风险代理的固定费用："
            if self.GetAgentFixedFee() == []:
                OutputStr += "无\n"
            else:
                for fee in self.GetAgentFixedFee():
                    OutputStr += "%s," % fee

        OutputStr += "\n=== 当事人信息 ===\n"

        # 原告列表
        index = 0
        for plaintiff in self.GetPlaintiffList():
            index += 1
            OutputStr += "原告" + str(index) + "\n" 
            OutputStr += plaintiff.OutputToStr() + "\n"

        # 被告列表
        index = 0
        for defendant in self.GetDefendantList():
            index += 1
            OutputStr += "被告" + str(index) + "\n"
            OutputStr += defendant.OutputToStr() + "\n"

        # 第三人列表
        index = 0
        for thirdparty in self.GetThirdPartyList():
            index += 1
            OutputStr += "第三人" + str(index) + "\n"
            OutputStr += thirdparty.OutputToStr() + "\n"

        # 最终输出
        return OutputStr

    # 输出案件信息成一个字典，便于后续转换为json，或直接提供给前端
    def OutputToDict(self,DebugMode=False) -> dict:
        # 需要返回的字典初始化
        OutputDict = {}

        OutputDict["caseAgentStage"] = self.GetCaseAgentStage()
        OutputDict["caseId"] = self.GetCaseId()
        OutputDict["caseType"] = self.GetCaseType()
        OutputDict["claimText"] = self.GetClaimText()
        OutputDict["causeOfAction"] = self.GetCauseOfAction()
        OutputDict["caseFolderGeneratedPath"] = self.GetCaseFolderPath()
        OutputDict["factAndReason"] = self.GetFactAndReasonText()
        OutputDict["litigationAmount"] = self.GetLitigationAmount()
        OutputDict["mediationIntention"] = self.GetMediationIntention()
        OutputDict["rejectMediationReasonText"] = self.GetRejectMediationReasonText()

        # 输出各个阶段的信息
        StageList = []
        for stage in self.GetStages():
            StageList.append(stage.OutputToDict())
        OutputDict["stages"] = StageList

        # 根据是否为风险收费代理，输出不同的费用信息
        if self.GetRiskAgentStatus() == True:     #风险收费
            OutputDict["riskAgentStatus"] = self.GetRiskAgentStatus()
            OutputDict["riskAgentUpfrontFee"] = self.GetRiskAgentUpfrontFee()
            OutputDict["riskAgentPostFeeRate"] = self.GetRiskAgentPostFeeRate()
            OutputDict["agentFixedFee"] = ""
        else:
            OutputDict["riskAgentStatus"] = self.GetRiskAgentStatus()
            OutputDict["riskAgentUpfrontFee"] = ""
            OutputDict["riskAgentPostFeeRate"] = ""
            OutputDict["agentFixedFee"] = self.GetAgentFixedFee()

        # 原告主体列表（列表归零）
        LitigantList = []
        for plaintiff in self.GetPlaintiffList():
            LitigantList.append(plaintiff.OutputToDict())
        OutputDict["plaintiffs"] = LitigantList

        # 被告主体列表（列表重新归零）
        LitigantList = []
        for defendant in self.GetDefendantList():
            LitigantList.append(defendant.OutputToDict())
        OutputDict["defendants"] = LitigantList

        # 第三人主体列表（列表重新归零）
        LitigantList = []
        for thirdparty in self.GetThirdPartyList():
            LitigantList.append(thirdparty.OutputToDict())
        OutputDict["thirdParties"] = LitigantList

        # 原告名字字符串
        OutputDict["plaintiffNames"] = self.GetAllPlaintiffNames()
        # 被告名字字符串
        OutputDict["defendantNames"] = self.GetAllDefendantNames()

        # 字典排序
        OutputDict = dict(sorted(OutputDict.items(),key=lambda x:x[0]))
        
        # 返回字典
        return OutputDict
    

