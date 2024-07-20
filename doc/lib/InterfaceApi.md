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
- MergeFilesTable
  - backEndGetCaseFolderFiles
  - backEndMergeFiles

## 详述

### 内部方法

### GetFilepath

#### 参数

| 名称     | 类型 | 含义                 |
| -------- | ---- | -------------------- |
| title    | str  | 弹出窗口的标题       |
| filetype | str  | 窗口接受的文件的类型 |

filetype是一个以英文逗号分隔的字符串，每个部分包括一组符合以下规则的字符串，代表弹出窗口接的文件类型

| 参数  | 含义      |
| ----- | --------- |
| Text  | txt文件   |
| Word  | docx文件  |
| Excel | Excel文件 |
| All   | 所有文件  |

#### 返回值

返回值类型为 str，是在弹出窗口中所选择的文件的绝对路径

#### 示例

假设弹出窗口的标题为“这是标题”，拟接受的文件为docx和Excel文件

```python
GetFilePath(title="这是标题",fileType="Word,Excel")
```


### GetFolderpath

#### 参数

| 名称  | 类型 | 含义           |
| ----- | ---- | -------------- |
| title | str  | 弹出窗口的标题 |

#### 返回值

返回值类型为 str，是在弹出窗口中所选择的文件夹的绝对路径

---

### 与CaseInfoForm交互

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

### 与CaseInfoEditForm交互

#### inputLitigantFromTxt

##### 参数

| 名称         | 类型 | 含义                                                  |
| ------------ | ---- | ----------------------------------------------------- |
| TxtPath      | str  | 诉讼参与人txt文档的对应绝对路径                       |
| LitigantType | str  | 诉讼参与人的类型，原告为"plaintiff";被告为"defendant" |

##### 返回值

返回值类型为 dict, 是一个符合前端读入接口（接口字段格式详见前端的对应文档）的字典

### 与TemplateFileForm交互

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

### 与TemplateFileEditForm交互

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

### 与MergeFilesTable交互

#### backEndGetCaseFolderFiles

##### 参数

| 名称   | 类型 |
| ------ | ---- |
| CaseId | str  |

##### 返回值

返回值类型为 str或list，如果函数执行成功，则返回list，失败则返回str

list：

该列表中的每一个元素都包括一个字典，对应一个文件对象
每个字典都有两个键，具体为

| 键名 | 含义             |
| ---- | ---------------- |
| name | 文件名称         |
| path | 该文件的绝对路径 |

str：

| 取值             | 含义                         |
| ---------------- | ---------------------------- |
| "CaseIdNotExist" | 读入的案件id无法在后端搜索到 |

#### backEndMergeFiles

##### 参数

| 名称          | 类型 | 含义                                     |
| ------------- | ---- | ---------------------------------------- |
| CaseId        | str  | 当前要进行处理案件的案件id               |
| SelectedFiles | list | 在前端所选中要合并的文件的绝对路径的列表 |

##### 返回值

返回值类型为 str

| 取值             | 含义                         |
| ---------------- | ---------------------------- |
| "Success"        | 函数执行成功                 |
| "CaseIdNotExist" | 读入的案件id无法在后端搜索到 |
