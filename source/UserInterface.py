import os,sys

# 不要生成字节码
sys.dont_write_bytecode = True

# 导入第三方webview模块
import webview

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 导入自写包InterfaceApi中的Api类
from library.InterfaceApi import Api
    

# 实例化这个api对象
WebApi = Api()

# 创建一个窗口实例
window = webview.create_window(title='WorkingDocumentGenerator', 
                               url='../interface/dist/index.html',
                               js_api = WebApi)

# 窗口循环
webview.start(debug=True)

