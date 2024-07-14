## 概述

该文件主要是用于作为前后端交互的函数，通过 Pywebview 暴露给前端

## api 概览

后端内部使用的 api

- GetFilepath
- GetFolderpath

测试用的 api（后续可能删除）

- testCasesOutput
- testTemplateFilesOutput

下面按照调用 api 的组件来进行描述与分类

- CaseInfoForm
  - 输入类
    - inputCaseFromFrontEndForm
    - inputCaseFromTxt
    - inputAllCasesFromTxt
    - backEndDeleteCase
  - 输出类
    - outputCaseInfoToExcel
    - outputCaseInfoToTxt
    - outputAllCasesInfoToTxt
    - outputAllCaseInfoToFrontEnd
    - documentsGenerate
- CaseInfoEditForm
  - 输入类
    - inputLitigantFromTxt
  - 输出类
    - 暂无
- TemplateFileForm
  - 输入类
    - backEndAddTemplateFileData
    - backEndUpdateTemplateFileData
    - backEndDeleteTemplateFileData
  - 输出类
    - backEndPushTemplateFileDataToFrontEnd
    - backEndOutputTemplateFileData
- TemplateFileEditForm
  - 输入类
    - backEndChooseTemplateFile
  - 输出类
    - 暂无

## 详述

### CaseInfoForm

#### inputCaseFromFrontEndForm

##### 参数

| 名称         | 类型 |
| ------------ | ---- |
| CaseFormDict | dict |

##### 返回值

返回值类型为 str

| 取值      | 含义         |
| --------- | ------------ |
| "Success" | 函数执行成功 |
| "Fail"    | 函数执行失败 |

#### inputCaseFromTxt

##### 参数

无

##### 返回值

返回值类型为 str

| 取值      | 含义         |
| --------- | ------------ |
| "Success" | 函数执行成功 |
| "Fail"    | 函数执行失败 |

#### inputAllCasesFromTxt

##### 参数

无

##### 返回值

返回值类型为 str

| 取值      | 含义         |
| --------- | ------------ |
| "Success" | 函数执行成功 |
| "Fail"    | 函数执行失败 |

#### outputCaseInfoToExcel

##### 参数

| 名称   | 类型 |
| ------ | ---- |
| CaseId | str  |

##### 返回值

返回值类型为 str

| 取值              | 含义                               |
| ----------------- | ---------------------------------- |
| "Success"         | 函数执行成功                       |
| "CaseListIsEmpty" | self._cases 为空，即后端无案件实例 |

#### outputCaseInfoToTxt

##### 参数

| 名称   | 类型 |
| ------ | ---- |
| CaseId | str  |

##### 返回值

返回值类型为 str

| 取值              | 含义                               |
| ----------------- | ---------------------------------- |
| "Success"         | 函数执行成功                       |
| "CaseListIsEmpty" | self._cases 为空，即后端无案件实例 |

#### outputAllCasesInfoToTxt

##### 参数

无

##### 返回值

返回值类型为 str

| 取值           | 含义                                      |
| -------------- | ----------------------------------------- |
| "Success"      | 函数执行成功                              |
| "PathNotExist" | 通过后端调windows窗体，所读入的路径不存在 |
| "NotDirectory" | 所读入的路径并非一个文件夹                |

#### outputAllCaseInfoToFrontEnd

##### 参数

无

##### 返回值

返回值类型为 list

#### documentsGenerate

##### 参数

| 名称                | 类型 |
| ------------------- | ---- |
| CaseId              | str  |
| templateFilesIdList | list |

##### 返回值

返回值类型为 str

| 取值                   | 含义                                      |
| ---------------------- | ----------------------------------------- |
| "Success"              | 函数执行成功                              |
| "GeneratorError"       | 该函数所调用的GeneratorError              |
| "TemplateFilesIsEmpty" | self._templateFiles为空，即无模板文件实例 |

#### backEndDeleteCase

##### 参数

| 名称   | 类型 |
| ------ | ---- |
| CaseId | str  |

##### 返回值

返回值类型为 str

| 取值      | 含义                     |
| --------- | ------------------------ |
| "Success" | 后端对应的案件，删除成功 |
| "Fail"    | 后端对应的案件，删除失败 |

### CaseInfoEditForm

#### inputLitigantFromTxt

##### 参数

| 名称         | 类型 | 含义                                                  |
| ------------ | ---- | ----------------------------------------------------- |
| TxtPath      | str  | 诉讼参与人txt文档的对应绝对路径                       |
| LitigantType | str  | 诉讼参与人的类型，原告为"plaintiff";被告为"defendant" |

##### 返回值

返回值类型为 dict, 是一个符合前端读入接口（接口字段格式详见前端的对应文档）的字典

### TemplateFileForm

#### backEndAddTemplateFileData

##### 参数

无

##### 返回值

返回值类型为 str

| 取值      | 含义                             |
| --------- | -------------------------------- |
| "Success" | 函数执行成功                     |
| "Cancel"  | 后端调用的窗体取消了模板文件选择 |

#### backEndPushTemplateFileDataToFrontEnd

##### 参数

无

##### 返回值

返回值类型为list，是一个给前端渲染的列表

#### backEndUpdateTemplateFileData

##### 参数

| 名称           | 类型 | 含义                     |
| -------------- | ---- | ------------------------ |
| TemplateFileId | str  | 所对应的模板文件的id     |
| Data           | dict | 对应的所要渲染的案件信息 |

##### 返回值

返回值类型为 str

| 取值      | 含义         |
| --------- | ------------ |
| "Success" | 函数执行成功 |
| "Fail"    | 函数执行失败 |

#### backEndDeleteTemplateFileData

##### 参数

| 名称           | 类型 | 含义                 |
| -------------- | ---- | -------------------- |
| TemplateFileId | str  | 所对应的模板文件的id |

##### 返回值

返回值类型为 str

| 取值      | 含义                       |
| --------- | -------------------------- |
| "Success" | 后端对应的模板文件删除成功 |
| "Fail"    | 后端对应的模板文件删除失败 |

#### backEndOutputTemplateFileData

##### 参数

无

##### 返回值

返回值类型为 str

| 取值      | 含义                             |
| --------- | -------------------------------- |
| "Success" | 函数执行成功                     |
| "Cancel"  | 后端调用的窗体取消了模板文件选择 |

### TemplateFileEditForm

#### backEndChooseTemplateFile

##### 参数

无

##### 返回值

返回值类型为 Dict，各字段的详情如下：

| 字段名称         | 类型 | 含义                                                                                    |
| ---------------- | ---- | --------------------------------------------------------------------------------------- |
| res              | str  | 函数执行的结果，"Success"——函数执行成功"；Cancel"——后端调用的窗体取消了模板文件选择 |
| templateFileDir  | str  | 从后端调用的窗体中，所选择的模板文件的绝对路径                                          |
| templateFileName | str  | 从后端调用的窗体中，所选择的模板文件的文件名（已去除文件后缀名）                        |
