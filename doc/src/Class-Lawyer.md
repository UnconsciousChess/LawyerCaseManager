## Lawyer

### 概述

 每一个实例对应的，是一位《**律师法**》第二条所规定的，提供法律服务的执业人员。

#### 对应源文件

    LitigantClass.py

#### 导入代码

```python
from library.LitigantClass import Lawyer
```

#### 属性

| 属性名          | 含义                     | 数据类型 |
| --------------- | ------------------------ | -------- |
| _Name           | 律师的姓名               | str      |
| _IdCode         | 律师的身份证号码         | str      |
| _Location       | 律师的地址               | str      |
| _ContactNumber  | 律师的联系电话           | str      |
| _LawyerLicense  | 律师执业证号码           | str      |
| _DeligationFile | 律师证明文件上传路径列表 | list     |
| _InternLawyer   | 该律师是否为实习律师     | bool     |

#### 方法

##### Getter方法

###### 简单的Getter方法

| 方法名                                     | 参数 | 返回值数据类型       | 作用             |
| ------------------------------------------ | ---- | -------------------- | ---------------- |
| **Get** + 属性名（InternLawyer除外） | N/A  | 对应属性 的 数据类型 | 外部访问实例属性 |
| IsInternLawyer                             | N/A  | 对应属性 的 数据类型 | 外部访问实例属性 |

---

##### Setter方法

###### SetName

| 方法名  | 返回值数据类型 | 作用             |
| ------- | -------------- | ---------------- |
| SetName | None           | 改变当前律师名称 |

参数

1 Name

* 类型：str
* 含义：传入的律师姓名
* 默认值：n/a

###### SetIdCode

| 方法名    | 返回值数据类型 | 作用                     |
| --------- | -------------- | ------------------------ |
| SetIdCode | None           | 改变当前律师的身份证号码 |

参数

1 IdCode

* 类型：str
* 含义：传入的律师身份证号码
* 默认值：n/a

###### SetLocation

| 方法名      | 返回值数据类型 | 作用                   |
| ----------- | -------------- | ---------------------- |
| SetLocation | None           | 改变当前律师的地址信息 |

参数

1 Location

* 类型：str
* 含义：传入的律师的地址信息
* 默认值：n/a

###### SetContactNumber

| 方法名           | 返回值数据类型 | 作用                   |
| ---------------- | -------------- | ---------------------- |
| SetContactNumber | None           | 改变当前律师的联系电话 |

参数

1 ContactNumber

* 类型：str
* 含义：传入的律师的联系电话
* 默认值：n/a

###### SetLawyerLicense

| 方法名           | 返回值数据类型 | 作用                     |
| ---------------- | -------------- | ------------------------ |
| SetLawyerLicense | None           | 改变当前律师的执业证号码 |

参数

1 LawyerLicense

* 类型：str
* 含义：传入的律师的执业证号码
* 默认值：n/a

###### SetDeligationFiles

| 方法名             | 返回值数据类型 | 作用                               |
| ------------------ | -------------- | ---------------------------------- |
| SetDeligationFiles | None           | 改变当前律师的执业文件所在路径信息 |

参数

1 DeligationFiles

* 类型：list
* 含义：传入的律师的执业文件所在路径信息
* 默认值：n/a

###### SetInternLawyer

| 方法名          | 返回值数据类型 | 作用                             |
| --------------- | -------------- | -------------------------------- |
| SetInternLawyer | None           | 改变当前律师是否为实习律师的状态 |

参数

1 TrueOrFalse

* 类型：bool
* 含义：决定当前律师是否为实习律师，True为实习律师，False为正式执业律师
* 默认值：n/a

---

##### Input方法

###### InputLawyerInfoFromTxt

| 方法名                 | 返回值数据类型 | 作用                                  |
| ---------------------- | -------------- | ------------------------------------- |
| InputLawyerInfoFromTxt | str            | 从一个txt文件中读入一个律师的所有信息 |

参数

1 InfoFile

* 类型：str
* 含义：传入的txt文件的路径
* 默认值：n/a

返回值

| 取值            | 含义                            |
| --------------- | ------------------------------- |
| "Success"       | 函数执行完毕，成功读入信息      |
| "PathNotExists" | 读入的路径不存在                |
| "NotFile"       | 读入的路径并非一个文件          |
| "NotTxtFile"    | 读入的文件后缀名并非一个txt文件 |

---

##### Output方法

###### OutputLawyerInfoToScreen

| 方法名                   | 返回值数据类型 | 作用                               |
| ------------------------ | -------------- | ---------------------------------- |
| OutputLawyerInfoToScreen | None           | 将当前律师信息在后端输出（测试用） |

无参数

###### OutputLawyerInfoToDict

| 方法名                 | 返回值数据类型 | 作用                         |
| ---------------------- | -------------- | ---------------------------- |
| OutputLawyerInfoToDict | dict           | 将当前律师信息输出成一个字典 |

无参数。

返回字段名称跟随前端要求，按照lower camel case命名法

返回值各字段的详情如下：

| 字段名称          | 类型 | 含义                   |
| ----------------- | ---- | ---------------------- |
| lawyerName        | str  | 当前律师名称           |
| lawyerIdNumber    | str  | 当前律师身份证号码     |
| lawyerAddress     | str  | 当前律师地址信息       |
| lawyerPhoneNumber | str  | 当前律师联系电话       |
| lawyerLicense     | str  | 当前律师执业证号码     |
| isInternLawyer    | bool | 当前律师是否为实习律师 |
