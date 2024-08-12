# 导入自带库
import sys,os
import shutil

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 导入自写库
from source.RenderFile import RenderFileInDocxtpl
from library.TemplateFile import TemplateFile

def ReadTemplateList(TemplateListDir) -> list[TemplateFile]: 
    # 本函数功能与效果：
    # 读取一个符合规则模板列表txt文件
    # 返回一个列表，列表中的每个元素都是一个TemplateFile对象  
    TemplateFilesList = []

    # 导入json库
    import json
    
    with open(TemplateListDir,"r",encoding="utf-8") as f:
        templatefiles = json.load(f)

        # 对文本进行逐行读取并判定
        for templatefile in templatefiles:
            # 实例化一个TemplateFile对象
            TemplateFileObj = TemplateFile()
            # 调用SetTemplateFileFromJsonDict方法，将读取到的json转化为TemplateFile对象
            Result = TemplateFileObj.SetTemplateFileFromJsonDict(templatefile)
            # 如果Result是Success,则将处理好的TemplateFile对象放入列表中
            if Result == "Success":
                TemplateFilesList.append(TemplateFileObj)

    return TemplateFilesList


# 生成文件夹，同时调用source.RenderFile中的方法生成对应的文书   
def FolderCreator(case,OutputDir,TemplateListOrTemplateListDir,Initial) -> str: 

    # 检查传入的参数OutputDir
    if isinstance(OutputDir,str):
        # 如果OutputDir不存在，则报错
        if not os.path.exists(OutputDir):
            print("输出文件夹不存在！")
            return "OutputDirNotExists"
        # 如果OutputDir不是文件夹，则报错
        if not os.path.isdir(OutputDir):
            print("输出文件夹应该是一个文件夹！")
            return "OutputDirNotADir"

    # 检查传入的参数TemplateListOrTemplateListDir
    # 如果TemplateListOrTemplateListDir是一个字符串，则认为是模板列表文件的路径,则进行读取模板列表的操作
    if isinstance(TemplateListOrTemplateListDir,str):
        # 如果TemplateListDir存在，则读取模板列表
        if not os.path.exists(TemplateListOrTemplateListDir):
            print("模板列表文件不存在！")
            return "TemplateListDirNotExists"
        if not os.path.isfile(TemplateListOrTemplateListDir):
            print("模板列表文件应该是一个文件！")
            return "TemplateListDirNotAFile"

        # 确定路径无误且为文件以后，调用ReadTemplateList函数读取模板列表
        TemplateFilesList = ReadTemplateList(TemplateListOrTemplateListDir)

    # 如果TemplateListOrTemplateListDir是一个列表，则认为是模板列表，直接赋值给TemplateFilesList
    elif isinstance(TemplateListOrTemplateListDir,list):
        TemplateFilesList = TemplateListOrTemplateListDir
    # 如果TemplateListOrTemplateListDir不是字符串也不是列表，则报类型错误
    else:
        print("模板列表参数类型错误！")
        return "TemplateListTypeError"

    # 创建顶层的案件文件夹
    # 如果是第一次生成文件夹，则创建案件项目文件夹到指定目录Outputdir下面
    if Initial:
        os.chdir(OutputDir)
        # 其中项目文件夹名称由案件的原告、被告和案由组成
        FolderName = case.GetAllPlaintiffNames() + "诉" + case.GetAllDefendantNames() + "-" + case.GetCauseOfAction() + "一案"
        # 如果文件夹已经存在，则不创建；如果不存在，则创建
        if os.path.exists(FolderName):
            print("名称为【%s】的文件夹已经存在,不再创建。" % FolderName)
        else:
            os.makedirs(FolderName)
        
        # 将该名字作为该案件的文件夹地址
        case.SetCaseFolderPath(OutputDir + "//" + FolderName)
        # 最后进入该案件文件夹路径
        os.chdir(FolderName)

    # 如果不是第一次生成文件夹，则直接进入该文件夹的地址
    if not Initial:
        os.chdir(OutputDir)



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
    for stage,stageIsExist in StageStrDict.items():
        if stageIsExist:
            # 创建对应各阶段的文件夹
            RestainStage = str(FolderNum) + stage + "阶段"
            # 如果对应阶段的文件夹已经存在，则不创建；如果不存在，则创建
            if os.path.exists(RestainStage):
                print("名称为【%s】的文件夹已经存在,不再创建。" % RestainStage)
            else:
                os.makedirs(RestainStage)

            # 进入对应阶段文件夹
            os.chdir(RestainStage)

            # 从TemplateFilesList中找到对应阶段的文件，再根据该文件的属性进行文件生成
            for TemplateFile in TemplateFilesList:
                # 如果该模板文件的阶段与当前阶段不符，则直接跳到下一个文件
                if TemplateFile.GetTemplateFileStage() != stage:
                    continue
                
                # 如果该模板文件的FileType为directCopy，调用shutil.copy函数，复制该文件到当前文件夹下
                if TemplateFile.GetTemplateFileType() == "directCopy":
                    shutil.copy(TemplateFile.GetTemplateFileDir(),
                                os.getcwd())
                # 如果该模板文件的FileType为docxtpl，调用RenderFileInDocxtpl函数，用模板来进行文书生成，并保存到当前文件夹下
                elif TemplateFile.GetTemplateFileType() == "docxtpl":
                    RenderFileInDocxtpl(TemplateFileDir=TemplateFile.GetTemplateFileDir(),
                                        Case=case,
                                        OutputDir=os.getcwd())
                    
            # 完成一个阶段的文件生成，下一文件夹序号+1
            FolderNum += 1
            # 返回上一级目录
            os.chdir("..")
        else:
            print("无须生成%s阶段的文件夹及文档" % stage)

    # 回到之前的目录
    os.chdir(OutputDir)
    
    return "Success"









