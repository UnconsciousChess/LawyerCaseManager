<template>
	<div style="height: 400px">
		<el-auto-resizer>
			<template #default="{width, height}">
				<el-table-v2
					:columns="columns"
					:data="data"
					:width="width"
					:height="height"
					fixed
				/>
			</template>
		</el-auto-resizer>
	</div>

	<!-- 表格外的功能按钮 -->
	<div style="margin-top: 20px">
		<el-button color="#9EC1DD" @click="createNewCase">新建案件</el-button>
		<el-button color="#B5BEF2" @click="loadData">刷新数据</el-button>
		<el-button color="#CEECAB" @click="handleBulkLoadingData"
			>批量加载案件</el-button
		>
		<el-button color="#FDC3D6" @click="handleBulkOutputData"
			>批量导出案件</el-button
		>
	</div>

	<!-- 测试按钮 -->
	<div style="margin-top: 20px">
		<el-button type="primary" @click="testOutputCase"
			>后端输出案件信息</el-button
		>
	</div>


	<!-- 编辑对话框 -->
	<el-dialog
		title="编辑案件信息"
		width="900"
		align-center
		v-model="dialogEditDataVisible"
		draggable
	>
		<el-scrollbar height="600px">
			<CaseInfoForm
				ref="caseInfoFormRef"
				:propCaseData="currentEditRow"
				:propMode="caseInfoFormMode"
				@updateCaseData="updateCaseDataFromCaseInfoForm"
			/>
		</el-scrollbar>
	</el-dialog>

</template>

<script setup lang="jsx">
import {onMounted} from "vue";
import {ref} from "vue";
// import {Column} from "element-plus";
import {
	ElButton,
	ElIcon,
	ElTag,
	ElTooltip,
	TableV2FixedDir,
} from "element-plus";

import importData from "./test/testdata.json";

// 定义列
const columns = [
	{key: "index", dataKey: "index", title: "序号", width: 50},
	// {key: "caseId", dataKey: "caseId", title: "案件ID", width: 170},
	{key: "startTime", dataKey: "startTime", title: "开始时间", width: 100},
	{key: "causeOfAction", dataKey: "causeOfAction", title: "案由", width: 200},
	{
		key: "litigantsNameShowText",
		dataKey: "litigantsNameShowText",
		title: "当事人",
		width: 300,
	},
	{
		key: "operation",
		dataKey: "operation",
		title: "操作",
		cellRenderer: () => (
			<>
				<ElButton type="primary" size="small" >
					编辑
				</ElButton>
			</>
		),
		width: 200,
		align: "center",
	},
];

const data = ref([]);
const currentRow = ref(null);
const dialogEditDataVisible = ref(false);
const caseInfoFormMode = ref("");

const loadData = () => {
	// 读取数据
	for (let i = 0; i < importData.length; i++) {
		let newData = {};

		newData = importData[i];
		newData["index"] = i + 1;
		newData["litigantsNameShowText"] =
			importData[i].plaintiffNames + " 诉 " + importData[i].defendantNames;

		// 把数据推送到data中
		data.value.push(newData);

		// console.log(data.value);
	}
};

// 创建新案件
function createNewCase() {
	dialogEditDataVisible.value = true;
	// 改变caseInfoFormMode为create（有edit和create两种模式）
	caseInfoFormMode.value = "create";
	// 将案件对象设为null，因为不需要传递现有案件对象到caseInfo之中
	currentRow.value = null;
}

// 编辑数据的前置函数
function handleEditData(val) {
	console.log("当前要编辑的案件id为" + val.caseId);
	dialogEditDataVisible.value = true;
	// 将当前要编辑的案件的对象传递给currentEditRow，便于接下来的组件调用
	currentRow.value = val;
	// 改变caseInfoFormMode为edit（有edit和create两种模式）
	caseInfoFormMode.value = "edit";

}


// 批量加载案件到后端,其中需要调用后端的函数
async function handleBulkLoadingData() {
	console.log("批量加载案件");
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleBulkLoadingData()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数
	else {
		let backendResult = await pywebview.api.inputAllCasesFromJson();
		if (backendResult == "Success") {
			// 如果后端返回成功，则刷新数据
			console.log("后端批量加载案件成功");
			loadData();
		} else if (backendResult == "Fail") {
			console.log("后端批量加载案件失败");
		}
	}
}

// 批量导出案件
async function handleBulkOutputData() {
	console.log("批量导出案件");
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === undefined) {
		console.log("handleBulkOutputData()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数outputAllCasesInfoToTxt
	else {
		pywebview.api.outputAllCasesToJson();
	}
}


// 测试后端输出的代码
function testOutputCase() {
	if (typeof pywebview === "undefined") {
		console.log("testOutputCase()：未连接后端，目前只测试前端");
	} else {
		console.log("测试函数，后端输出案件信息");
		pywebview.api.testCasesOutput();
	}
}

onMounted(() => {
	loadData();
});
</script>
