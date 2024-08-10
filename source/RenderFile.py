# 导入自带模块-时间
import time
# 导入自带模块-系统
import os,sys

# 导入第三方库docxtpl
from docxtpl import DocxTemplate
# 导入第三方库python-docx(目前还作为RenderArchiveDirectory的依赖库，看后续该函数是否也不要python-docx)
from docx import Document


# 不要生成字节码
sys.dont_write_bytecode = True


def CheckFolderPath(OutputDir) -> None:
    # 判断该文件夹路径是否以\结尾，如果不是则加上
    if OutputDir[-1] != "\\":
        OutputDir += "\\"
    return OutputDir

# 遍历文件夹，删除文件夹下与待生成文书同名的文件
def DeleteFileIfExist(OutputDir,FileName) -> None:
    # 检查OutputDir是否以\结尾，如果不是则加上
    OutputDir = CheckFolderPath(OutputDir) 
    # 判断是否存在同名文件，如果存在就删除原文件
    if os.path.exists(OutputDir + FileName):
        # 防止因文件被WINWORD或其他应用打开中而删除失败
        while True:
            try:
                os.remove(OutputDir + FileName)
                break
            except:
                time.sleep(3)
                print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")
    return
    
# 用docxtpl库来渲染文书
def RenderFileInDocxtpl(TemplateFileDir,Case,OutputDir) -> None:
    # 检查OutputDir是否以\结尾，如果不是则加上
    OutputDir = CheckFolderPath(OutputDir) 
    # 读取模板文件
    doc = DocxTemplate(TemplateFileDir)
    # 获取模板文件名
    TemplaterFileName = TemplateFileDir.split("\\")[-1]
    
    # 初始化文件是否在我方当事人需要分开的列表和对方当事人需要分开的列表
    CurrentTemplateFileIsInOurClientMultipleFileList = False
    CurrentTemplateFileIsInOppositeMultipleFileList = False
    CurrentTemplateFileIsInCourtMultipleFileList = False

    # 自动生成时间信息
    context = {

        '年' : time.strftime("%Y",time.localtime()),
        '月' : time.strftime("%m",time.localtime()),
        '日' : time.strftime("%d",time.localtime()),
    }

    # 案件共同信息（非当事人信息）
    context["案由"] = Case.GetCauseOfAction()

    context["委托阶段"] = Case.GetCaseAgentStageStr()

    # 获取全部原告信息
    context["全部原告名称"] = Case.GetAllPlaintiffNames()
    # 获取全部被告信息
    context["全部被告名称"] = Case.GetAllDefendantNames()

    # 获取事实和理由
    context["事实和理由"] = Case.GetFactAndReasonText()
    # 获取诉讼请求
    context["诉讼请求"] = Case.GetClaimText()

    # 获取案件阶段的实例列表
    CaseStages = Case.GetStages()
    
    # 默认案号为空
    CaseCodeIsEmpty = True

    # 遍历各个阶段，获取各个阶段的法院名称和案号
    for stage in CaseStages:
        if stage.GetStageName() == "一审":
            context["一审法院"] = stage.GetCourtName()
            context["一审案号"] = stage.GetCaseNumber()
            CaseCodeIsEmpty = False
        if stage.GetStageName() == "二审":
            context["二审法院"] = stage.GetCourtName()
            context["二审案号"] = stage.GetCaseNumber()
            CaseCodeIsEmpty = False
        if stage.GetStageName() == "再审":
            context["再审法院"] = stage.GetCourtName()
            context["再审案号"] = stage.GetCaseNumber()
            CaseCodeIsEmpty = False
        if stage.GetStageName() == "执行":
            context["执行法院"] = stage.GetCourtName()
            context["执行案号"] = stage.GetCaseNumber()
            CaseCodeIsEmpty = False
        if stage.GetStageName() == "仲裁":
            context["仲裁机构"] = stage.GetCourtName()
            context["仲裁案号"] = stage.GetCaseNumber()
            CaseCodeIsEmpty = False

    if CaseCodeIsEmpty:
        context["委托合同案号"] = "本案尚未立案，最终以实际案号为准"
    else:
        if Case.GetCaseAgentStage() != None:
            for AgentStage in Case.GetCaseAgentStage():
                if AgentStage == 1:
                    context["委托合同案号"] = context["一审案号"]
                    break
                if AgentStage == 2:
                    context["委托合同案号"] = context["二审案号"]
                    break
                if AgentStage == 3:
                    context["委托合同案号"] = context["再审案号"]
                    break
                if AgentStage == 4:
                    context["委托合同案号"] = context["执行案号"]
                    break
                if AgentStage == 5:
                    context["委托合同案号"] = context["仲裁案号"]
                    break
                

    # 获取每一原告身份信息的字典，并将其装到一个字典里面
    PlaintiffIdentityDict = {}
    # 用i来记录原告的序号
    i = 0
    for plaintiff in Case.GetPlaintiffList():
        i += 1
        PlaintiffIdentityDict[i] = plaintiff.OutputLitigantInfoToFrontEnd()
    context["plaintiffList"] = PlaintiffIdentityDict
    # print(PlaintiffIdentityDict)

    # 获取每一被告身份信息的字典，并将其装到一个字典里面
    DefendantIdentityDict = {}
    # 用i来记录被告的序号
    i = 0
    for defendant in Case.GetDefendantList():
        i += 1
        DefendantIdentityDict[i] = defendant.OutputLitigantInfoToFrontEnd()
    context["defendantList"] = DefendantIdentityDict
    # print(DefendantIdentityDict)

    # 获取每一第三人身份信息的字典，并将其装到一个字典里面
    ThirdPartyIdentityDict = {}
    # 用i来记录第三人的序号
    i = 0
    for thirdparty in Case.GetLegalThirdPartyList():
        i += 1
        ThirdPartyIdentityDict[i] = thirdparty.OutputLitigantInfoToFrontEnd()
    context["thirdpartyList"] = ThirdPartyIdentityDict
    # print(ThirdPartyIdentityDict)

    # 获取我方当事人列表以及我方代理原告还是被告
    OurClientList,OurClientSide = Case.GetOurClientListAndSide()

    # 获取我方当事人的字典，将其装到一个字典里面
    OurClientIdentityDict = {}
    # 用i来记录我方当事人的序号
    i = 0
    for client in OurClientList:
        i += 1
        OurClientIdentityDict[i] = client.OutputLitigantInfoToFrontEnd()
    context["ourClientList"] = OurClientIdentityDict
    # print(OurClientIdentityDict)


    # 读取委托付费信息
    # 判断是否需要收费,如果status是None，则不需要收费；是True则为风险收费；是False则为固定收费
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


    # 如果代理原告,对方全部当事人则为被告
    if OurClientSide == "p":
        context['对方全部当事人'] = context["全部被告名称"]
        OppositeSideLitigantList = Case.GetDefendantList()
    # 如果代理被告，对方全部当事人则为原告
    if OurClientSide == "d":
        context['对方全部当事人'] = context["全部原告名称"]
        OppositeSideLitigantList = Case.GetPlaintiffList()
    
    # 获取我方全部当事人名称
    context['我方全部当事人'] = Case.GetOurClientNames()

    # 判断是否为需要分开不同情况，根据同一模板生成不同的文件

    # 我方当事人需要分开的列表
    OurClientMultipleFileList = ["授权委托书","征求意见表","账户确认书","提交材料清单","地址确认书"]     
    # 对方当事人需要分开的列表
    OppositeMultipleFileList = ["线索书"]
    # 按照法院需要分开的列表，目前应该只有所函
    CourtMultipleFileList = ["所函"]

    # 判断本模板是否在【我方当事人需要分开的列表】
    for name in OurClientMultipleFileList:
        if name in TemplaterFileName:
            CurrentTemplateFileIsInOurClientMultipleFileList = True
    # 判断本模板是否在【对方当事人需要分开的列表】
    for name in OppositeMultipleFileList:
        if name in TemplaterFileName:
            CurrentTemplateFileIsInOppositeMultipleFileList = True
    # 判断本模板是否在【法院需要分开的列表】
    for name in CourtMultipleFileList:
        if name in TemplaterFileName:
            CurrentTemplateFileIsInCourtMultipleFileList = True

    # 如果当前文书是我方当事人需要分开的文书，则遍历我方当事人列表并分别生成
    if CurrentTemplateFileIsInOurClientMultipleFileList:
        for client in OurClientList:
            # 如果我方当事人是法人或者其他组织
            if client.GetLitigantType() == 2 or client.GetLitigantType() == 3:
                # 如果该文书是自然人的模版，则跳过该当事人
                if "自然人版"  in TemplaterFileName:
                    continue
                # 下面获取法人代表名称
                context["我方当事人法定代表人"] = client.GetLegalRepresentative()
                # 获取法人代表身份证号码
                context["我方当事人法定代表人身份号码"] = client.GetLegalRepresentativeIdCode()
            #  如果我方当事人是自然人
            if client.GetLitigantType() == 1:
                if "法人、其他组织版"  in TemplaterFileName:
                    continue
            # 填入context
            context['我方当事人名称'] = client.GetName()
            context['我方当事人身份号码'] = client.GetIdCode()
            context['我方当事人地址'] = client.GetLocation()
            context['我方当事人电话'] = client.GetContactNumber()
            
            # 如果当事人存在银行账户信息
            if client.GetBankAccount() != None:
                context['我方当事人银行账户名'] = client.GetBankAccount().GetAccountName()
                context['我方当事人开户行'] = client.GetBankAccount().GetBankName()
                context['我方当事人银行账户号码'] = client.GetBankAccount().GetAccountNumber()

            # 渲染模板
            doc.render(context)
            DocSaveName = TemplaterFileName.replace(".docx", "（" + client.GetName() + "）.docx")
            # 判断是否存在同名文件，如果存在就删除原文件
            DeleteFileIfExist(OutputDir,DocSaveName)
            # 保存文件
            doc.save(OutputDir + DocSaveName)

    # 如果当前文书是对方当事人需要分开的文书，则遍历对方当事人列表并分别生成
    if CurrentTemplateFileIsInOppositeMultipleFileList:
        for opposlitigant in OppositeSideLitigantList:
            # 如果该对方当事人是法人或者其他组织，则需要
            if opposlitigant.GetLitigantType() == 2 or opposlitigant.GetLitigantType() == 3:
                # 如果该文书是自然人的模版，则跳过该当事人
                if "自然人版"  in TemplaterFileName:
                    continue
                    # 下面获取法人代表名称
                context["对方当事人法定代表人"] = opposlitigant.GetLegalRepresentative()
                # 获取法人代表身份证号码
                context["对方当事人法定代表人身份号码"] = opposlitigant.GetLegalRepresentativeIdCode()                   
                #  如果我方当事人是自然人
            if opposlitigant.GetLitigantType() == 1:
                if "法人、其他组织版"  in TemplaterFileName:
                    continue
            # 填入context
            context['对方当事人名称'] = opposlitigant.GetName()
            context['对方当事人身份号码'] = opposlitigant.GetIdCode()
            context['对方当事人地址'] = opposlitigant.GetLocation()
            context['对方当事人电话'] = opposlitigant.GetContactNumber()

            # 渲染模板
            doc.render(context)
            DocSaveName = TemplaterFileName.replace(".docx", "（" + opposlitigant.GetName() + "）.docx")
            # 判断是否存在同名文件，如果存在就删除原文件
            DeleteFileIfExist(OutputDir,DocSaveName)
            # 保存文件
            doc.save(OutputDir + DocSaveName)


    # 如果当前文书是法院需要分开的文书，则遍历法院字典并分别生成
    if CurrentTemplateFileIsInCourtMultipleFileList:
        for stage in Case.GetStages():
            #  根据情况填入
            if stage.GetStageName() !="" and stage.GetCourtName() !="":
                context['管辖法院'] = stage.GetCourtName()
                context['委托阶段'] = stage.GetStageName()  
                # 渲染模板
                doc.render(context)
                
                DocSaveName = TemplaterFileName.replace(".docx", "")
                DocSaveName += "({}-{}).docx".format(context['委托阶段'],context['管辖法院']) 
                # 判断是否存在同名文件，如果存在就删除原文件
                DeleteFileIfExist(OutputDir,DocSaveName)
                # 保存文件
                doc.save(OutputDir + DocSaveName)

    # 如果当前文书不需要分开，则直接渲染
    if (not CurrentTemplateFileIsInOurClientMultipleFileList and 
        not CurrentTemplateFileIsInOppositeMultipleFileList  and 
        not CurrentTemplateFileIsInCourtMultipleFileList):
        # context['管辖法院'] = Case.GetJurisdictionDict()["一审"]
        # 直接渲染模板
        doc.render(context)
        # 判断是否存在同名文件，如果存在就删除原文件
        DeleteFileIfExist(OutputDir,TemplaterFileName)
        # 保存文件
        doc.save(OutputDir + TemplaterFileName)

    return
    
