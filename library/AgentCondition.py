import os,sys

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

class AgentCondition:

    def __init__(self) -> None:
        # 案件代理的阶段
        self._AgentStage = []
        # 风险代理情况
        self._RiskAgentStatus = None
        # 风险代理前期费用
        self._RiskAgentUpfrontFee = 0
        # 风险代理后期比例
        self._RiskAgentPostFeeRate = 0
        # 非风险代理的固定费用(是一个列表，第一个元素对应第一个阶段的费用，第二个元素对应第二个阶段的费用...)
        self._AgentFixedFeeList = []

    # ======= Get方法 ======= #
    # 获取案件代理的阶段
        # 案件代理的阶段
    def GetAgentStage(self):
        return self._AgentStage
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

    # ======= Set方法 ======= #

    # 案件代理阶段设定方法
    def SetAgentStage(self,AgentStage,DebugMode=False):
        if isinstance(AgentStage,list):
            # 对比新列表的数字是否与现有的列表重复
            for i in AgentStage:
                if i not in self._AgentStage and i in [1,2,3,4,5]:
                    self._AgentStage.append(i)
        elif isinstance(AgentStage,int):
            if AgentStage not in self._AgentStage and AgentStage in [1,2,3,4,5]:
                self._AgentStage.append(AgentStage)
        else:
            if DebugMode:
                print("SetAgentStage报错：该输入对象的类型与属性不匹配,案件代理阶段输入值为列表或1-5的整数")

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
                if len(AgentFixedFeeList) <= len(self.GetAgentStage()):
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
    

    # ======= Input方法 ======= #
    def InputFromDict(self,InfoFile,DebugMode=False) -> str:

        if not isinstance(InfoFile,dict):
            if DebugMode:
                print("InputFromDict报错：输入值不是字典")
            return "Error"
        
        # 正式部分
        for key, value in InfoFile.items():
            # 案件代理阶段
            if key == "agentStage":
                self.SetAgentStage(value)
            # 风险代理情况
            if key == "riskAgentStatus":
                self.SetRiskAgentStatus(value)
            # 风险代理前期费用
            if key == "riskAgentUpfrontFee":
                self.SetRiskAgentUpfrontFee(value)
            # 风险代理后期比例
            if key == "riskAgentPostFeeRate":
                self.SetRiskAgentPostFeeRate(value)
            # 非风险代理的固定费用
            if key == "agentFixedFee":
                self.SetAgentFixedFeeByList(value)

        return "Success"
    
    # ======= Output方法 ======= #

    def OutputToDict(self) -> dict:

        OutputDict = {
            "agentStage":self.GetAgentStage(),
            "riskAgentStatus":self.GetRiskAgentStatus(),
            "riskAgentUpfrontFee":self.GetRiskAgentUpfrontFee(),
            "riskAgentPostFeeRate":self.GetRiskAgentPostFeeRate(),
            "agentFixedFee":self.GetAgentFixedFee()
        }

        # 排序
        OutputDict = dict(sorted(OutputDict.items(), key=lambda item: item[0]))

        return OutputDict