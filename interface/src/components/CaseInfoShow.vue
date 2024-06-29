<template>
    <el-table :data="tableData" stripe style="width: 100%" empty-text="目前暂无案件" :expand-row-keys="expandRowKeys"
        :row-key="row => row.caseId" @expand-change="(row, expandedRows) => generateShowText(row, expandedRows)">
        <el-table-column label="" width="40" type="expand">
            <template #default>
                <CaseInfoShowDescription :propShowTextList="showTextList" :propId="caseId" />
            </template>
        </el-table-column>
        <el-table-column prop="index" label="序号" width="80" />
        <el-table-column prop="causeOfAction" label="案由" width="250" />
        <el-table-column prop="caseCourtCode" label="案号" width="250" />
        <el-table-column fixed="right" label="操作" width="300">
            <template #default="{ row }">
                <el-button type="primary" size="small">编辑</el-button>
                <el-button type="danger" size="small" @click="handledeleteData(row)">删除</el-button>
                <el-button type="success" size="small" @click="handleOutputData(row)">输出</el-button>
                <el-button color="#626aef" size="small" disabled>上传</el-button>
            </template>
        </el-table-column>
    </el-table>

    <!-- 刷新按钮 -->
    <div>
        <el-button type="primary" @click="getTableData">刷新</el-button>
    </div>


    <!-- 删除确认对话框 -->
    <el-dialog title="注意" v-model="dialogDeleteDataVisible" width="400" align-center>
        <span>确认删除当前案件吗？</span>
        <template #footer>
            <div>
                <el-button @click="dialogDeleteDataVisible = false">取 消</el-button>
                <el-button type="danger" @click="deleteData(currentDeleteRow)">确 定</el-button>
            </div>
        </template>
    </el-dialog>
    <!-- 输出对话框 -->
    <el-dialog v-model="dialogOutputDataVisible" title="选择输出格式" width="500" align-center>
        <el-button type="primary" @click="row => outputToExcel(currentOutputRow)">输出当前案件信息为Excel文件</el-button>
        <el-button type="success" @click="row => outputToTxt(currentOutputRow)">输出当前案件信息为Txt文件</el-button>
    </el-dialog>

</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";

import CaseInfoShowDescription from "./CaseInfoShowDescription.vue";


// 初始化tableData，为空数组，是案件表格的数据
const tableData = ref([]);


const showTextList = ref([]);

// 这个变量是用于传递给子组件的caseId
const caseId = ref(null);
//一开始展开的行的数量为0
const currentExpandedRow = ref(0);

// 这个列表是存放展开的行的caseId（即rowkey
const expandRowKeys = ref([]);

// 以下变量是用于控制输出对话框的显示
const dialogOutputDataVisible = ref(false);
const dialogDeleteDataVisible = ref(false);

const currentDeleteRow = ref(null);
const currentOutputRow = ref(null);

// 测试数据
const testCase1 = {
    index: 1,
    title: "案件1",
    causeOfAction: "案由1",
    litigationAmount: "1000",
    courtName: "法院1",
    caseCourtCode: "案号1",
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
    caseId: "1.1"
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
    caseId: "2.3"
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
    caseId: "3.4"
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
        pywebview.api.OutputAllCaseInfoToFrontEnd().then((cases) => {
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

                    // 测试title的数据
                    title: cases[i].causeOfAction + "一案，编号：" + cases[i].caseId,

                });
                // console.log(tableData.value)

            }

            // 对tableData的index进行重新排序
            for (let i = 0; i < tableData.value.length; i++) {
                tableData.value[i].index = i + 1;
            }
        });
    }

}

// 删除数据
function deleteData(val) {
    console.log("当前要删除的案件id为" + val.caseId);
    // 将对话框隐藏
    dialogDeleteDataVisible.value = false;

    // 获取要删除的数据的index
    var deleteItemIndex = tableData.value.findIndex(
        (item) => item.caseId === val.caseId
    );

    // 将对应的id传递给后端
    try {
        pywebview.api.BackEndDeleteCase(val.caseId);
    } catch (e) {
        console.log("未连接后端，目前只测试前端");
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

function handledeleteData(val) {
    // console.log("当前要输出的案件id为" + val.caseId);
    dialogDeleteDataVisible.value = true;
    // 将当前要删除的案件的对象传递给currentDeleteRow，便于接下来的组件调用
    currentDeleteRow.value = val;
    // console.log(currentDeleteRow.value);
}

function handleOutputData(val) {
    // console.log("当前要输出的案件id为" + val.caseId);
    dialogOutputDataVisible.value = true;
    // 将当前要输出的案件的对象传递给currentOutputRow，便于接下来的组件调用
    currentOutputRow.value = val;
}


function outputToExcel(val) {
    // 将对话框隐藏
    dialogOutputDataVisible.value = false;
    console.log("输出案件信息到excel");
    console.log(val.caseId)
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("outputToExcel()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数
    else {
        pywebview.api.OutputCaseInfoToExcel(val.caseId);
    }
}


function outputToTxt(val) {
    // 将对话框隐藏
    dialogOutputDataVisible.value = false;
    console.log("输出案件信息到txt");
    console.log(val.caseId)
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("outputToTxt()：未连接后端，目前只测试前端");
    }
    // 如果连接了后端，则调用后端的函数
    else {
        pywebview.api.OutputCaseInfoToTxt(val.caseId);
    }
}


// 加载页面时先调用一次getTableData()获取数据
onMounted(() => {
    getTableData();
});
</script>
