import sys,os
import shutil
from docx import Document


# 将当前文件夹加入sys.path
sys.path.append(os.path.split(sys.path[0])[0])

# 不产生字节码文件
sys.dont_write_bytecode = True


from Library.CaseClass import Case


def FolderNameCreator(case):
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
    
    # 测试输出
    print(FolderName)

    return FolderName


def RenderFile(TemplateFile,Case):
    pass

def FolderCreator(case,OutputDir,TemplateListDir): 


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
                        if FileType != "0" and FileType != "1":
                            print("ReadTemplateList函数报错：FileType错误，该行不符合规则")
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
    
    # 测试输出
    for k,v in TemplateFilesDict.items():
        print(k,v)
    

    # 创建案件项目文件夹到指定目录Outputdir下面，其中项目文件夹名称由案件的原告、被告和案由组成
    os.chdir(OutputDir)
    FolderName = FolderNameCreator(case)
    # 如果文件夹已经存在，则不创建；如果不存在，则创建
    if os.path.exists(FolderName):
        print("名称为【%s】的文件夹已经存在，不再创建。" % FolderName)
    else:
        os.makedirs(FolderName)

    # 进入该案件文件夹
    os.chdir(FolderName)

    # 文件夹序号初始化
    FileNum = 0
    # 创建委托阶段文件夹
    RestainStage = str(FileNum)+".委托阶段"
    # 如果文件夹已经存在，则不创建；如果不存在，则创建
    if os.path.exists(RestainStage):
        print("名称为【%s】的文件夹已经存在，不再创建。" % RestainStage)
    else:
        os.makedirs(RestainStage)
    # 进入委托阶段文件夹
    os.chdir(RestainStage)
    # 读取委托文件模板
    for file in TemplateFilesDict["委托"]:
        # 如果FileType为0，则直接复制该文件到这个文件夹下
        if file[1] == 0:
            shutil.copy(file[0],os.getcwd())
        # 如果FileType为1，则需要替换填充，执行FileRender函数
        elif file[1] == 1:
            RenderFile(TemplateFile=file[0],Case=case)

    # 随后返回上一级目录
    os.chdir("..")
    # 创建立案阶段文件夹
    FileNum += 1
    FilingStage = str(FileNum)+".立案阶段"
    os.makedirs(FilingStage)
    # 创建审理阶段文件夹
    FileNum += 1
    TrialStage = str(FileNum)+".审理阶段"
    os.makedirs(TrialStage)
    # 创建执行阶段文件夹
    FileNum += 1
    ExecutionStage = str(FileNum)+".执行阶段"
    os.makedirs(ExecutionStage)
    # 创建归档阶段文件夹
    FileNum += 1
    ArchiveStage = str(FileNum)+".归档阶段"
    os.makedirs(ArchiveStage)
    # 创建其他材料文件夹
    FileNum += 1
    OtherDocuments = str(FileNum)+".其他材料"
    os.makedirs(OtherDocuments)










