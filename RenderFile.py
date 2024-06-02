import time
import os,sys

# 导入第三方库python-docx
from docx import Document
from docx.shared import Pt    # 字体大小模块
# 导入第三方库docxtpl
from docxtpl import DocxTemplate


def RenderMaterialCreator(Case,number) -> dict:
    # 本函数用于生成渲染材料字典，用于填充模板文件
    # 输入值为案件的实例，通过一系列规则生成渲染材料字典
    # 输出值类型为字典

    # 初始化材料字典
    RenderMaterialDict = {}

    # 原被告姓名
    RenderMaterialDict["PlaintiffName"] = Case.GetPlaintiffList()[number].GetName()
    RenderMaterialDict["DefendantName"] = Case.GetDefendantList()[number].GetName()

    RenderMaterialDict["PlaintiffIDCode"] = Case.GetPlaintiffList()[number].GetIDCode()
    RenderMaterialDict["DefendantIDCode"] = Case.GetDefendantList()[number].GetIDCode()

    RenderMaterialDict["PlaintiffContactNumber"] = Case.GetPlaintiffList()[number].GetContactNumber()
    RenderMaterialDict["DefendantContactNumber"] = Case.GetDefendantList()[number].GetContactNumber()

    RenderMaterialDict["PlaintiffAddress"] = Case.GetPlaintiffList()[number].GetLocation()
    RenderMaterialDict["DefendantAddress"] = Case.GetDefendantList()[number].GetLocation()

    RenderMaterialDict["CauseOfAction"] = Case.GetCauseOfAction()
    RenderMaterialDict["Jurisdiction"] = Case.GetJurisdiction()

    RenderMaterialDict["BankAccountName"] = Case.GetPlaintiffList()[number].GetBankAccount().GetAccountName()
    RenderMaterialDict["BankName"] = Case.GetPlaintiffList()[number].GetBankAccount().GetBankName()
    RenderMaterialDict["BankAccountNumber"] = Case.GetPlaintiffList()[number].GetBankAccount().GetAccountNumber()
    

    # 如果原告是法人，则需要读取法人代表信息
    if Case.GetPlaintiffList()[number].GetLitigantType() == 2 or Case.GetPlaintiffList()[number].GetLitigantType() == 3:
        # 法人代表名称
         RenderMaterialDict["PlaintiffLegalRepresentative"] = Case.GetPlaintiffList()[number].GetLegalRepresentative()
        # 法人代表身份证号码
         RenderMaterialDict["PlaintiffLegalRepresentativeIDCode"] = Case.GetPlaintiffList()[number].GetLegalRepresentativeIDCode()
    else:
         RenderMaterialDict["PlaintiffLegalRepresentative"] = None
         RenderMaterialDict["PlaintiffLegalRepresentativeIDCode"] = None

    # 如果被告是法人，则需要读取法人代表信息
    if Case.GetDefendantList()[number].GetLitigantType() == 2 or Case.GetDefendantList()[number].GetLitigantType() == 3:
        # 法人代表名称
         RenderMaterialDict["DefendantLeagalRepresentative"] = Case.GetDefendantList()[number].GetLegalRepresentative()
    else:
         RenderMaterialDict["DefendantLeagalRepresentative"] = None
    
    # 委托部分
    # 先判断是否需要收费,如果status是None，则不需要收费；是True则为风险收费；是False则为固定收费
    if Case.GetRiskAgentStatus() is not None:
        # 先判断是否为风险收费
        if Case.GetRiskAgentStatus() == True:                 # 风险收费
            RenderMaterialDict["RiskAgentUpfrontFee"] = Case.GetRiskAgentUpfrontFee()
            RenderMaterialDict["RiskAgentPostFeeRate"] = Case.GetRiskAgentPostFeeRate()

        if Case.GetRiskAgentStatus() == False:                # 固定收费
            FixedFeeRuleStr = ""
            i = 0
            # 先判断案件阶段与案件收费的长度是否一致
            if len(Case.GetAgentFixedFee()) == len(Case.GetCaseAgentStage()):
                if Case.GetAgentFixedFee() != []:
                    for stage in Case.GetCaseAgentStage():
                        if stage == 1:
                            FixedFeeRuleStr += "一审立案阶段收费：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 2:
                            FixedFeeRuleStr += "一审审理阶段收费：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 3:
                            FixedFeeRuleStr += "二审阶段：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1                  
                        elif stage == 4:
                            FixedFeeRuleStr += "执行阶段收费" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 5:
                            FixedFeeRuleStr += "再审阶段：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1    
                    # 最后赋值到RenderMaterial字典中的FixedAgentFeeRuleStr键里面
                    RenderMaterialDict["FixedAgentFeeRuleStr"] = FixedFeeRuleStr
                else:
                    print("RenderMaterialCreator函数报错：固定收费列表为空，请检查")        
            else:
                print("RenderMaterialCreatorh函数报错：案件阶段与案件收费规则不一致，请检查")           
    return RenderMaterialDict


