<template>
    <el-table :data="tableData" stripe style="width: 100%"
        @expand-change="(row, expandedRows) => generateShowText(row, expandedRows)">
        <el-table-column label="" width="40" type="expand">
            <template #default="{ row }">
                <CaseInfoShowTable :propShowTextList="showTextList" :propId="caseId" />
            </template>
        </el-table-column>
        <el-table-column prop="index" label="序号" width="80" />
        <el-table-column prop="causeOfAction" label="案由" width="250" />
        <el-table-column prop="caseCourtCode" label="案号" width="250" />
        <el-table-column fixed="right" label="操作" width="300">
            <template #default="{ row }">
                <el-button type="primary" size="small">查看</el-button>
                <el-button type="danger" size="small" @click="deleteData(row)">删除</el-button>
                <el-button type="success" size="small">输出</el-button>
                <el-button type="info" size="small">上传</el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-button type="primary" @click="getTableData">刷新</el-button>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";

import CaseInfoShowTable from "./CaseInfoShowTable.vue";




const showTextList = ref([]);
const caseId = ref(null);

//一开始展开的行的数量为0
const currentExpandedRow = ref(0);



// 初始化tableData，为空数组，其内部格式为
// {
//     index: 1,
//     causeOfAction: "案由",
//     caseCourtCode: "案号",
//     courtName: "法院",
//     litigationAmount: "诉讼金额",
//     mediationIntention: true,
//     riskAgentUpfrontFee: "前期风险收费金额",
//     riskAgentPostFeeRate: "后期风险收费比例",
//     caseType: 1,
//     caseAgentStage: ['1','2'],
//     claimText: "诉讼请求",
//     factAndReason: "事实与理由",
//     rejectMediationReasonText: "拒绝调解理由",
//     id : 时间戳
// }
// 测试时将下面这一行注释掉
const tableData = ref([]);

// 测试数据
// const tableData = ref([
//     {
//         index: 1,
//         title: "案件1",
//         causeOfAction: "案由1",
//         litigationAmount: "1000",
//         courtName: "法院1",
//         caseCourtCode: "案号1",
//         mediationIntention: true,
//         riskAgentUpfrontFee: "100",
//         caseType: 1,
//         riskAgentPostFeeRate: "1",
//         caseAgentStage: ['1','2'],
//         claimText: "诉讼请求1",
//         factAndReason: "事实与理由1",
//         rejectMediationReasonText: "拒绝调解理由1",
//         id: 1.1
//     },
//     {
//         index: 2,
//         title: "案件2",
//         causeOfAction: "案由2",
//         courtName: "法院2",
//         litigationAmount: "2000",
//         caseCourtCode: "案号2",
//         mediationIntention: false,
//         riskAgentUpfrontFee: "200",
//         caseType: 2,
//         riskAgentPostFeeRate: "2",
//         caseAgentStage: ['3','4'],
//         claimText: "诉讼请求2",
//         factAndReason: "事实与理由2",
//         rejectMediationReasonText: "拒绝调解理由2",
//         id: 2.3
//     },
//     {
//         index: 3,
//         title: "案件3",
//         causeOfAction: "案由3",
//         courtName: "法院3",
//         litigationAmount: "3000",
//         caseCourtCode: "案号3",
//         mediationIntention: true,
//         riskAgentUpfrontFee: "300",
//         caseType: 3,
//         riskAgentPostFeeRate: "3",
//         caseAgentStage: ['1','2','3','4','5'],
//         claimText: "诉讼请求3",
//         factAndReason: "事实与理由3",
//         rejectMediationReasonText: "拒绝调解理由3",
//         id: 3.4
//     }
// ]);

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
        o.riskAgentStatus = "√";
    } else {
        o.riskAgentStatus = "×";
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

        console.log(showTextList.value)
        console.log("展开，当前展开行数量为"+currentExpandedRow.value);

    } else {
        // 如果expandedRows的长度小于currentExpandedRow
        // 则将currentExpandedRow更新为当前展开的行的数量,同时认为目前是点选了一下收起的状态
        currentExpandedRow.value = expandedRows.length;
        // 从showTextList中删除对应的数据
        showTextList.value.splice(showTextList.value.findIndex((item) => item.id === row.id), 1);
        console.log(showTextList.value);
        console.log("收起，当前展开行数量为"+currentExpandedRow.value);
    }

}



// 从后端获取数据
function getTableData() {
    // 从前端获取数据
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

// 删除数据
function deleteData(val) {
    console.log("当前案件的id为" + val.caseId);

    // 获取要删除的数据的index
    var deleteItemIndex = tableData.value.findIndex(
        (item) => item.caseId === val.caseId
    );

    // 将对应的id传递给后端
    pywebview.api.BackEndDeleteCase(val.caseId);

    // 删除tableData中对应数组index的数据
    tableData.value.splice(deleteItemIndex, 1);

    // 对应的showTextList也要删除
    showTextList.value.splice(showTextList.value.findIndex((item) => item.id === val.id), 1);

    // 对应展开的行数减一
    currentExpandedRow.value -= 1;

    // 对tableData的index进行重新排序
    for (let i = 0; i < tableData.value.length; i++) {
        tableData.value[i].index = i + 1;
    }
}

// 加载页面时获取数据
onMounted(() => {
    getTableData();
});
</script>
