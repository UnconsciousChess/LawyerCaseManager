import os,sys

# 导入第三方webview模块
import webview

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 定义一个Api类，用于与前端交互 
class Api:
    def __init__(self):

        # case属性是一个列表，用于存放案件对象
        self._case = []
  
    # 该方法用于生成案件归档目录
    def generateArchiveDirectoryDocument(self,TemplateFilePath,SavedPath):
        # 导入自写包RenderFile中的RenderArchiveDirectory函数（生成归档目录）
        from source.RenderFile import RenderArchiveDirectory
        # 判断输入的路径是否存在
        if not os.path.exists(SavedPath):
            return "Error: The path is not exist!"
        else:
            # 执行归档目录生成
            RenderDict = {}      # 用于渲染的字典,格式为{key:(True/False,str)  
            RenderArchiveDirectory(TemplateFilePath,RenderDict,SavedPath)

        return f"归档目录生成成功,保存路径为{SavedPath}"
    
    # 该方法用于生成案件文件夹及依据模板生成对应的文件
    def generateCaseFolder(self,CaseFormDict):
        # 导入案件类Case
        from library.CaseClass import Case
        case = Case()
         # 导入自写包FolderCreator
        from source.Generator import FolderCreator
        # 将CaseFormDict中的数据，调用InputCaseInfoFromFrontEnd方法导入到当前case对象中
        case.InputCaseInfoFromFrontEnd(CaseFormDict)

        # # 如果保存路径不为空生成案件文件夹
        if case.GetCaseFolderPath() == "": 
            print("Error: The path is empty!")
            return 
        # 判断该路径是否存在
        if not os.path.exists(case.GetCaseFolderPath()):
            print("Error: The path is not exist!")
            return 
        
        # 检验无误后，执行案件文件夹生成的操作
        FolderCreator(case=case,                 # 传入案件对象
                      OutputDir=case.GetCaseFolderPath(),    # 传入保存路径
                      TemplateListDir=r"test\TestData\TemplateFilesList.txt")  # 传入模板文件列表路径
        
        print("=====================")

        # 最后将案件对象添加到案件列表中
        self._case.append(case)

        return 
    

# 实例化这个api对象
apiDiy = Api()

# 创建一个窗口实例
window = webview.create_window(title='WorkingDocumentGenerator', 
                               url='../interface/dist/index.html',
                               js_api = apiDiy)

# 窗口循环
webview.start(debug=False)

