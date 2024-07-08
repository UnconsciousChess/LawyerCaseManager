<template>
    <el-table :data="tableData" style="width: 100%" empty-text="目前暂无案件" :expand-row-keys="expandRowKeys"
        :row-key="row => row.caseId" @expand-change="(row, expandedRows) => generateShowText(row, expandedRows)">
        <el-table-column label="" width="40" type="expand">
            <template #default>
                <CaseInfoShowDescription :propShowTextList="showTextList" :propId="caseId" />
            </template>
        </el-table-column>
        <el-table-column prop="index" label="序号" width="55" />
        <el-table-column prop="causeOfAction" label="案由" width="180" />
        <!-- <el-table-column prop="caseCourtCode" label="案号" width="200" /> -->
        <el-table-column prop="litigantsName" label="当事人" width="350" />
        <el-table-column fixed="right" label="操作" width="400">
            <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEditData(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDeleteData(row)">删除</el-button>
                <el-button type="success" size="small" @click="handleOutputData(row)">导出</el-button>
                <el-button color="#626aef" size="small" disabled>上传</el-button>
                <el-button type="warning" size="small" plain @click="handleDocumentsGenerate(row)">文书生成</el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-divider></el-divider>
    <!-- 刷新按钮 -->
    <div>
        <el-button color="#9EC1DD" @click="createNewCase">新建案件</el-button>
        <el-button color="#B5BEF2" @click="getTableData">刷新数据</el-button>
        <el-button color="#CEECAB" @click="handleBulkLoadingData">批量加载案件</el-button>
        <el-button color="#FDC3D6" @click="handleBulkOutputData">批量导出案件</el-button>
    </div>
    <el-divider></el-divider>
    <!-- 测试按钮 -->
     <div>
        <el-button type="primary" @click="testOutputCase">后端输出案件信息</el-button>
     </div>


    <!-- 下面是按下按钮以后弹出的对话框 -->

    <!-- 编辑对话框 -->
    <el-dialog title="编辑案件信息" width="700" align-center v-model="dialogEditDataVisible">
        <CaseInfoForm :propCaseData="currentEditRow" :propMode="caseInfoFormMode" @updateCaseData="updateCaseDataFromCaseInfoForm" />
    </el-dialog>

    <!-- 删除对话框 -->
    <el-dialog title="注意" v-model="dialogDeleteDataVisible" width="400" align-center>
        <span>确认删除当前案件吗？</span>
        <template #footer>
            <div>
                <el-button @click="dialogDeleteDataVisible = false">取消</el-button>
                <el-button type="danger" @click="deleteData(currentDeleteRow)">确定</el-button>
            </div>
        </template>
    </el-dialog>

    <!-- 输出对话框 -->
    <el-dialog v-model="dialogOutputDataVisible" title="选择输出格式" width="500" align-center>
        <el-button type="primary" @click="outputToExcel(currentOutputRow)">输出当前案件信息为Excel文件</el-button>
        <el-button type="success" @click="outputToTxt(currentOutputRow)">输出当前案件信息为Txt文件</el-button>
    </el-dialog>

    <!-- 上传功能对话框（待开发）-->

</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";

import CaseInfoShowDescription from "./CaseInfoShowDescription.vue";
import CaseInfoForm from "./CaseInfoForm.vue";


// 初始化tableData，为空数组，是案件表格的数据
const tableData = ref([]);


const showTextList = ref([]);

// 这个变量是用于传递给子组件的caseId
const caseId = ref(null);
//一开始展开的行的数量为0
const currentExpandedRow = ref(0);

// 这个列表是存放展开的行的caseId（即rowkey
const expandRowKeys = ref([]);

// 以下变量是用于控制输出对话框的显示的布尔值
const dialogOutputDataVisible = ref(false);
const dialogDeleteDataVisible = ref(false);
const dialogEditDataVisible = ref(false);


const currentEditRow = ref(null);
const currentDeleteRow = ref(null);
const currentOutputRow = ref(null);
const caseInfoFormMode = ref(null);

// 测试数据
const testCase1 = {
    index: 1,
    title: "案件1",
    causeOfAction: "信息网络买卖合同纠纷",
    litigationAmount: "1000",
    courtName: "法院1",
    caseCourtCode: "（2024）粤0303民初12507号",
    mediationIntention: false,
    riskAgentUpfrontFee: "100",
    caseType: 1,
    riskAgentPostFeeRate: "1",
    caseAgentStage: ['1', '2'],
    riskAgentStatus: false,
    claimText: "诉讼请求1",
    factAndReason: "事实与理由1",
    rejectMediationReasonText: "拒绝调解理由1",
    agentFixedFee: "一审3000元，二审5000元，执行1000元，再审2000元",
    caseId: "1.1",
    litigantsName: "张三 诉 李四"
};
const testCase2 = {
    index: 2,
    title: "案件2",
    causeOfAction: "案由2",
    courtName: "法院2",
    litigationAmount: "2000",
    caseCourtCode: "案号2",
    mediationIntention: false,
    riskAgentUpfrontFee: "200",
    caseType: 2,
    riskAgentPostFeeRate: "2",
    caseAgentStage: ['3', '4'],
    riskAgentStatus: true,
    claimText: "诉讼请求2",
    factAndReason: "事实与理由2",
    rejectMediationReasonText: "拒绝调解理由2",
    agentFixedFee: "",
    caseId: "2.3",
    litigantsName: "王五 诉 赵六"
};
const testCase3 = {
    index: 3,
    title: "案件3",
    causeOfAction: "案由3",
    courtName: "法院3",
    litigationAmount: "3000",
    caseCourtCode: "案号3",
    mediationIntention: true,
    riskAgentUpfrontFee: "300",
    caseType: 3,
    riskAgentPostFeeRate: "3",
    caseAgentStage: ['1', '2', '3', '4', '5'],
    riskAgentStatus: false,
    claimText: "诉讼请求3",
    factAndReason: "事实与理由3",
    rejectMediationReasonText: "拒绝调解理由3",
    agentFixedFee: "一审3000元，二审5000元，执行1000元，再审1000元",
    caseId: "3.4",
    litigantsName: "赵六 诉 王五",
};



// 工厂函数，传入tableData的数据，返回可以直接输出的showText
function showTextCreator(tableData) {
    // 要返回的对象o
    var o = new Object();
    // 下面是直接复制的字段
    o.title = tableData.title;
    o.causeOfAction = tableData.causeOfAction;
    o.litigationAmount = tableData.litigationAmount;
    o.courtName = tableData.courtName;
    o.caseCourtCode = tableData.caseCourtCode;
    o.riskAgentUpfrontFee = tableData.riskAgentUpfrontFee;
    o.riskAgentPostFeeRate = tableData.riskAgentPostFeeRate;
    o.claimText = tableData.claimText;
    o.factAndReason = tableData.factAndReason;
    o.rejectMediationReasonText = tableData.rejectMediationReasonText;
    o.agentFixedFee = tableData.agentFixedFee;
    o.caseId = tableData.caseId;

    // 下面是需要转换的字段

    // 转换调解意向为√或×
    if (tableData.mediationIntention == true) {
        o.mediationIntention = "同意调解";
    } else {
        o.mediationIntention = "拒绝调解";
    }

    // 转换风险代理人状态为√或×
    if (tableData.riskAgentStatus == true) {
        o.riskAgentStatus = "是";
    } else {
        o.riskAgentStatus = "否";
    }

    // 转换案件类型为文字
    if (tableData.caseType == 1) {
        o.caseType = "民事案件";
    } else if (tableData.caseType == 2) {
        o.caseType = "行政案件";
    } else if (tableData.caseType == 3) {
        o.caseType = "执行案件";
    }

    if (tableData.caseAgentStage.length == 0) {
        o.caseAgentStage = "无";
    } else {
        o.caseAgentStage = "";
        // 遍历数组并转换为字符串
        tableData.caseAgentStage.forEach(stage => {
            if (stage == '1') {
                o.caseAgentStage += "一审立案阶段" + "、";
            }
            else if (stage == '2') {
                o.caseAgentStage += "一审诉讼阶段" + "、";
            }
            else if (stage == '3') {
                o.caseAgentStage += "二审阶段" + "、";
            }
            else if (stage == '4') {
                o.caseAgentStage += "执行阶段" + "、";
            }
            else if (stage == '5') {
                o.caseAgentStage += "再审阶段" + "、";
            }
        })
        // 如果最后一个字符是顿号，则去掉最后一个字符
        if (o.caseAgentStage.charAt(o.caseAgentStage.length - 1) == "、") {
            o.caseAgentStage = o.caseAgentStage.substring(0, o.caseAgentStage.length - 1);
        }
    }

    return o;
}

function generateShowText(row, expandedRows) {
    // 获取当前展开的行的数量，与currentExpandedRow进行比较
    if (expandedRows.length > currentExpandedRow.value) {
        // 如果expandedRows的长度大于currentExpandedRow
        // 则将currentExpandedRow更新为当前展开的行的数量,同时认为目前是点选了一下展开的状态
        currentExpandedRow.value = expandedRows.length;
        // 利用row的数据，运用showTextCreator工厂函数生成showText
        var showText = showTextCreator(row)
        // 将当前行的数据推向showTextList
        showTextList.value.push(showText);
        // 要prop给子组件的caseId为当前行对象的caseId
        caseId.value = row.caseId;

        // 将当前行的caseId推向expandRowKeys
        expandRowKeys.value.push(row.caseId);
        // console.log(expandRowKeys.value)
        // console.log("展开，当前展开行数量为" + currentExpandedRow.value);

    } else {
        // 如果expandedRows的长度小于currentExpandedRow
        // 则将currentExpandedRow更新为当前展开的行的数量,同时认为目前是点选了一下收起的状态
        currentExpandedRow.value = expandedRows.length;

        // 从expandRowKeys中删除对应的caseId
        expandRowKeys.value.splice(expandRowKeys.value.findIndex((item) => item === row.caseId), 1);

        // 从showTextList中删除对应的数据
        showTextList.value.splice(showTextList.value.findIndex((item) => item.caseid === row.caseid), 1);

        // console.log("收起，当前展开行数量为" + currentExpandedRow.value);
    }

}

// 创建新案件
function createNewCase() {
    dialogEditDataVisible.value = true;
    // 改变caseInfoFormMode为create（有edit和create两种模式）
    caseInfoFormMode.value = "create";
    // 将案件对象设为null，因为不需要传递现有案件对象到caseInfo之中
    currentEditRow.value = null;
}

// 从后端获取数据
function getTableData() {
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("getTableData()：未连接后端，目前只测试前端");
        // 当tableData为空时，添加测试数据
        if (tableData.value.length == 0) {
            tableData.value.push(testCase1);
            tableData.value.push(testCase2);
            tableData.value.push(testCase3);
        }
    }
    // 如果连接了后端，则从后端获取数据(实际工作流程)
    else {
        pywebview.api.outputAllCaseInfoToFrontEnd().then((cases) => {
            // 遍历cases，将数据根据一定的规则添加到tableData中
            for (let i = 0; i < cases.length; i++) {
                // 对比案件的id，如果相同则不添加
                if (
                    tableData.value.findIndex((item) => item.caseId === cases[i].caseId) !==
                    -1
                ) {
                    continue;
                }
                // 如果没有相同的，则将数据添加到tableData中
                tableData.value.push({
                    causeOfAction: cases[i].causeOfAction,
                    courtName: cases[i].courtName,
                    litigationAmount: cases[i].litigationAmount,
                    caseCourtCode: cases[i].caseCourtCode,
                    mediationIntention: cases[i].mediationIntention,
                    caseType: cases[i].caseType,
                    riskAgentStatus: cases[i].riskAgentStatus,
                    riskAgentUpfrontFee: cases[i].riskAgentUpfrontFee,
                    riskAgentPostFeeRate: cases[i].riskAgentPostFeeRate,
                    caseAgentStage: cases[i].caseAgentStage,
                    claimText: cases[i].claimText,
                    factAndReason: cases[i].factAndReason,
                    rejectMediationReasonText: cases[i].rejectMediationReasonText,
                    agentFixedFee: cases[i].agentFixedFee,
                    caseId: cases[i].caseId,
                    plaintiffs: cases[i].plaintiffs,
                    defendants: cases[i].defendants,
                    thirdParties: cases[i].thirdParties,
                    litigantsName : cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames ,
                    // 测试title的数据
                    title: cases[i].causeOfAction + "一案，编号：" + cases[i].caseId,

                });
                console.log(tableData.value)

            }

            // 对tableData的index进行重新排序
            for (let i = 0; i < tableData.value.length; i++) {
                tableData.value[i].index = i + 1;
            }
        });
    }

}

