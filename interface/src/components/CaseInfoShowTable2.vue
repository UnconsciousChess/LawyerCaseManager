<template>
	<div style="height: 400px">
		<el-auto-resizer>
			<template #default="{width, height}">
				<el-table-v2
					v-model:sort-state="sortState"
					:columns="columns"
					:data="tableData"
					:width="width"
					:estimated-row-height="50"
					:height="height"
					fixed
					@column-sort="onSort"
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

	<!-- 下面是按下按钮以后弹出的对话框 -->

	<!-- 编辑对话框 -->
	<el-dialog
		title="编辑案件信息"
		width="900"
		align-center
		v-model="editDialogVisible"
		draggable
	>
		<el-scrollbar height="600px">
			<CaseInfoForm
				ref="caseInfoFormRef"
				:propCaseData="selectedRowData"
				:propMode="caseInfoFormMode"
				@updateCaseData="updateCaseDataFromCaseInfoForm"
			/>
		</el-scrollbar>
	</el-dialog>

	<!-- 删除对话框 -->
	<el-dialog
		title="注意"
		v-model="deleteDialogVisible"
		width="400"
		align-center
	>
		<span>确认删除当前案件吗？</span>
		<template #footer>
			<div>
				<el-button @click="deleteDialogVisible = false">取消</el-button>
				<el-button type="danger" @click="deleteData(selectedRowData)"
					>确定</el-button
				>
			</div>
		</template>
	</el-dialog>

	<!-- 输出对话框 -->
	<el-dialog
		v-model="outputDialogVisible"
		title="选择输出格式"
		width="500"
		align-center
	>
		<el-button type="primary" @click="outputToJson(selectedRowData)"
			>案件信息保存为JSON文件</el-button
		>
		<el-button type="success" @click="outputToTxt(selectedRowData)"
			>案件信息保存为TXT文件</el-button
		>
	</el-dialog>

	<!-- 上传功能对话框（待开发）-->

	<!-- 选择生成文书对话框 -->
	<el-dialog
		title="选择生成文书"
		width="600"
		v-model="chooseTemplateDialogVisible"
	>
		<TemplateFileCheckBoxList @generate="documentsGenerate" />
	</el-dialog>

	<!-- 合并文书对话框 -->
	<el-dialog title="合并文书" width="800" v-model="mergeFilesDialogVisible">
		<el-scrollbar height="500px">
			<MergeFilesTable :caseId="selectedRowData.caseId" />
		</el-scrollbar>
	</el-dialog>
</template>

<script setup lang="jsx">
import {onMounted} from "vue";
import {ref} from "vue";
import {ElMessage, TableV2SortOrder} from "element-plus";

// 引入用于测试的案件信息
import importData from "./test/testdata.json";

// 表格数据
const tableData = ref([]);

// 当前选中行的案件数据
const selectedRowData = ref(null);

// 各个对话框的显示状态
const editDialogVisible = ref(false);
const deleteDialogVisible = ref(false);
const outputDialogVisible = ref(false);
const chooseTemplateDialogVisible = ref(false);
const mergeFilesDialogVisible = ref(false);

// 案件编辑模式，有edit和create两种模式
const caseInfoFormMode = ref("");

