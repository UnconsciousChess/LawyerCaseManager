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

    # 直接通过一个txt用于输入银行账户信息
    def InputInfoFromTxt(self,InfoFile) -> str:
        # 先对传入的路径进行判断
        if not os.path.exists(InfoFile):
            return "PathNotExists"
        if not os.path.isfile(InfoFile):
            return "NotFile"
        if InfoFile.endswith(".txt") == False:
            return "NotTxtFile"
        
        # 读取文件到列表中
        with open(file=InfoFile,mode="r",encoding="utf-8") as f:
            BankAccountInfoLines = f.readlines()
        # 去除每行的换行符
        BankAccountInfoLines = [line.strip() for line in BankAccountInfoLines]
        for line in BankAccountInfoLines:
            # 判断是否为空行
            if line == "":
                continue
            # 判断是否为注释行
            if line[0] == "#":
                continue
            # 判断是否为信息行
            key,information = line.split("=")
            # 银行账户名
            if key =="AccountName" :
                self.SetAccountName(information)
            # 银行账户号码
            if key == "AccountNumber":
                self.SetAccountNumber(information)
            # 开户行名称
            if key == "BankName":
                self.SetBankName(information)
        return "Success"