def RenderFileInDocxtpl(TemplateFile,Case,OutputDir) -> None:
        
    # 读取模板文件
    doc = DocxTemplate(TemplateFile)
    
    context = {
        # 自动生成时间信息
        '年' : time.strftime("%Y",time.localtime()),
        '月' : time.strftime("%m",time.localtime()),
        '日' : time.strftime("%d",time.localtime()),
    }

    # 用函数生成渲染材料字典
    RenderMaterialDict = RenderMaterialCreator(Case)
    # 将字典放入context中
    if "PlaintiffName" in RenderMaterialDict:
        context["原告"] = RenderMaterialDict["PlaintiffName"]
    if "DefendantName" in RenderMaterialDict:
        context["被告"] = RenderMaterialDict["DefendantName"]
    if "PlaintiffIDCode" in RenderMaterialDict:
        context["原告身份号码"] = RenderMaterialDict["PlaintiffIDCode"]
    if "DefendantIDCode" in RenderMaterialDict:
        context["被告身份号码"] = RenderMaterialDict["DefendantIDCode"]
    if "PlaintiffContactNumber" in RenderMaterialDict:
        context["原告电话"] = RenderMaterialDict["PlaintiffContactNumber"]
    if "DefendantContactNumber" in RenderMaterialDict:
        context["被告电话"] = RenderMaterialDict["DefendantContactNumber"]
    if "PlaintiffAddress" in RenderMaterialDict:
        context["原告地址"] = RenderMaterialDict["PlaintiffAddress"]
    if "DefendantAddress" in RenderMaterialDict:
        context["被告地址"] = RenderMaterialDict["DefendantAddress"]

    # 诉讼参与人为公司时
    if "PlaintiffLegalRepresentative" in RenderMaterialDict :
        context["原告法定代表人"] = RenderMaterialDict["PlaintiffLegalRepresentative"]
    if "PlaintiffLegalRepresentativeIDCode" in RenderMaterialDict:
        context["原告法定代表人身份号码"] = RenderMaterialDict["PlaintiffLegalRepresentativeIDCode"]
    if "DefendantLeagalRepresentative" in RenderMaterialDict:
        context["被告法定代表人"] = RenderMaterialDict["DefendantLeagalRepresentative"]

    # 案件信息
    if "CauseOfAction" in RenderMaterialDict:
        context["案由"] = RenderMaterialDict["CauseOfAction"]
    if "Jurisdiction" in RenderMaterialDict:
        context["管辖法院"] = RenderMaterialDict["Jurisdiction"]
    if "CourtCaseCode" in RenderMaterialDict:
        context["案号"] = RenderMaterialDict["CourtCaseCode"]
    if "CaseAgentStage" in RenderMaterialDict:
        context["委托阶段"] = RenderMaterialDict["CaseAgentStageStr"]

    # 执行人银行账户信息
    if "BankAccountName" in RenderMaterialDict:
        context["银行账户"] = RenderMaterialDict["BankAccountName"]
    if "BankName" in RenderMaterialDict:
        context["开户行"] = RenderMaterialDict["BankName"]
    if "BankAccountNumber" in RenderMaterialDict:
        context["账号"] = RenderMaterialDict["BankAccountNumber"]

    # 委托付费信息
    if "RiskAgentUpfrontFee" in RenderMaterialDict:
        context["风险代理前期律师费"] = RenderMaterialDict["RiskAgentUpfrontFee"]
    if "RiskAgentPostFeeRate" in RenderMaterialDict:
        context["风险代理后期比例"] = RenderMaterialDict["RiskAgentPostFeeRate"]
    if "FixedAgentFeeRuleStr" in RenderMaterialDict:
        context["固定代理费收费规则"] = RenderMaterialDict["FixedAgentFeeRuleStr"]

    # 当事人信息
    if "ClientName" in RenderMaterialDict:
        context["当事人"] = RenderMaterialDict["ClientName"]
    if "ClientIDCode" in RenderMaterialDict:
        context["'当事人身份号码"] = RenderMaterialDict["ClientIDCode"]

    # 将context填充到模板中
    doc.render(context)

    # 判断是否存在同名文件，如果存在就删除原文件
    if os.path.exists(OutputDir + "\\" + os.path.split(TemplateFile)[1]):
        # 防止因文件用word打开中而失败
        while True:
            try:
                os.remove(OutputDir + "\\" + os.path.split(TemplateFile)[1])
                break
            except:
                time.sleep(3)
                print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")
    
    # 最后保存文件
    doc.save(OutputDir + "\\" + os.path.split(TemplateFile)[1])