// 定义列
const columns = [
	{key: "index", dataKey: "index", title: "序号", width: 50},
	// {key: "caseId", dataKey: "caseId", title: "案件ID", width: 170},
	{key: "startTime", dataKey: "startTime", title: "开始时间", width: 100},
	{
		key: "litigantsNameShowText",
		dataKey: "litigantsNameShowText",
		title: "当事人",
		width: 300,
		// headerCellRenderer : (props) => {
		// 	return props.column.title
		// },
	},
	{key: "causeOfAction", dataKey: "causeOfAction", title: "案由", width: 200},
	{
		key: "operation",
		dataKey: "operation",
		title: "功能菜单",
		width: 400,
		align: "center",

		cellRenderer: (tableData) => (
			<>
				{/* 案件操作（编辑和删除） */}
				<el-dropdown
					size="small"
					placement="bottom"
					style="margin-right: 20px"
					v-slots={{
						dropdown: () => (
							<el-dropdown-menu>
								<el-dropdown-item>
									<el-button
										type="primary"
										size="small"
										onClick={() => handleEditData(tableData.rowData)}
									>
										编辑
									</el-button>
								</el-dropdown-item>

								<el-dropdown-item>
									<el-button
										type="danger"
										size="small"
										onClick={() => handleDeleteData(tableData.rowData)}
									>
										删除
									</el-button>
								</el-dropdown-item>
							</el-dropdown-menu>
						),
					}}
				>
					<span class="el-dropdown-link">
						案件操作
						<el-icon class="el-icon--right">
							<arrow-down />
						</el-icon>
					</span>
				</el-dropdown>

				{/* 输出 */}
				<el-dropdown
					size="small"
					placement="bottom"
					style="margin-right: 20px"
					v-slots={{
						dropdown: () => (
							<el-dropdown-menu>
								<el-dropdown-item>
									<el-button
										type="success"
										size="small"
										onClick={() => handleOutputData(tableData.rowData)}
									>
										导出
									</el-button>
								</el-dropdown-item>
								<el-dropdown-item>
									<el-button color="#626aef" size="small" disabled>
										上传
									</el-button>
								</el-dropdown-item>
							</el-dropdown-menu>
						),
					}}
				>
					<span class="el-dropdown-link">
						输出
						<el-icon class="el-icon--right">
							<arrow-down />
						</el-icon>
					</span>
				</el-dropdown>

				{/* 文书 */}
				<el-dropdown
					size="small"
					placement="bottom"
					style="margin-right: 20px"
					v-slots={{
						dropdown: () => (
							<el-dropdown-menu>
								<el-dropdown-item
									onClick={() => handleGenerateDocuments(tableData.rowData)}
								>
									文书生成
								</el-dropdown-item>
								<el-dropdown-item
									onClick={() => handleMergeDocuments(tableData.rowData)}
								>
									文书合并
								</el-dropdown-item>
							</el-dropdown-menu>
						),
					}}
				>
					<span class="el-dropdown-link">
						文书
						<el-icon class="el-icon--right">
							<arrow-down />
						</el-icon>
					</span>
				</el-dropdown>

				{/* 打开案件文件夹 */}

				<el-button
					type="warning"
					size="small"
					link
					onClick={() => handleOpenCaseFolder(tableData.rowData)}
				>
					打开案件文件夹
				</el-button>
			</>
		),
	},
];

// 设置允许排序的列(按时间排序)
columns[1].sortable = true;

columns[2].filterable = true;

// 排序状态
const sortState = ref({
	startTime: TableV2SortOrder.ASC,
});

// 排序的方法
const onSort = ({key, order}) => {
	sortState.value[key] = order;

	// 按案件开始时间排序
	if (key === "startTime") {
		if (order === TableV2SortOrder.ASC) {
			tableData.value = tableData.value.sort(
				(a, b) => new Date(a.startTime) - new Date(b.startTime)
			);
		} else {
			tableData.value = tableData.value.sort(
				(a, b) => new Date(b.startTime) - new Date(a.startTime)
			);
		}

		// 重新给tableData的序号赋值
		for (let i = 0; i < tableData.value.length; i++) {
			tableData.value[i].index = i + 1;
		}
	}
};

const loadData = async () => {
	// 未连接后端，只调取前端
	if (typeof pywebview === "undefined") {
		for (let i = 0; i < importData.length; i++) {
			let newData = {};
			newData = importData[i];
			newData["index"] = i + 1;
			newData["litigantsNameShowText"] =
				importData[i].plaintiffNames + " 诉 " + importData[i].defendantNames;

			// 把数据推送到data中
			tableData.value.push(newData);
		}

	// 连接后端后的实际运行环境
	} else {

		// 开始获取数据
		await pywebview.api.pushAllCasesToList().then((cases) => {
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

					// 代理条件
					// console.log("更新代理条件信息");

					// console.log(cases[i].agentCondition);

					if (cases[i].agentCondition != null) {
						console.log("代理条件不为空");
						tableData.value[updateItemIndex].agentCondition =
							cases[i].agentCondition;
					}

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
					tableData.value[updateItemIndex].litigantsNameShowText =
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

					// 案件各阶段
					tableData.value[updateItemIndex].stages = cases[i].stages;

					// 当事人-第三人
					tableData.value[updateItemIndex].thirdParties = cases[i].thirdParties;

					// 开始时间
					tableData.value[updateItemIndex].startTime = cases[i].startTime;
				} else {
					// 如果没有相同的，则将数据添加到tableData中
					let newData = {};
					newData = cases[i];
					newData["index"] = i + 1;
					newData["litigantsNameShowText"] =
						cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames;

					tableData.value.push(newData);

				}
			}

		});
	}
};

// 创建新案件
function createNewCase() {
	// 打开编辑（新建）对话框
	editDialogVisible.value = true;
	// 改变caseInfoFormMode为create（有edit和create两种模式）
	caseInfoFormMode.value = "create";
	// 将案件对象设为null，因为不需要传递现有案件对象到caseInfo之中
	selectedRowData.value = null;
}

// 编辑数据的前置函数
function handleEditData(val) {
	console.log("当前要编辑的案件id为" + val.caseId);
	// 打开编辑（新建）对话框
	editDialogVisible.value = true;
	// 将当前要编辑的案件的对象传递给currentEditRow，便于接下来的组件调用
	selectedRowData.value = val;
	// 改变caseInfoFormMode为edit（有edit和create两种模式）
	caseInfoFormMode.value = "edit";
}

