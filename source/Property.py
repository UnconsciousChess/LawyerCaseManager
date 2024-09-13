import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

# 设定银行账户类
class BankAccount():

    def __init__(self) -> None:
        self._AccountName = ""
        self._AccountNumber = ""
        self._BankName = ""

    # ======= Get方法 ======= #

    # 定义外部获取银行账户名的方法
    def GetAccountName(self):
        return self._AccountName
    # 定义外部获取银行账户号码的方法
    def GetAccountNumber(self):
        return self._AccountNumber
    # 定义外部获取开户行的方法
    def GetBankName(self):
        return self._BankName
    
    # ======= Set方法 ======= #

    # 定义外部设置银行账户名的方法
    def SetAccountName(self,AccountName):
        if isinstance(self._AccountName,str):
            self._AccountName = AccountName
            return
        
    # 定义外部设置银行账户号码的方法
    def SetAccountNumber(self,AccountNumber):
        if isinstance(self._AccountNumber,str):
            if  AccountNumber.isdigit():
                self._AccountNumber = AccountNumber
                return
            
    # 定义外部设置开户行的方法 
    def SetBankName(self,BankName):
        if isinstance(self._BankName,str):
            self._BankName = BankName
            return
        
    # ======= Input方法 ======= #

    # 通过一个字典输入银行账户信息
    def InputFromDict(self,InfoFile) -> str:

        if not isinstance(InfoFile,dict):
            return "Error"
        
        # 正式部分
        for key, value in InfoFile.items():
            # 银行账户名
            if key == "accountName":
                self.SetAccountName(value)
            # 银行账户号码
            if key == "accountNumber":
                self.SetAccountNumber(value)
            # 开户行名称
            if key == "bankName":
                self.SetBankName(value)
        return "Success"
    

    # ======= Output方法 ======= #

    # 输出银行账户信息到字符串
    def OutputToStr(self) -> str:
        return "户名: %s\n账号: %s\n开户行: %s\n" % (self.GetAccountName(),self.GetAccountNumber(),self.GetBankName())

    # 输出银行账户信息到字典
    def OutputToDict(self) -> dict:
        Info = {
            "accountName":self.GetAccountName(),
            "accountNumber":self.GetAccountNumber(),
            "bankName":self.GetBankName()
        }
        return Info