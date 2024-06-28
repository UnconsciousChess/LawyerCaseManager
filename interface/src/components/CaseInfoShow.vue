<template>
    <el-table :data="tableData" stripe style="width: 100%" @expand-change="(row,expandedRows) => generateShowText(row,expandedRows)">
        <el-table-column label="" width="40" type="expand" >
            <template #default="{ row }">
                <CaseInfoShowTable :propShowTextList="showTextList" :propId="id"/>
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
import { ref, onMounted ,defineProps} from "vue";

import CaseInfoShowTable from "./CaseInfoShowTable.vue";




const showTextList = ref([]);
const id = ref(null);

//一开始展开的行的数量为0
const currentExpandedRow = ref(0);



// 初始化tableData，为空数组，其内部格式为
// {
//     index: 1,
//     causeOfAction: "案由",
//     caseCourtCode: "案号",
//     id : 时间戳
// }
// const tableData = ref([]);

function generateShowText(row,expandedRows){
    // 获取当前展开的行的数量，与currentExpandedRow进行比较
    if (expandedRows.length > currentExpandedRow.value){
        // 如果expandedRows的长度大于currentExpandedRow
        // 则将currentExpandedRow更新为当前展开的行的数量,同时认为目前是点选了一下展开的状态
        currentExpandedRow.value = expandedRows.length;
        // 将当前行的数据推向showTextList
        showTextList.value.push({
            title: row.title,
            causeOfAction: row.causeOfAction,
            litigationAmount: row.litigationAmount,
            courtName: row.courtName,
            caseCourtCode: row.caseCourtCode,
            riskAgentUpfrontFee: row.riskAgentUpfrontFee,
            riskAgentPostFeeRate: row.riskAgentPostFeeRate,
            claimText: row.claimText,
            factAndReason: row.factAndReason,
            rejectMediationReasonText: row.rejectMediationReasonText,
            id: row.id
        });

        // 要prop给子组件的id为当前行对象的id
        id.value = row.id;

        console.log(showTextList.value)

    }else{
        // 如果expandedRows的长度小于currentExpandedRow
        // 则将currentExpandedRow更新为当前展开的行的数量,同时认为目前是点选了一下收起的状态
        currentExpandedRow.value = expandedRows.length;
        // 从showTextList中删除对应的数据
        showTextList.value.splice(showTextList.value.findIndex((item) => item.id === row.id),1);
        console.log(showTextList.value);
    }

}

// 测试版本，模拟数据
const tableData = ref([
    {
        index: 1,
        title: "案件1",
        causeOfAction: "案由1",
        litigationAmount: "1000",
        courtName: "法院1",
        caseCourtCode: "案号1",
        mediationIntention: true,
        riskAgentUpfrontFee: "100",
        riskAgentPostFeeRate: "1",
        id: 1.1
    },
    {
        index: 2,
        title: "案件2",
        causeOfAction: "案由2",
        courtName: "法院2",
        litigationAmount: "2000",
        caseCourtCode: "案号2",
        mediationIntention: false,
        riskAgentUpfrontFee: "200",
        riskAgentPostFeeRate: "2",
        id: 2.3
    },
    {
        index: 3,
        title: "案件3",
        causeOfAction: "案由3",
        courtName: "法院3",
        litigationAmount: "3000",
        caseCourtCode: "案号3",
        mediationIntention: true,
        riskAgentUpfrontFee: "300",
        riskAgentPostFeeRate: "3",
        id: 3.4
    }
]);

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
                index: i + 1,
                causeOfAction: cases[i].causeOfAction,
                caseCourtCode: cases[i].caseCourtCode, //temp test
                caseId: cases[i].caseId,
            });
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

    // 对tableData的index进行重新排序
    for (let i = 0; i < tableData.value.length; i++) {
        tableData.value[i].index = i + 1;
    }
}

// 加载页面时获取数据
onMounted(() => {
    // getTableData();
});
</script>
