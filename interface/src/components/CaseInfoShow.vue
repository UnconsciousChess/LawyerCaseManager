<template>
	<el-table :data="tableData" stripe style="width: 100%">
		<el-table-column prop="index" width="40" type="expand">
			<template #default>
				<CaseInfoShowTable />
			</template>
		</el-table-column>
		<el-table-column prop="index" label="序号" width="80" />
		<el-table-column prop="causeOfAction" label="案由" width="250" />
		<el-table-column prop="caseCourtCode" label="案号" width="250" />
		<el-table-column fixed="right" label="操作" width="300">
			<template #default="{row}">
				<el-button type="primary" size="small">查看</el-button>
				<el-button type="danger" size="small" @click="deleteData(row)"
					>删除</el-button
				>
				<el-button type="success" size="small">输出</el-button>
				<el-button type="info" size="small">上传</el-button>
			</template>
		</el-table-column>
	</el-table>

	<el-button type="primary" @click="getTableData">刷新</el-button>
</template>

<script setup>
import {ref, onMounted} from "vue";

import CaseInfoShowTable from "./CaseInfoShowTable.vue";

// 初始化tableData，为空数组，其内部格式为
// {
//     index: 1,
//     causeOfAction: "案由",
//     caseCourtCode: "案号",
//     id : 时间戳
// }
const tableData = ref([]);

// 测试版本，模拟数据
// const tableData = ref([
//     {
//         index: 1,
//         causeOfAction: "案由1",
//         caseCourtCode: "案号1",
//         id: 1.1
//     },
//     {
//         index: 2,
//         causeOfAction: "案由2",
//         caseCourtCode: "案号2",
//         id: 2.3
//     },
//     {
//         index: 3,
//         causeOfAction: "案由3",
//         caseCourtCode: "案号3",
//         id: 3.4
//     }
// ]);

// 从后端获取数据
function getTableData() {
    // 从前端获取数据
	pywebview.api.OutputAllCaseInfoToFrontEnd().then((cases) => {
		// 遍历cases，将数据根据一定的规则添加到tableData中
		for (let i = 0; i < cases.length; i++) {
            // 对比案件的id，如果相同则不添加
            if (tableData.value.findIndex((item) => item.caseId === cases[i].caseId) !== -1) {
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
	// 删除tableData中的数据
	var deleteItemIndex = tableData.value.findIndex(
		(item) => item.caseId === val.caseId
	);
	tableData.value.splice(deleteItemIndex, 1);

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