// 收到子组件的编辑数据以后，父组件中的数据进行更新
function updateCaseDataFromCaseInfoForm() {
	console.log("更新案件信息");
	// 将编辑（新建）对话框关闭
	editDialogVisible.value = false;
	// 刷新数据
	loadData();
}

// 删除数据的前置函数
function handleDeleteData(val) {
	console.log("handleDeleteData：当前要删除的案件id为" + val.caseId);
	// 打开删除对话框
	deleteDialogVisible.value = true;
	// 将当前要删除的案件的对象传递给selectedRowData，便于接下来的组件调用
	selectedRowData.value = val;
}

// 具体删除数据的函数
function deleteData(val) {
	console.log("deleteData：当前确定要删除的案件id为" + val.caseId);
	// 将对话框隐藏
	deleteDialogVisible.value = false;

	// 获取要删除的数据的index
	var deleteItemIndex = tableData.value.findIndex(
		(item) => item.caseId === val.caseId
	);
	console.log("要删除的数据的index为" + deleteItemIndex);

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("deleteData()：未连接后端，目前只测试前端");
	}
	// 将对应的id传递给后端(实际运行环境)
	else {
		pywebview.api.backEndDeleteCase(val.caseId);
	}

	// 删除前端tableData中对应数组index的数据
	tableData.value.splice(deleteItemIndex, 1);

	// 重新给tableData的序号赋值
	for (let i = 0; i < tableData.value.length; i++) {
		tableData.value[i].index = i + 1;
	}
}

// 输出数据的前置函数，作用是打开对话框，随后，再根据在对话框中的选择调用下面的outputToExcel或outputToTxt
function handleOutputData(val) {
	console.log("当前要输出的案件id为" + val.caseId);
	outputDialogVisible.value = true;
	// 将当前要输出的案件的对象传递给currentOutputRow，便于接下来的组件调用
	selectedRowData.value = val;
}

// 输出数据到txt
function outputToJson(val) {
	// 将对话框隐藏
	outputDialogVisible.value = false;

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("outputToJson()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		pywebview.api.outputSingleCaseToJson(val.caseId);
	}
}

// 输出数据到txt
function outputToTxt(val) {
	// 将对话框隐藏
	outputDialogVisible.value = false;

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("outputToTxt()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		pywebview.api.outputSingleCaseToTxt(val.caseId);
	}
}

// 唤起文书生成对话框
function handleGenerateDocuments(val) {
	chooseTemplateDialogVisible.value = true;
	selectedRowData.value = val;
}

// 收到从子组件传来的，文书生成的模板data以后，调用下面的DocumentsGenerate函数生成文书
async function documentsGenerate(data) {
	console.log("文书生成");
	console.log("当前要生成文书的案件id为" + selectedRowData.value.caseId);

	// 将对话框隐藏
	chooseTemplateDialogVisible.value = false;

	// 将data里面的模板文件id传递给后端
	let templateFileIdList = [];
	for (let i = 0; i < data.length; i++) {
		templateFileIdList.push(data[i].id);
	}

	// 前后端通信部分

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleDocumentGenerate()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数,将当前案件id,以及模板id列表传到后端(实际运行环境)
	else {
		let result = await pywebview.api.documentsGenerate(
			selectedRowData.value.caseId,
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
function handleMergeDocuments(val) {
	// 显示文书合并对话框
	mergeFilesDialogVisible.value = true;
	selectedRowData.value = val;
}

async function handleOpenCaseFolder(val) {
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleOpenCaseFolder()：未连接后端，目前只测试前端");
		console.log("选择的案件id为:" + val.caseId);
		// 输出Elmessage
		ElMessage({
			message: "所选案件文件夹路径为：" + val.caseFolderGeneratedPath,
			type: "info",
		});
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		var result = await pywebview.api.openCaseFolder(val.caseId);
		if (result == "Success") {
			ElMessage({
				message: "打开案件文件夹成功",
				type: "success",
			});
		} else if (result == "CaseFolderNotExist") {
			ElMessage({
				message: "案件文件夹不存在",
				type: "error",
			});
		} else if (result == "CaseFolderPathNotExist") {
			ElMessage({
				message: "该案件没有设定文件夹路径",
				type: "info",
			});
		}
	}
}

// === 以下是表格下方的功能按钮的函数 ===

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
	console.log("测试函数，后端输出案件信息");
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("testOutputCase()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数testCasesOutput
	else {
		pywebview.api.testCasesOutput();
	}
}

onMounted(() => {
	loadData();
});
</script>