// 批量加载案件到后端,其中需要调用后端的函数
async function handleBulkLoadingData() {
    console.log("批量加载案件");
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("handleBulkLoadingData()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数
    else {
        let backendResult = await pywebview.api.inputAllCasesFromTxt();
        if (backendResult == "Success") {   // 如果后端返回成功，则刷新数据
            console.log("后端批量加载案件成功");
            getTableData();
        }
        else if (backendResult == "Fail") {
            console.log("后端批量加载案件失败");
        }

    }
}

// 批量导出案件
async function handleBulkOutputData() {
    console.log("批量导出案件");
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("handleBulkOutputData()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数outputAllCasesInfoToTxt
    else {
        pywebview.api.outputAllCasesInfoToTxt();
    }
}


// 编辑数据的前置函数
function handleEditData(val) {
    console.log("当前要编辑的案件id为" + val.caseId);
    dialogEditDataVisible.value = true;
    // 将当前要编辑的案件的对象传递给currentEditRow，便于接下来的组件调用
    currentEditRow.value = val;
    // 改变caseInfoFormMode为edit（有edit和create两种模式）
    caseInfoFormMode.value = "edit";
}

// 收到编辑数据以后，父组件中的数据进行更新
async function updateCaseDataFromCaseInfoForm(data) {
    console.log("更新案件信息");
    console.log(data);
    // 将对话框隐藏
    dialogEditDataVisible.value = false;
    // 前端的父组件更新数据
    // 获取要更新的数据的index
    var updateItemIndex = tableData.value.findIndex(
        (item) => item.caseId === data.caseId
    );
    // 对应的tableData更新数据
    tableData.value[updateItemIndex].causeOfAction = data.causeOfAction;
    tableData.value[updateItemIndex].courtName = data.courtName;
    tableData.value[updateItemIndex].litigationAmount = data.litigationAmount;
    tableData.value[updateItemIndex].caseCourtCode = data.caseCourtCode;
    tableData.value[updateItemIndex].mediationIntention = data.mediationIntention;
    tableData.value[updateItemIndex].caseType = data.caseType;
    tableData.value[updateItemIndex].riskAgentStatus = data.riskAgentStatus;
    tableData.value[updateItemIndex].riskAgentUpfrontFee = data.riskAgentUpfrontFee;
    tableData.value[updateItemIndex].riskAgentPostFeeRate = data.riskAgentPostFeeRate;
    tableData.value[updateItemIndex].caseAgentStage = data.caseAgentStage;
    tableData.value[updateItemIndex].claimText = data.claimText;
    tableData.value[updateItemIndex].factAndReason = data.factAndReason;
    tableData.value[updateItemIndex].rejectMediationReasonText = data.rejectMediationReasonText;
    tableData.value[updateItemIndex].agentFixedFee = data.agentFixedFee;
    tableData.value[updateItemIndex].plaintiffs = data.plaintiffs;
    tableData.value[updateItemIndex].defendants = data.defendants;
    tableData.value[updateItemIndex].thirdParties = data.thirdParties;
    tableData.value[updateItemIndex].litigantsName = data.litigantsName;
    tableData.value[updateItemIndex].title = data.causeOfAction + "一案，编号：" + data.caseId;

    // 下面是将信息传递给后端的部分
    // // 如果未连接后端，则只测试前端
    // if (typeof pywebview === 'undefined') {
    //     console.log("updateCaseDataFromCaseInfoForm()：未连接后端，目前只测试前端");
    // }
    // // 将对应的id及其他数据，传递给后端(实际运行环境)
    // else {
    //     let result = await pywebview.api.backEndUpdateCaseData(data.caseId, data);
    //     console.log(result);
    // }
}


// 删除数据的前置函数，作用是打开对话框，提示是否删除，最终确认后调用下面的deleteData
function handleDeleteData(val) {
    // console.log("当前要输出的案件id为" + val.caseId);
    dialogDeleteDataVisible.value = true;
    // 将当前要删除的案件的对象传递给currentDeleteRow，便于接下来的组件调用
    currentDeleteRow.value = val;
    // console.log(currentDeleteRow.value);
}

// 具体删除数据的函数
function deleteData(val) {
    console.log("当前要删除的案件id为" + val.caseId);
    // 将对话框隐藏
    dialogDeleteDataVisible.value = false;

    // 获取要删除的数据的index
    var deleteItemIndex = tableData.value.findIndex(
        (item) => item.caseId === val.caseId
    );

    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("deleteData()：未连接后端，目前只测试前端");
    }
    // 将对应的id传递给后端(实际运行环境)
    else {
        pywebview.api.backEndDeleteCase(val.caseId);
    }

    // 删除tableData中对应数组index的数据
    tableData.value.splice(deleteItemIndex, 1);

    // 对应的expandRowKeys也要删除
    expandRowKeys.value.splice(expandRowKeys.value.findIndex((item) => item === val.caseId), 1);

    // 对应的showTextList也要删除
    showTextList.value.splice(showTextList.value.findIndex((item) => item.caseId === val.caseId), 1);

    // 对应展开的行数减一
    currentExpandedRow.value -= 1;

    // 对tableData的index进行重新排序
    for (let i = 0; i < tableData.value.length; i++) {
        tableData.value[i].index = i + 1;
    }
}


// 输出数据的前置函数，作用是打开对话框，随后，再根据在对话框中的选择调用下面的outputToExcel或outputToTxt
function handleOutputData(val) {
    // console.log("当前要输出的案件id为" + val.caseId);
    dialogOutputDataVisible.value = true;
    // 将当前要输出的案件的对象传递给currentOutputRow，便于接下来的组件调用
    currentOutputRow.value = val;
}
// 输出数据到excel
function outputToExcel(val) {
    // 将对话框隐藏
    dialogOutputDataVisible.value = false;
    console.log("输出案件信息到excel");
    console.log(val.caseId)
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("outputToExcel()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数(实际运行环境)
    else {
        pywebview.api.outputCaseInfoToExcel(val.caseId);
    }
}

// 输出数据到txt
function outputToTxt(val) {
    // 将对话框隐藏
    dialogOutputDataVisible.value = false;
    // console.log("输出案件信息到txt");
    // console.log(val.caseId)
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("outputToTxt()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数(实际运行环境)
    else {
        pywebview.api.outputCaseInfoToTxt(val.caseId);
    }
}


// 生成文书
async function handleDocumentsGenerate(val) {
    console.log("文书生成");
    console.log("当前要生成文书的案件id为" + val.caseId)
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("handleDocumentGenerate()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数,将当前案件id传到后端(实际运行环境)
    else {
         let result = await pywebview.api.documentsGenerate(val.caseId);
         if (result == 0) {
             console.log("文书生成成功");
         }
    }
}


// 测试的代码
function testOutputCase(){
    if (typeof pywebview === 'undefined') {
        console.log("testOutputCase()：未连接后端，目前只测试前端");
    }
    else{
        console.log("测试函数，后端输出案件信息");
        pywebview.api.testCasesOutput();
    }
}



// 加载页面时先调用一次getTableData()获取数据
onMounted(() => {
    getTableData();
});
</script>