# 归档卷内目录自动生成功能
def RenderArchiveDirectory(TemplateFileDir,RenderDict,OutputDir) -> None:
    # 检查OutputDir是否以\结尾，如果不是则加上
    OutputDir = CheckFolderPath(OutputDir) 
    # 获取模板文件名
    TemplateFileName = TemplateFileDir.split("\\")[-1]
    # 实例化模板文件
    Doc = Document(TemplateFileDir)
    
    # 获取其中的表格,因为本文件只有一个表格，所以直接取第一个表格
    table = Doc.tables[0]
    
    # 目前没有发现这个包里面有直接获取对应单元格的行数和列数的方法，所以只能用下面的方法
    # 遍历表格中第一列的所有单元格，并将其行数储存在一个字典中
    RowNumberDict = {}
    RowNumber = 0
    for cell in table.columns[0].cells:
        # 单元格的文字作为字典的key，单元格的行数作为字典的value
        RowNumberDict[cell.text] = RowNumber
        RowNumber += 1

    # 对比两个字典，如果RenderDict的key在RowNumberDict的key中，说明该行属性是要渲染的，则按下面的规则进行
    for Tablekey in RowNumberDict.keys():
        for RenderDictkey in RenderDict.keys():
            # 如果表格中的某个单元格的文字与字典中的key相同
            if RenderDictkey in Tablekey:
                # 如果字典中的key对应的value的第一个元素为True，为原件
                if RenderDict[RenderDictkey][0] == True:
                    # 将该单元格所在行的第二列的文字变为√
                    table.cell(RowNumberDict[Tablekey],1).text = "√"
                # 如果字典中的key对应的value的第一个元素为False
                if RenderDict[RenderDictkey][0] == False:
                    # 将该单元格所在行的第三列的文字变为√
                    table.cell(RowNumberDict[Tablekey],2).text = "√"
                # 将该单元格所在行第四列的文字变为字典中的value的第二个元素
                table.cell(RowNumberDict[Tablekey],3).text = RenderDict[RenderDictkey][1]
                
    TemplateFileName += "（" + "已填充完成" + "）.docx"
    # 保存文件
    Doc.save(OutputDir + TemplateFileName)
    return