def RenderFileInDOCX(TemplateFile,Case,OutputDir) -> None:
    # 如果TemplateFile的文件名为起诉状，则用下面的代码
    if "起诉状" in TemplateFile.split("\\")[-1]:
        # 实例化一个Document对象
        Doc = Document(TemplateFile)
        for para in Doc.paragraphs:
            # 填写诉讼参与人信息
            if "LitigantInformation" in para.text:
                # 先删除该行
                para.text = ""
                para.style.font.size = Pt(12)
                # 写入所有原告信息
                for plaintiff in Case.GetPlaintiffList():
                    # 如果只有一个原告，就不用写序号
                    if len(Case.GetPlaintiffList()) == 1:
                        plaintiffinfo = "原告：" + plaintiff.GetName() + "，"
                    else:
                        plaintiffinfo = "原告" + str(Case.GetPlaintiffList().index(plaintiff)+1) + ":" + plaintiff.GetName() + "，"
                    if plaintiff.GetLitigantType() == 1:
                        plaintiffinfo +=  "身份证号码：" + plaintiff.GetIDCode() + "，" 
                    elif plaintiff.GetLitigantType() == 2 or plaintiff.GetLitigantType() == 3:
                        plaintiffinfo += "统一社会信用代码：" + plaintiff.GetIDCode() + "，"
                        plaintiffinfo += "法定代表人/负责人：" + plaintiff.GetLegalRepresentative() + "，"
                    # 地址和联系方式
                    if plaintiff.GetLocation() != None:
                        plaintiffinfo += "地址：" + plaintiff.GetLocation() + "，"
                    if plaintiff.GetContactNumber() != None:
                        plaintiffinfo += "联系方式：" + plaintiff.GetContactNumber() + "，"
                    # 删掉最后一个逗号
                    plaintiffinfo = plaintiffinfo[:-1]

                    run = para.add_run(plaintiffinfo + "\n")
                
                #原被告之间空一行
                para.add_run("\n")

                # 写入所有被告信息
                for defendant in Case.GetDefendantList():
                    # 如果只有一个被告，就不用写序号
                    if len(Case.GetDefendantList()) == 1:
                        defendantinfo = "被告：" + defendant.GetName() + "，"
                    else:    
                        defendantinfo = "被告" + str(Case.GetDefendantList().index(defendant)+1) + ":" + defendant.GetName() + "，"
                    if defendant.GetLitigantType() == 1:
                        defendantinfo +=  "身份证号码：" + defendant.GetIDCode() + "，" 
                    elif defendant.GetLitigantType() == 2 or defendant.GetLitigantType() == 3:
                        defendantinfo += "统一社会信用代码：" + defendant.GetIDCode() + "，"
                        defendantinfo += "法定代表人/负责人：" + defendant.GetLegalRepresentative() + "，"
                    # 地址和联系方式
                    if defendant.GetLocation() != None:
                        defendantinfo += "地址：" + defendant.GetLocation() + "，"
                    if defendant.GetContactNumber() != None:
                        defendantinfo += "联系方式：" + defendant.GetContactNumber() + "，"
                    # 删掉最后一个逗号
                    defendantinfo = defendantinfo[:-1]

                    run = para.add_run(defendantinfo + "\n")

            
            # 替换案由
            if "CauseOfAction" in para.text:
                para.text = para.text.replace("CauseOfAction",Case.GetCauseOfAction())
                para.style.font.size = Pt(12)
            # 替换此致后面的管辖法院
            if "CourtName" in para.text:
                para.text = para.text.replace("CourtName",Case.GetJurisdiction())
                para.style.font.size = Pt(12)
            # 写每个原告的姓名，每个空一行
            if "PlaintiffSignature" in para.text:
                # 把PlaintiffSignature删掉
                para.text = para.text.replace("PlaintiffSignature","")
                # 当事人为自然人时，在后面加上（签名）
                for plaintiff in Case.GetPlaintiffList():
                    count = 0
                    if plaintiff.GetLitigantType() == 1:
                        para.add_run(plaintiff.GetName() + "（签名）" )
                        count += 1
                    if plaintiff.GetLitigantType() == 2 or plaintiff.GetLitigantType() == 3:
                        para.add_run(plaintiff.GetName() + "（盖章）" )
                        count += 1
                    # 如果不是最后一个原告，则加一个换行
                    if count != len(Case.GetPlaintiffList()):
                        para.add_run("\n")
            # 落款后写日期
            if "SignatureDate" in para.text:
                para.text = para.text.replace("SignatureDate",time.strftime("%Y年%m月%d日",time.localtime())) 
                para.style.font.size = Pt(12)
            
        # 判断是否存在同名文件，如果存在就删除原文件
        if os.path.exists(OutputDir + "\\" + os.path.split(TemplateFile)[1]):
            # 防止因文件用word打开中而失败
            while True:
                try:
                    os.remove(OutputDir + "\\" + os.path.split(TemplateFile)[1])
                    break
                except:
                    time.sleep(3)
                    print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")

        # 最后保存文件
        FileName = OutputDir + "\\" + os.path.split(TemplateFile)[1]
        # 去掉文件名后缀
        FileName = FileName.replace(".docx","")
        # 加上原被告双方的名字，中间用"V."隔开，再加上后缀
        FileName += "（" + Case.GetAllPlaintiffNames() + "v." + Case.GetAllDefendantNames() + "）" + ".docx"
        # 保存文件
        Doc.save(FileName)


