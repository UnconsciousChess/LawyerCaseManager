<template>
	<el-table
		:data="tableData"
		style="width: 100%"
		empty-text="目前暂无案件"
		:expand-row-keys="expandRowKeys"
		:row-key="(row) => row.caseId"
		@expand-change="(row, expandedRows) => generateShowText(row, expandedRows)"
	>
		<el-table-column label="" width="40" type="expand">
			<template #default>
				<CaseInfoShowDescription
					:propShowTextList="tableData"
					:propId="caseId"
				/>
			</template>
		</el-table-column>
		<el-table-column prop="index" label="序号" width="55" />
		<el-table-column prop="causeOfAction" label="案由" width="180" />
		<!-- <el-table-column prop="caseCourtCode" label="案号" width="200" /> -->
		<el-table-column prop="litigantsName" label="当事人" width="350" />
		<el-table-column fixed="right" label="操作" width="450">
			<template #default="{row}">
				<el-button type="primary" size="small" @click="handleEditData(row)"
					>编辑</el-button
				>
				<el-button type="danger" size="small" @click="handleDeleteData(row)"
					>删除</el-button
				>
				<el-button type="success" size="small" @click="handleOutputData(row)"
					>导出</el-button
				>
				<el-button color="#626aef" size="small" disabled>上传</el-button>
				<el-button
					type="warning"
					size="small"
					plain
					@click="handleDocumentsGenerate(row)"
					>文书生成</el-button
				>
				<el-button
					type="info"
					size="small"
					plain
					@click="handleDocumentsMerge(row)"
					>文书合并</el-button
				>
			</template>
		</el-table-column>
	</el-table>

	<!-- 刷新按钮 -->
	<div style="margin-top: 20px">
		<el-button color="#9EC1DD" @click="createNewCase">新建案件</el-button>
		<el-button color="#B5BEF2" @click="getTableData">刷新数据</el-button>
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

	<!-- 下面是按下按钮以后弹出的对话框 -->

	<!-- 编辑对话框 -->
	<el-dialog
		title="编辑案件信息"
		width="700"
		align-center
		v-model="dialogEditDataVisible"
	>
		<el-scrollbar height="600px">
			<CaseInfoForm
				ref="caseInfoFormRef"
				:propCaseData="currentEditRow"
				:propMode="caseInfoFormMode"
				@updateCaseData="updateCaseDataFromCaseInfoForm"
				@newCaseData="createNewCaseDataFromCaseInfoForm"
			/>
		</el-scrollbar>
	</el-dialog>

	<!-- 删除对话框 -->
	<el-dialog
		title="注意"
		v-model="dialogDeleteDataVisible"
		width="400"
		align-center
	>
		<span>确认删除当前案件吗？</span>
		<template #footer>
			<div>
				<el-button @click="dialogDeleteDataVisible = false">取消</el-button>
				<el-button type="danger" @click="deleteData(currentDeleteRow)"
					>确定</el-button
				>
			</div>
		</template>
	</el-dialog>

	<!-- 输出对话框 -->
	<el-dialog
		v-model="dialogOutputDataVisible"
		title="选择输出格式"
		width="500"
		align-center
	>
		<el-button type="primary" @click="outputToExcel(currentOutputRow)"
			>输出当前案件信息为Excel文件</el-button
		>
		<el-button type="success" @click="outputToTxt(currentOutputRow)"
			>输出当前案件信息为Txt文件</el-button
		>
	</el-dialog>

	<!-- 上传功能对话框（待开发）-->

	<!-- 选择生成文书对话框 -->
	<el-dialog
		title="选择生成文书"
		width="600"
		v-model="dialogChooseTemplateVisible"
	>
		<TemplateFileCheckBoxList @generate="documentsGenerate" />
	</el-dialog>

	<!-- 合并文书对话框 -->
	<el-dialog title="合并文书" width="800" v-model="dialogMergeFilesVisible">
		<el-scrollbar height="500px">
			<MergeFilesTable :caseId="currentMergeFilesRow.caseId" />
		</el-scrollbar>
	</el-dialog>
</template>

<script setup>
// 导入案件信息展示组件
import CaseInfoShowDescription from "./CaseInfoShowDescription.vue";
// 导入案件信息编辑表单组件
import CaseInfoForm from "./CaseInfoForm.vue";
// 导入选择模板文件列表组件
import TemplateFileCheckBoxList from "./TemplateFileCheckBoxList.vue";
// 导入合并文件列表组件
import MergeFilesTable from "./MergeFilesTable.vue";

// 导入测试数据
import {testCase1, testCase2, testCase3} from "./test/data.js";

// 初始化tableData，为空数组，是案件表格的数据
const tableData = ref([]);

// 这个变量是用于传递给子组件的caseId
const caseId = ref(null);

//一开始展开的行的数量为0
const currentExpandedRow = ref(0);

// 这个列表是存放展开的行的caseId（即rowkey）
const expandRowKeys = ref([]);


