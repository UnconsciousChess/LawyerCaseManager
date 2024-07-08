## Case

### 概述

    案件，每一个实例对应的是现实中每一个单独的案子

#### 对应源文件

    CaseClass.py

#### 属性

| 属性名                     | 含义                   | 数据类型 |
| -------------------------- | ---------------------- | -------- |
| _CaseType                  | 案件类型               | int      |
| _LitigationAmount          | 诉讼标的额             | float    |
| _CaseOfAction              | 案由                   | str      |
| _JurisdictionDict          | 管辖法院（各诉讼阶段） | dict     |
| _UploadFilesList           | 上传文件列表           | list     |
| _ClaimText                 | 诉讼请求               | str      |
| _FactAndReasonText         | 事实和理由             | str      |
| _CaseFolderPath            | 案件文件夹绝对路径     | str      |
| _PlaintiffList             | 原告列表               | list     |
| _DefendantLis              | 被告列表               | list     |
| _LegalThirdPartyList       | 第三人列表             | list     |
| _MediationIntention        | 调解意愿               | bool     |
| _RejectMediationReasonText | 拒绝调解的理由         | str      |
| _CaseAgentStage            | 律师代理阶段           | list     |
| _RiskAgentStatus           | 是否采取风险收费的方式 | bool     |
| _RiskAgentUpfrontFee       | 风险收费前期费用       | float    |
| _RiskAgentPostFeeRate      | 风险收费后期提成比例   | float    |
| _AgentFixedFeeList         | 各阶段固定收费列表     | list     |
| _CaseCourtCode             | 案号                   | str      |
| _CaseId                    | 案件生成的id           | str      |

#### 方法

##### Getter方法

###### 简单的Getter方法

| 方法名                 | 参数 | 返回值数据类型       |
| ---------------------- | ---- | -------------------- |
| **Get** + 属性名 | N/A  | 对应属性 的 数据类型 |

###### 进阶的Getter方法

| 方法名                  | 参数 | 返回值数据类型 | 作用                                     |
| ----------------------- | ---- | -------------- | ---------------------------------------- |
| GetAllPlaintiffNames    | N/A  | str            | 以中文顿号间隔，返回所有原告的名称       |
| GetAllDefendantNames    | N/A  | str            | 以中文顿号间隔，返回所有被告的名称       |
| GetCaseAgentStageStr    | N/A  | str            | 以中文顿号间隔，返回所有代理阶段的名称   |
| GetOurClientListAndSide | N/A  | list，str      | 返回我方当事人的列表，以及代理的方向     |
| GetOurClientNames       | N/A  | str            | 以中文顿号间隔，返回所有我方当事人的名称 |
| GetCourtNameStr         | N/A  | str            |                                          |

##### Setter方法

## Litigant

### 概述

    诉讼参与人，每一个实例对应的是一个《民法典》第二条中规定的民事主体

#### 对应源文件

    LitigantClass.py

#### 属性

#### 方法

## Lawyer

### 概述

    律师，每一个实例对应的是一个诉讼代理人（自然人）

#### 对应源文件

    LitigantClass.py

#### 属性

#### 方法

## BankAccount

### 概述

    银行账户，每一个实例对应的是一个民事主体，在一家银行所开的一个账户

#### 对应源文件

    Property.py

#### 属性

#### 方法

## TemplateFile

### 概述

    模板文件，每一个实例对应的是一个word文件（docx）

#### 对应源文件

    TemplateFile.py

#### 属性

#### 方法
