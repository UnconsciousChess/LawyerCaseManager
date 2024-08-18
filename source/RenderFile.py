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


# 遍历文件夹，删除文件夹下与待生成文书同名的文件
def DeleteFileIfExist(OutputDir,FileName) -> None:

    # 判断是否存在同名文件，如果存在就删除原文件
    if os.path.exists(os.path.join(OutputDir,FileName)):
        # 防止因文件被WINWORD或其他应用打开中而删除失败
        while True:
            try:
                os.remove(os.path.join(OutputDir,FileName))
                break
            except:
                time.sleep(3)
                print("该文件被其他程序占用，删除原同名文件失败,等待3秒后重试")
    return
    
# 用docxtpl库来渲染文书
def RenderFileInDocxtpl(TemplateFileObj,Case) -> None:

    # 获取输出文件夹
    OutputDir = os.path.join(Case.GetCaseFolderPath(),
                             TemplateFileObj.GetRenderStage() + "阶段")

    # 读取模板文件
    doc = DocxTemplate(TemplateFileObj.GetDir())

    # 自动生成时间信息
    context = {
        'year' : time.strftime("%Y",time.localtime()),
        'month' : time.strftime("%m",time.localtime()),
        'day' : time.strftime("%d",time.localtime()),
    }

    # 案件共同信息（非当事人信息）
    context["causeOfAction"] = Case.GetCauseOfAction()

    context["caseAgentStage"] = Case.GetCaseAgentStageStr()

    # 获取全部原告信息
    context["allPlaintiffNames"] = Case.GetAllPlaintiffNames()
    # 获取全部被告信息
    context["allDefendantNames"] = Case.GetAllDefendantNames()

    # 获取事实和理由
    context["factAndReason"] = Case.GetFactAndReasonText()
    # 获取诉讼请求
    context["claimText"] = Case.GetClaimText()

    # 获取案件阶段的实例列表
    CaseStages = Case.GetStages()
    
    # 遍历各个阶段，获取各个阶段的法院名称和案号
    context["allCourtNames"] = Case.GetAllCourtNames()
    
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

    AgentCondition = Case.GetAgentCondition()

    if CaseCodeIsEmpty:
        context["agentContractCaseCode"] = "本案尚未立案，最终以实际案号为准"
    else:
        
        if AgentCondition.GetAgentStage() != None:
            for AgentStage in AgentCondition.GetAgentStage():
                if AgentStage == 1:
                    context["agentContractCaseCode"] = context["一审案号"]
                    break
                if AgentStage == 2:
                    context["agentContractCaseCode"] = context["二审案号"]
                    break
                if AgentStage == 3:
                    context["agentContractCaseCode"] = context["再审案号"]
                    break
                if AgentStage == 4:
                    context["agentContractCaseCode"] = context["执行案号"]
                    break
                if AgentStage == 5:
                    context["agentContractCaseCode"] = context["仲裁案号"]
                    break
                
    # 获取我方当事人列表以及我方代理原告还是被告
    UsList,OurSide = Case.GetOurClientListAndSide()

    # 获取每一原告身份信息的字典，并将其装到一个列表里面
    PlaintiffIdentityDict = {}
    # 用i来记录原告的序号
    i = 0
    for plaintiff in Case.GetPlaintiffList():
        i += 1
        PlaintiffIdentityDict[i] = plaintiff.OutputToDict()
    context["plaintiffs"] = PlaintiffIdentityDict

    # 获取每一被告身份信息的字典，并将其装到一个字典里面
    DefendantIdentityDict = {}
    # 用i来记录被告的序号
    i = 0
    for defendant in Case.GetDefendantList():
        i += 1
        DefendantIdentityDict[i] = defendant.OutputToDict()
    context["defendants"] = DefendantIdentityDict

    # 获取每一第三人身份信息的字典，并将其装到一个字典里面
    ThirdPartyIdentityDict = {}
    # 用i来记录第三人的序号
    i = 0
    for thirdparty in Case.GetThirdPartyList():
        i += 1
        ThirdPartyIdentityDict[i] = thirdparty.OutputToDict()
    context["thirdparties"] = ThirdPartyIdentityDict


    # 获取我方当事人的字典，将其装到一个字典里面
    UsDict = {}
    # 用i来记录我方当事人的序号
    i = 0
    for client in UsList:
        i += 1
        UsDict[i] = client.OutputToDict()
    context["us"] = UsDict


    # 读取委托付费信息
    # 判断是否需要收费,如果status是None，则不需要收费；是True则为风险收费；是False则为固定收费
    if AgentCondition.GetRiskAgentStatus() is not None:
        # 先判断是否为风险收费
        if AgentCondition.GetRiskAgentStatus() == True:                 # 风险收费
            context["riskAgentUpfrontFee"] = AgentCondition.GetRiskAgentUpfrontFee()
            context["riskAgentPostFeeRate"] = AgentCondition.GetRiskAgentPostFeeRate()
        if AgentCondition.GetRiskAgentStatus() == False:                # 固定收费
            FixedFeeRuleStr = ""
            i = 0
            # 先判断案件阶段与案件收费的长度是否一致
            if len(AgentCondition.GetAgentFixedFee()) == len(AgentCondition.GetAgentStage()):
                if AgentCondition.GetAgentFixedFee() != []:
                    for stage in AgentCondition.GetAgentStage():
                        if stage == 1:
                            FixedFeeRuleStr += "一审立案阶段收费：" + str(AgentCondition.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 2:
                            FixedFeeRuleStr += "一审审理阶段收费：" + str(AgentCondition.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 3:
                            FixedFeeRuleStr += "二审阶段收费：" + str(AgentCondition.GetAgentFixedFee()[i]) + "元；"
                            i += 1                  
                        elif stage == 4:
                            FixedFeeRuleStr += "执行阶段收费" + str(AgentCondition.GetAgentFixedFee()[i]) + "元；"
                            i += 1
                        elif stage == 5:
                            FixedFeeRuleStr += "再审阶段：" + str(AgentCondition.GetAgentFixedFee()[i]) + "元；"
                            i += 1    

            # 最后赋值到RenderMaterial字典中的fixedAgentFeeRule键里面
            context["fixedAgentFeeRule"] = FixedFeeRuleStr


    # 如果代理原告,对方全部当事人则为被告
    if OurSide == "p":
        OppositeSideLitigantList = Case.GetDefendantList()
        context["allOpponentNames"] = Case.GetAllDefendantNames()
    # 如果代理被告，对方全部当事人则为原告
    if OurSide == "d":
        OppositeSideLitigantList = Case.GetPlaintiffList()
        context["allOpponentNames"] = Case.GetAllPlaintiffNames()
    
    # 获取我方全部当事人名称
    context['ourClientNames'] = Case.GetOurClientNames()


    # 根据该模板文书的类型，判断是否需要分开生成文书（这是本函数的核心部分）

    # 如果多重渲染列表为空，则不需要分开生成文书，直接渲染
    if TemplateFileObj.GetMultiRenderOption() == "":

        # 定义后缀名
        Suffix = ".docx"
        # 直接渲染模板
        doc.render(context)
        # 判断是否存在同名文件，如果存在就删除原文件
        DeleteFileIfExist(OutputDir,TemplateFileObj.GetFileName() + Suffix)
        # 保存文件
        doc.save(os.path.join(OutputDir,TemplateFileObj.GetFileName()) + Suffix)

        print(os.path.join(OutputDir,TemplateFileObj.GetFileName()))
        print("文书【%s】已生成" % TemplateFileObj.GetFileName())

        return
        
    # 如果多重渲染设置为Us，则需要根据我方当事人分开生成文书
    elif TemplateFileObj.GetMultiRenderOption() == "Us":
        
        for litigant in UsList:

            context['oneOfUs'] = litigant.OutputToDict()
            context['oneOfUsBankAccount'] = litigant.GetBankAccount().OutputToDict()
            # 渲染模板
            doc.render(context)
            DocSaveName = TemplateFileObj.GetFileName() + "（" + litigant.GetName() + "）.docx"
            # 判断是否存在同名文件，如果存在就删除原文件
            DeleteFileIfExist(OutputDir,DocSaveName)
            # 保存文件
            doc.save(os.path.join(OutputDir,DocSaveName))
        
        return
    
    # 如果多重渲染设置为Opponents，则需要根据对方当事人分开生成文书
    elif TemplateFileObj.GetMultiRenderOption() == "Opponents":
        
        for oppositeLitigant in OppositeSideLitigantList:
            # 渲染模板

            context['oppositeLitigant'] = oppositeLitigant.OutputToDict()
            context['oppositeLitigantBankAccount'] = oppositeLitigant.GetBankAccount().OutputToDict()
            doc.render(context)
            DocSaveName = TemplateFileObj.GetFileName() + "（" + litigant.GetName() + "）.docx"
            # 判断是否存在同名文件，如果存在就删除原文件
            DeleteFileIfExist(OutputDir,DocSaveName)
            # 保存文件
            doc.save(os.path.join(OutputDir,DocSaveName))
        
        return
    
    # 如果多重渲染设置为Courts，则需要根据法院分开生成文书
    elif TemplateFileObj.GetMultiRenderOption() == "Courts":
            
        for stage in Case.GetStages():
            #  根据情况填入
            if stage.GetStageName() !="" and stage.GetCourtName() !="":
                context['courtName'] = stage.GetCourtName()
                context['stageName'] = stage.GetStageName()  
                context['caseNumber'] = stage.GetCaseNumber() 
                # 渲染模板
                doc.render(context)
                
                DocSaveName = TemplateFileObj.GetFileName().replace(".docx", "")
                DocSaveName += "({}-{}).docx".format(context['stageName'],context['courtName']) 
                print(DocSaveName)
                # 判断是否存在同名文件，如果存在就删除原文件
                DeleteFileIfExist(OutputDir,DocSaveName)
                # 保存文件
                doc.save(os.path.join(OutputDir,DocSaveName))
        
        return
    
    # 如果多重渲染设置为CourtsAndUs，则需要根据法院和我方当事人分开生成文书
    elif TemplateFileObj.GetMultiRenderOption() == "CourtsAndUs":
            
        for stage in Case.GetStages():
            #  根据情况填入
            if stage.GetStageName() !="" and stage.GetCourtName() !="":
                context['courtName'] = stage.GetCourtName()
                context['stageName'] = stage.GetStageName()  
                context['caseNumber'] = stage.GetCaseNumber()

                for litigant in UsList:

                    context['oneOfUs'] = litigant.OutputToDict()
                    context['oneOfUsBankAccount'] = litigant.GetBankAccount().OutputToDict()
                    # 渲染模板
                    doc.render(context)
                    DocSaveName = TemplateFileObj.GetFileName().replace(".docx", "")
                    DocSaveName += "({}-{}-{}).docx".format(context['stageName'],context['courtName'],litigant.GetName()) 
                    print(DocSaveName)
                    # 判断是否存在同名文件，如果存在就删除原文件
                    DeleteFileIfExist(OutputDir,DocSaveName)
                    # 保存文件
                    doc.save(os.path.join(OutputDir,DocSaveName))
        
        return
    
    # 如果多重渲染设置为CourtsAndOpponents，则需要根据法院和对方当事人分开生成文书
    elif TemplateFileObj.GetMultiRenderOption() == "CourtsAndOpponents":

        for stage in Case.GetStages():
            #  根据情况填入
            if stage.GetStageName() !="" and stage.GetCourtName() !="":
                context['courtName'] = stage.GetCourtName()
                context['stageName'] = stage.GetStageName()  
                context['caseNumber'] = stage.GetCaseNumber()

                for oppositeLitigant in OppositeSideLitigantList:
                    # 渲染模板
                    context['oppositeLitigant'] = oppositeLitigant.OutputToDict()
                    context['oppositeLitigantBankAccount'] = oppositeLitigant.GetBankAccount().OutputToDict()
                    doc.render(context)
                    DocSaveName = TemplateFileObj.GetFileName().replace(".docx", "")
                    DocSaveName += "({}-{}-{}).docx".format(context['stageName'],context['courtName'],oppositeLitigant.GetName()) 
                    print(DocSaveName)
                    # 判断是否存在同名文件，如果存在就删除原文件
                    DeleteFileIfExist(OutputDir,DocSaveName)
                    # 保存文件
                    doc.save(os.path.join(OutputDir,DocSaveName))
                    
            return
            
    
# 归档卷内目录自动生成功能
def RenderArchiveDirectory(TemplateFileDir,RenderDict,OutputDir) -> None:

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