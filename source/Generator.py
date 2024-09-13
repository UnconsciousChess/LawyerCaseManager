# 导入自带库
import sys,os
import shutil

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 导入自写库
from RenderFile import RenderFileInDocxtpl
from Class_TemplateFile import TemplateFile

def ReadTemplateList(TemplateListDir:str) -> list[TemplateFile]: 

    # 本函数功能与效果：
    # 读取一个符合规则的JSON文件，该JSON文件中包含了模板文件的信息
    # 返回一个列表，列表中的每个元素都是一个TemplateFile对象  
    TemplateFilesList = []

    # 导入json库
    import json
    
    with open(TemplateListDir,"r",encoding="utf-8") as f:
        templatefiles : list[dict] = json.load(f)

        # 对文本进行逐行读取并判定
        for templatefile in templatefiles:
            # 实例化一个TemplateFile对象
            TemplateFileObj = TemplateFile()
            # 调用SetTemplateFileFromJsonDict方法，将读取到的json转化为TemplateFile对象
            Result = TemplateFileObj.InputFromDict(templatefile)
            # 如果Result是Success,则将处理好的TemplateFile对象放入列表中
            if Result == "Success":
                TemplateFilesList.append(TemplateFileObj)

    return TemplateFilesList


# 生成案件内的文件夹
def FolderCreator(case,OutputDir) -> str: 

    # 设定一个字典，键名为各种阶段的字符串，键值为True和False，True代表该阶段需要准备材料，False代表无须准备材料可以跳过
    # 目前委托和归档阶段默认存在
    StageStrDict = {"委托":True,
                     "立案":False,
                     "审理":False,
                     "执行":False,
                     "归档":True
                     }
    AgentCondition = case.GetAgentCondition()
    # 根据案件的代理阶段，修改StageStrDict的值
    if AgentCondition.GetAgentStage() != None:
        for stage in AgentCondition.GetAgentStage():
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
            RestainStage = stage + "阶段"
            # 如果对应阶段的文件夹已经存在，则不创建；如果不存在，则创建该文件夹
            if os.path.exists(os.path.join(OutputDir,RestainStage)):
                print("名称为【%s】的文件夹已经存在,不再创建。" % RestainStage)
            else:
                os.makedirs(os.path.join(OutputDir,RestainStage))


    return "Success"


# 生成文件
def FilesGenerator(case,
                   OutputDir:str,
                   RenderTemplatesList:list[TemplateFile]) -> str:

    # 检查传入的参数OutputDir
    if not os.path.exists(OutputDir):
        print("输出文件夹不存在！")
        return "OutputDirNotExists"

    if not os.path.isdir(OutputDir):
        print("输出文件夹应该是一个文件夹！")
        return "OutputDirNotADir"
        

    #从TemplateFilesList中找到对应阶段的文件，再根据该文件的属性进行文件生成
    for TemplateFile in RenderTemplatesList:
        # 如果该模板文件的FileType为directCopy，调用shutil.copy函数，复制该文件到当前文件夹下
        if TemplateFile.GetRenderType() == "directCopy":
            shutil.copy(TemplateFile.GetDir(),
                        os.path.join(OutputDir,
                                     TemplateFile.GetRenderStage() + "阶段"))
        # 如果该模板文件的FileType为docxtpl，调用RenderFileInDocxtpl函数，用模板来进行文书生成，并保存到当前文件夹下
        elif TemplateFile.GetRenderType() == "docxtpl":
            RenderFileInDocxtpl(TemplateFileObj=TemplateFile,
                                Case=case)
                
    return "Success"








