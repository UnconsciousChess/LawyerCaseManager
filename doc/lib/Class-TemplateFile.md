## TemplateFile

### 概述

    模板文件，每一个实例对应的是一个word文件（docx）

#### 对应源文件

    TemplateFile.py

#### 属性

| 属性名             | 含义                   | 数据类型 |
| ------------------ | ---------------------- | -------- |
| _TemplateFileId    | 模板文件的id           | str      |
| _TemplateFileName  | 模板文件的文件名       | str      |
| _TemplateFileDir   | 模板文件的绝对路径     | str      |
| _TemplateFileType  | 模板文件的渲染类型     | str      |
| _TemplateFileStage | 模板文件对应的案件阶段 | str      |

#### 方法

##### Getter方法

| 方法名           | 参数 | 返回值数据类型       | 作用             |
| ---------------- | ---- | -------------------- | ---------------- |
| **Get** + 属性名 | N/A  | 对应属性 的 数据类型 | 外部访问实例属性 |

##### Setter方法

###### SetTemplateFileId

| 方法名            | 返回值数据类型 | 作用                 |
| ----------------- | -------------- | -------------------- |
| SetTemplateFileId | int            | 改变当前模板文件的id |

**参数**

1 TemplateFileId

* 类型：str
* 含义：传入的模板文件的id
* 默认值：n/a
* 

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false

**返回值**

| 值  | 含义         |
| --- | ------------ |
| 0   | 正常运行完毕 |
| -1  | 运行出错     |

###### SetTemplateFileName

| 方法名              | 返回值数据类型 | 作用                 |
| ------------------- | -------------- | -------------------- |
| SetTemplateFileName | int            | 改变模板文件的文件名 |

**参数**

1 TemplateFileName

* 类型：str
* 含义：传入模板文件的文件名
* 默认值：n/a
* 

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false

**返回值**

| 值  | 含义         |
| --- | ------------ |
| 0   | 正常运行完毕 |
| -1  | 运行出错     |

###### SetTemplateFileDir

| 方法名             | 返回值数据类型 | 作用                       |
| ------------------ | -------------- | -------------------------- |
| SetTemplateFileDir | int            | 改变当前模板文件的绝对路径 |

**参数**

1 TemplateFileDir

* 类型：str
* 含义：传入的模板文件的绝对路径
* 默认值：n/a
* 

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false

**返回值**

| 值  | 含义         |
| --- | ------------ |
| 0   | 正常运行完毕 |
| -1  | 运行出错     |

###### SetTemplateFileType

| 方法名              | 返回值数据类型 | 作用                       |
| ------------------- | -------------- | -------------------------- |
| SetTemplateFileType | int            | 改变当前模板文件的渲染类型 |

**参数**

1 TemplateFileType

* 类型：str
* 含义：传入的模板文件的渲染类型
* 默认值：n/a
* 取值范围："directCopy" or "docxtpl"

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false

**返回值**

| 值  | 含义         |
| --- | ------------ |
| 0   | 正常运行完毕 |
| -1  | 运行出错     |

###### SetTemplateFileStage

| 方法名               | 返回值数据类型 | 作用                           |
| -------------------- | -------------- | ------------------------------ |
| SetTemplateFileStage | int            | 改变当前模板文件对应的案件阶段 |

**参数**

1 TemplateFileStage

* 类型：str
* 含义：当前模板文件对应的案件阶段
* 默认值：n/a
* 取值范围：'委托' or '立案' or '审理' or '执行' or '归档'

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false

**返回值**

| 值  | 含义         |
| --- | ------------ |
| 0   | 正常运行完毕 |
| -1  | 运行出错     |

##### 进一步封装的Setter方法

###### SetTemplateFileFromString

| 方法名                    | 返回值数据类型 | 作用                                     |
| ------------------------- | -------------- | ---------------------------------------- |
| SetTemplateFileFromString | str            | 从一个特定格式的字符串中读取模板文件信息 |

**参数**
1 InputString

* 类型：str
* 含义：包含模板文件信息的，符合特定格式的字符串
* 默认值：n/a
* 格式：

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false
* 

**返回值**

| 值      | 含义         |
| ------- | ------------ |
| Success | 正常运行完毕 |
| Error   | 运行出错     |

###### SetTemplateFileFromDict

| 方法名                  | 返回值数据类型 | 作用                                   |
| ----------------------- | -------------- | -------------------------------------- |
| SetTemplateFileFromDict | str            | 从一个特定格式的字典中读取模板文件信息 |

**参数**
1 InputDict

* 类型：dict
* 含义：包含模板文件信息的，符合特定格式的字典
* 默认值：n/a

2 Debug

* 类型：bool
* 含义：是否开启调试模式，true为开启，false为关闭
* 默认值：false
* 字典键名及要求：

| 序号 | 键名              | 类型 | 是否必须 |
| ---- | ----------------- | ---- | -------- |
| 1    | templateFileId    | str  | 是       |
| 2    | templateFileName  | str  | 是       |
| 3    | templateFileDir   | str  | 是       |
| 4    | templateFileType  | str  | 是       |
| 5    | templateFileStage | str  | 是       |

以上键值的含义与取值范围，和Setter方法各对应的参数完全相同
跟随前端要求，采用lower camel case命名法

**返回值**

| 值      | 含义         |
| ------- | ------------ |
| Success | 正常运行完毕 |
| Error   | 运行出错     |

##### Output方法

###### OutputTemplateFileToString

| 方法名                   | 返回值数据类型 | 作用                                             |
| ------------------------ | -------------- | ------------------------------------------------ |
| OutputTemplateFileToDict | str            | 将当前模板文件信息输出成一个符合特定格式的字符串 |

无参数。

返回值的具体格式为：

> **templateFileStage|templateFileDir@templateFileType**

###### OutputTemplateFileToDict

| 方法名                   | 返回值数据类型 | 作用                             |
| ------------------------ | -------------- | -------------------------------- |
| OutputTemplateFileToDict | dict           | 将当前模板文件信息输出成一个字典 |

无参数。

返回字段名称跟随前端要求，按照lower camel case命名法

返回值各字段的详情如下：

| 序号 | 键名              | 类型 |
| ---- | ----------------- | ---- |
| 1    | templateFileId    | str  |
| 2    | templateFileName  | str  |
| 3    | templateFileDir   | str  |
| 4    | templateFileType  | str  |
| 5    | templateFileStage | str  |

以上键值的含义与取值范围，和Setter方法各对应的参数完全相同
