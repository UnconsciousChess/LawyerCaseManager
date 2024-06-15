# 导入自带库
import sys,os
import shutil

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 导入案件类
from library.CaseClass import Case

# 导入自写库
from source.RenderFile import RenderFileInDocxtpl,RenderFileInDOCX

# 将当前文件夹加入sys.path
sys.path.append(os.path.split(sys.path[0])[0])
# 不产生字节码文件
sys.dont_write_bytecode = True


def FolderNameCreator(case) -> str:
    # 递归原告名称
    Plaintiffs = ""
    for litigant in case.GetPlaintiffList():
        Plaintiffs += litigant.GetName() + "、"
    # 递归被告名称
    Defendants = ""
    for litigant in case.GetDefendantList():
        Defendants += litigant.GetName() + "、"

    # 去掉原被告最后的顿号
    Plaintiffs = Plaintiffs[:-1]
    Defendants = Defendants[:-1]

    # 得到案由
    Cause = case.GetCauseOfAction()

    # 合并文件夹名称
    FolderName = Plaintiffs + "诉" + Defendants + Cause + "一案"
    
    return FolderName



def FolderCreator(case,OutputDir,TemplateListDir) -> None: 


    def ReadTemplateList(TemplateListDir):   # 读取模板列表的子函数
        # 设定一个字典，是模板类型和模板文件列表的关系
        TemplateFilesDict = {
            "委托":[],
            "立案":[],
            "审理":[],
            "执行":[],
            "归档":[]
        }
        CurrentTemplateType = ""
        with open(TemplateListDir,"r",encoding="utf-8") as f:
            lines = f.readlines()
            # 对文本进行逐行读取并判定
            for line in lines:
                if line.startswith("|"):
                    # 读取|后面的内容，并判断是否是模板类型
                    TemplateType = line.split("|")[1].strip()
                    if TemplateType in TemplateFilesDict.keys():
                       CurrentTemplateType = TemplateType
                       continue
                    else:
                        print("ReadTemplateList函数报错：模板类型错误无法识别")
                        return
                if line == "\n":            # 如果是空行，则跳过
                    continue
                else:                      #如果不是空行则进行后续判断
                    if CurrentTemplateType != "":
                        # 判断是否有@分隔符
                        if "@" not in line:
                            print("ReadTemplateList函数报错：该行不符合规则")
                            continue
                        # 分离用@分隔的信息
                        Filedir = line.split("@")[0].strip()
                        FileType = line.split("@")[1].strip()
                        # 判断FileType 是否为0和1，0代表该文件直接复制，1代表该文件后续需要替换填充
                        if FileType != "0" and FileType != "1" and FileType != "2":
                            print("ReadTemplateList函数报错：FileType错误，该行不符合规则，模板文件【%s】无法被添加到待生成的文件列表中"  % Filedir.split("\\")[-1])
                            continue
                        # 检查该行对应的文件是否存在，不存在则报错并跳过
                        if not os.path.exists(Filedir):
                            print("ReadTemplateList函数报错：文件不存在或路径错误")
                            continue
                        # 将文件路径和FileType组成元组，加入到字典中
                        TemplateFilesDict[CurrentTemplateType].append((Filedir,int(FileType)))

            
        return TemplateFilesDict
    
    # 如果TemplateListDir存在，则读取模板列表
    if os.path.exists(TemplateListDir):
        TemplateFilesDict = ReadTemplateList(TemplateListDir)
    else:
        print("模板列表文件不存在")
        return

    # 创建案件项目文件夹到指定目录Outputdir下面，其中项目文件夹名称由案件的原告、被告和案由组成
    os.chdir(OutputDir)
    FolderName = FolderNameCreator(case)
    # 如果文件夹已经存在，则不创建；如果不存在，则创建
    if os.path.exists(FolderName):
        print("名称为【%s】的文件夹已经存在，不再创建。" % FolderName)
    else:
        os.makedirs(FolderName)

    # 进入该案件文件夹路径
    os.chdir(FolderName)

    # 文件夹序号初始化
    FolderNum = 0
    
    # 设定一个字典，键名为各种阶段的字符串，键值为True和False，True代表该阶段需要准备材料，False代表无须准备材料可以跳过
    # 其中委托和归档阶段默认存在
    StageStrDict = {"委托":True,
                     "立案":False,
                     "审理":False,
                     "执行":False,
                     "归档":True
                     }
    # 根据案件的代理阶段，修改StageStrDict的值
    if case.GetCaseAgentStage() != None:
        for stage in case.GetCaseAgentStage():
            if stage == 1:   # 1代表一审立案阶段
                StageStrDict["立案"] = True
            elif stage == 2:  # 2代表一审审理阶段
                StageStrDict["审理"] = True
            elif stage == 3:  # 3代表二审阶段
                StageStrDict["审理"] = True
            elif stage == 4:   # 4代表执行阶段
                StageStrDict["执行"] = True
            elif stage == 5:  # 5代表再审阶段
                StageStrDict["审理"] = True

    # 遍历各阶段，根据委托阶段是否存在，决定是否创建对应阶段的文件夹
    for stage,stageisexist in StageStrDict.items():
        if stageisexist:
            # 创建对应各阶段的文件夹
            RestainStage = str(FolderNum) + stage + "阶段"
            # 如果对应阶段的文件夹已经存在，则不创建；如果不存在，则创建
            if os.path.exists(RestainStage):
                print("名称为【%s】的文件夹已经存在，不再创建。" % RestainStage)
            else:
                os.makedirs(RestainStage)

            # 进入对应阶段文件夹
            os.chdir(RestainStage)

            # 读取对应阶段的文件模板,fileandtype[0]为文件路径，fileandtype[1]为FileType
            for fileandtype in TemplateFilesDict[stage]:
                # 如果FileType为0，则直接复制该文件到这个文件夹下
                if fileandtype[1] == 0:
                    shutil.copy(fileandtype[0],os.getcwd())
                # 如果FileType为1，调用docxtpl库，直接用模板来进行文书生成
                elif fileandtype[1] == 1:
                    RenderFileInDocxtpl(TemplateFileDir=fileandtype[0],
                                        Case=case,
                                        OutputDir=os.getcwd())
                # 如果FileType为2，调用docx库，进行文书生成（更复杂一些）
                elif fileandtype[1] == 2:
                    RenderFileInDOCX(TemplateFileDir=fileandtype[0],
                                     Case=case,
                                     OutputDir=os.getcwd())
                else:
                    print("文件[%s]对应的FileType不是0/1/2,无法识别" % fileandtype[0])
            # 文件夹序号+1
            FolderNum += 1
            # 随后返回上一级目录
            os.chdir("..")
        else:
            print("无须生成%s阶段的文件夹及文档" % stage)