// 以下变量是用于控制各个对话框的显示的布尔值
const dialogOutputDataVisible = ref(false);
const dialogDeleteDataVisible = ref(false);
const dialogEditDataVisible = ref(false);
const dialogChooseTemplateVisible = ref(false);
const dialogMergeFilesVisible = ref(false);

// 当前编辑、删除、输出、生成的行的数据
const currentEditRow = ref(null);
const currentDeleteRow = ref(null);
const currentOutputRow = ref(null);
const currentGenerateRow = ref(null);
const currentMergeFilesRow = ref(null);

// 这个变量是用于控制编辑表单的模式，有edit和create两种模式
const caseInfoFormMode = ref(null);

// 引用子组件的ref(暂时无用)
const caseInfoFormRef = ref(null);

function generateShowText(row, expandedRows) {
	// 获取当前展开的行的数量，与currentExpandedRow进行比较

	// 如果expandedRows的长度大于currentExpandedRow,同时认为目前是点选了一下展开的状态
	if (expandedRows.length > currentExpandedRow.value) {
		// 将currentExpandedRow更新为当前展开的行的数量
		currentExpandedRow.value = expandedRows.length;
		// 要prop给子组件的caseId为当前行对象的caseId
		caseId.value = row.caseId;
		// 将当前行的caseId推向expandRowKeys
		expandRowKeys.value.push(row.caseId);
		// console.log("展开，当前展开行数量为" + currentExpandedRow.value);

		// 如果expandedRows的长度小于currentExpandedRow,同时认为目前是点选了一下收起的状态
	} else {
		// 将currentExpandedRow更新为当前展开的行的数量
		currentExpandedRow.value = expandedRows.length;
		// 从expandRowKeys中删除对应的caseId
		expandRowKeys.value.splice(
			expandRowKeys.value.findIndex((item) => item === row.caseId),
			1
		);
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
async function getTableData() {

	// 如果未连接后端，则只测试前端,并只导入默认数据
	if (typeof pywebview === "undefined") {
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

		let result = await pywebview.api.appStartInit();
		console.log(result);

		// 开始获取数据的过程
		pywebview.api.outputAllCaseInfoToFrontEnd().then((cases) => {
			// 遍历cases，将数据根据一定的规则添加到tableData中
			for (let i = 0; i < cases.length; i++) {
				// 对比案件的id，如果相同则不添加，改为更新
				if (
					tableData.value.findIndex(
						(item) => item.caseId === cases[i].caseId
					) !== -1
				) {
					// 获取要更新的数据的index
					var updateItemIndex = tableData.value.findIndex(
						(item) => item.caseId === cases[i].caseId
					);

					// 对应的tableData更新数据

					// 代理固定费用
					tableData.value[updateItemIndex].agentFixedFee =
						cases[i].agentFixedFee;

					// 代理阶段
					tableData.value[updateItemIndex].caseAgentStage =
						cases[i].caseAgentStage;

					// 案件文件夹路径
					tableData.value[updateItemIndex].caseFolderGeneratedPath =
						cases[i].caseFolderGeneratedPath;

					// 案件id
					// 案件id无须更新

					// 案件类型
					tableData.value[updateItemIndex].caseType = cases[i].caseType;

					// 案由
					tableData.value[updateItemIndex].causeOfAction =
						cases[i].causeOfAction;

					// 诉讼请求
					tableData.value[updateItemIndex].claimText = cases[i].claimText;

					// 当事人-被告
					tableData.value[updateItemIndex].defendants = cases[i].defendants;

					// 事实与理由
					tableData.value[updateItemIndex].factAndReason =
						cases[i].factAndReason;

					// 当事人-原告与被告
					tableData.value[updateItemIndex].litigantsName =
						cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames;

					// 诉讼标的额
					tableData.value[updateItemIndex].litigationAmount =
						cases[i].litigationAmount;

					// 调解意向
					tableData.value[updateItemIndex].mediationIntention =
						cases[i].mediationIntention;

					// 当事人-原告
					tableData.value[updateItemIndex].plaintiffs = cases[i].plaintiffs;

					// 拒绝调解理由
					tableData.value[updateItemIndex].rejectMediationReasonText =
						cases[i].rejectMediationReasonText;

					// 风险代理后付费率
					tableData.value[updateItemIndex].riskAgentPostFeeRate =
						cases[i].riskAgentPostFeeRate;

					// 风险代理状态
					tableData.value[updateItemIndex].riskAgentStatus =
						cases[i].riskAgentStatus;

					// 风险代理预付费
					tableData.value[updateItemIndex].riskAgentUpfrontFee =
						cases[i].riskAgentUpfrontFee;

					// 案件各阶段
					tableData.value[updateItemIndex].stages = cases[i].stages;

					// 当事人-第三人
					tableData.value[updateItemIndex].thirdParties = cases[i].thirdParties;

					// 表格title的数据
					tableData.value[updateItemIndex].title =
						cases[i].causeOfAction + "一案，编号：" + cases[i].caseId;
				} else {
					// 如果没有相同的，则将数据添加到tableData中
					tableData.value.push({
						agentFixedFee: cases[i].agentFixedFee,

						caseAgentStage: cases[i].caseAgentStage,

						caseFolderGeneratedPath: cases[i].caseFolderGeneratedPath,

						caseId: cases[i].caseId,

						caseType: cases[i].caseType,

						causeOfAction: cases[i].causeOfAction,

						claimText: cases[i].claimText,

						defendants: cases[i].defendants,

						factAndReason: cases[i].factAndReason,

						litigantsName:
							cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames,

						litigationAmount: cases[i].litigationAmount,

						mediationIntention: cases[i].mediationIntention,

						plaintiffs: cases[i].plaintiffs,

						rejectMediationReasonText: cases[i].rejectMediationReasonText,

						riskAgentPostFeeRate: cases[i].riskAgentPostFeeRate,

						riskAgentStatus: cases[i].riskAgentStatus,

						riskAgentUpfrontFee: cases[i].riskAgentUpfrontFee,

						stages: cases[i].stages,

						thirdParties: cases[i].thirdParties,

						title: cases[i].causeOfAction + "一案，编号：" + cases[i].caseId,
					});
					// console.log(tableData.value);
				}
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
	if (typeof pywebview === "undefined") {
		console.log("handleBulkLoadingData()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数
	else {
		let backendResult = await pywebview.api.inputAllCasesFromJson();
		if (backendResult == "Success") {
			// 如果后端返回成功，则刷新数据
			console.log("后端批量加载案件成功");
			getTableData();
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

// 编辑数据的前置函数
function handleEditData(val) {
	console.log("当前要编辑的案件id为" + val.caseId);
	dialogEditDataVisible.value = true;
	// 将当前要编辑的案件的对象传递给currentEditRow，便于接下来的组件调用
	currentEditRow.value = val;
	
	
	// 改变caseInfoFormMode为edit（有edit和create两种模式）
	caseInfoFormMode.value = "edit";
	// caseInfoFormRef.value.caseFormInfoInitiation();
}

// 收到子组件的编辑数据以后，父组件中的数据进行更新
function updateCaseDataFromCaseInfoForm() {
	console.log("更新案件信息");

	// 将对话框隐藏
	dialogEditDataVisible.value = false;

	// 从后端刷新数据 
	getTableData()
}


// 删除数据的前置函数，作用是打开对话框，提示是否删除，最终确认后调用下面的deleteData
function handleDeleteData(val) {

	dialogDeleteDataVisible.value = true;

	// 将当前要删除的案件的对象传递给currentDeleteRow，便于接下来的组件调用
	currentDeleteRow.value = val;
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
	if (typeof pywebview === "undefined") {
		console.log("deleteData()：未连接后端，目前只测试前端");
	}
	// 将对应的id传递给后端(实际运行环境)
	else {
		pywebview.api.backEndDeleteCase(val.caseId);
	}

	// 删除tableData中对应数组index的数据
	tableData.value.splice(deleteItemIndex, 1);

	// 对应的expandRowKeys也要删除
	expandRowKeys.value.splice(
		expandRowKeys.value.findIndex((item) => item === val.caseId),
		1
	);

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
	// console.log(val.caseId)
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
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
	if (typeof pywebview === "undefined") {
		console.log("outputToTxt()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		pywebview.api.outputCaseInfoToTxt(val.caseId);
	}
}

// 唤起文书生成对话框
function handleDocumentsGenerate(val) {
	// 显示文书生成对话框
	dialogChooseTemplateVisible.value = true;
	currentGenerateRow.value = val;
}

// 收到从子组件传来的，文书生成的模板data以后，调用下面的DocumentsGenerate函数生成文书
async function documentsGenerate(data) {
	console.log("文书生成");
	console.log(
		"documentsGenerate当前要生成文书的案件id为" +
			currentGenerateRow.value.caseId
	);

	// 将对话框隐藏
	dialogChooseTemplateVisible.value = false;

	console.log(data);
	// 将data里面的模板文件id传递给后端
	let templateFileIdList = [];
	for (let i = 0; i < data.length; i++) {
		templateFileIdList.push(data[i].templateFileId);
	}

	// 前后端通信部分

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleDocumentGenerate()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数,将当前案件id,以及模板id列表传到后端(实际运行环境)
	else {
		let result = await pywebview.api.documentsGenerate(
			currentGenerateRow.value.caseId,
			templateFileIdList
		);

		// 如果后端返回成功
		if (result == "Success") {
			console.log("文书生成成功");
			// 生成成功以后，刷新数据
			getTableData();
		}
		// 如果后端未返回成功则直接输出后端返回的错误信息
		else {
			console.log(result);
		}
	}
}

// 唤起文书合并对话框
function handleDocumentsMerge(val) {
	// 显示文书合并对话框
	dialogMergeFilesVisible.value = true;
	currentMergeFilesRow.value = val;
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

// 加载页面时先调用一次getTableData()获取数据
onMounted(() => {
	getTableData();
});
</script>
