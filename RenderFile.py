import time
import os,sys

# 导入第三方库python-docx
from docx import Document
from docx.shared import Pt    # 字体大小模块
# 导入第三方库docxtpl
from docxtpl import DocxTemplate

def DeleteFileIfExist(OutputDir,FileName) -> None:
    # 判断是否存在同名文件，如果存在就删除原文件
    if os.path.exists(OutputDir + "\\" + os.path.split(FileName)[1]):
        # 防止因文件被WINWORD或其他应用打开中而删除失败
        while True:
            try:
                os.remove(OutputDir + "\\" + os.path.split(FileName)[1])
                break
            except:
                time.sleep(3)
                print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")
    return
    

def RenderFileInDocxtpl(TemplateFileDir,Case,OutputDir) -> None:
        
    # 读取模板文件
    doc = DocxTemplate(TemplateFileDir)

    TemplaterFileName = TemplateFileDir.split("\\")[-1]
    
    context = {
        # 自动生成时间信息
        '年' : time.strftime("%Y",time.localtime()),
        '月' : time.strftime("%m",time.localtime()),
        '日' : time.strftime("%d",time.localtime()),
    }

    # 案件共同信息（非当事人信息）

    context["案由"] = Case.GetCauseOfAction()
    context["管辖法院"] = Case.GetJurisdiction()
    context["案号"] = Case.GetCaseCourtCode()
    context["委托阶段"] = Case.GetCaseAgentStageStr()

    # 委托付费信息

    # 先判断是否需要收费,如果status是None，则不需要收费；是True则为风险收费；是False则为固定收费
    if Case.GetRiskAgentStatus() is not None:
        # 先判断是否为风险收费
        if Case.GetRiskAgentStatus() == True:                 # 风险收费
            context["风险代理前期律师费"] = Case.GetRiskAgentUpfrontFee()
            context["风险代理后期比例"] = Case.GetRiskAgentPostFeeRate()
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
                            FixedFeeRuleStr += "二审阶段收费：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1                  
                        elif stage == 4:
                            FixedFeeRuleStr += "执行阶段收费" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 5:
                            FixedFeeRuleStr += "再审阶段：" + str(Case.GetAgentFixedFee()[i]) + "元；"
                            i += 1    
            # 最后赋值到RenderMaterial字典中的FixedAgentFeeRuleStr键里面
            context["固定代理费收费规则"] = FixedFeeRuleStr

    # 获取我方当事人列表
    OurClientList,OurClientSide = Case.GetOurClientListAndSide()
    # 如果代理原告
    if OurClientSide == "p":
        context['对方全部当事人'] = Case.GetAllDefendantNames()

    if OurClientSide == "d":
        context['对方全部当事人'] = Case.GetAllPlaintiffNames()
    
    # 得到我方当事人的字符串AllClients，以顿号分割
    AllClients = "" 
    for client in OurClientList:
        AllClients += client.GetName() + "、"
    context['我方全部当事人'] = AllClients[:-1]    # 去掉最后一个顿号

       
    MultipleFileList = ["授权委托书","征求意见表","账户确认书","提交材料清单","地址确认书"]
    # 判断是否为需要分开不同人做的材料
    for name in MultipleFileList:
        if name in TemplaterFileName:
            # 如果文件名在上述列表之中，则遍历我方当事人列表来逐个做
            for client in OurClientList:
                # 如果我方当事人是法人或者其他组织
                if client.GetLitigantType() == 2 or client.GetLitigantType() == 3:
                    # 如果该文书是自然人的模版，则跳过该当事人
                    if "自然人版"  in TemplaterFileName:
                        continue
                    # 下面获取法人代表名称
                    context["我方当事人法定代表人"] = client.GetLegalRepresentative()
                    # 获取法人代表身份证号码
                    context["我方当事人法定代表人身份号码"] = client.GetLegalRepresentativeIDCode()

                # 填入context
                context['我方当事人名称'] = client.GetName()
                context['我方当事人身份号码'] = client.GetIDCode()
                context['我方当事人地址'] = client.GetLocation()
                context['我方当事人电话'] = client.GetContactNumber()
                context['我方当事人银行账户名'] = client.GetBankAccount().GetAccountName()
                context['我方当事人开户行'] = client.GetBankAccount().GetBankName()
                context['我方当事人银行账户号码'] = client.GetBankAccount().GetAccountNumber()

                # 渲染模板
                doc.render(context)
                DocSaveName = TemplaterFileName.replace(".docx", "（" + client.GetName() + "）.docx")
                # 判断是否存在同名文件，如果存在就删除原文件
                DeleteFileIfExist(OutputDir,DocSaveName)
                # 保存文件
                doc.save(OutputDir + "\\" + DocSaveName)

    return
              

def RenderFileInDOCX(TemplateFileDir,Case,OutputDir) -> None:
    # 如果TemplateFile的文件名为起诉状，则用下面的代码
    if "起诉状" in TemplateFileDir.split("\\")[-1]:
        # 实例化一个Document对象
        Doc = Document(TemplateFileDir)
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
        if os.path.exists(OutputDir + "\\" + os.path.split(TemplateFileDir)[1]):
            # 防止因文件用word打开中而失败
            while True:
                try:
                    os.remove(OutputDir + "\\" + os.path.split(TemplateFileDir)[1])
                    break
                except:
                    time.sleep(3)
                    print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")

        # 最后保存文件
        FileName = OutputDir + "\\" + os.path.split(TemplateFileDir)[1]
        # 去掉文件名后缀
        FileName = FileName.replace(".docx","")
        # 加上原被告双方的名字，中间用"V."隔开，再加上后缀
        FileName += "（" + Case.GetAllPlaintiffNames() + "v." + Case.GetAllDefendantNames() + "）" + ".docx"
        # 保存文件
        Doc.save(FileName)


