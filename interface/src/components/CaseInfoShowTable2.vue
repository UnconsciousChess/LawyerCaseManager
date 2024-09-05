<template>
	<div style="height: 300px">
		<el-auto-resizer>
			<template #default="{width, height}">
				<el-table-v2
					:sort-state="sortState"
					:columns="columns"
					:data="tableData"
					:width="width"
					:height="height"
					:estimated-row-height="50"
					@column-sort="onSort"
					fixed
				/>
			</template>
		</el-auto-resizer>
	</div>

	<!-- 表格外的功能按钮 -->
	<div style="margin-top: 20px">
		<el-button color="#9EC1DD" @click="createNewCase">新建案件</el-button>
		<el-button color="#B5BEF2" @click="loadAllCasesData">刷新数据</el-button>
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
import {ElMessage, ElNotification, TableV2SortOrder} from "element-plus";

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
	},
	{
		key: "causeOfAction",
		dataKey: "causeOfAction",
		title: "案由",
		width: 200,
		align: "right",
		cellRenderer: ({cellData: causeOfAction}) => (
			<el-tag type="warning">{causeOfAction}</el-tag>
		),
	},
	{
		key: "operation",
		dataKey: "operation",
		title: "功能菜单",
		width: 400,
		align: "right",

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
								<el-dropdown-item
									onClick={() => handleEditData(tableData.rowData)}
								>
									编辑
								</el-dropdown-item>

								<el-dropdown-item
									onClick={() => handleDeleteData(tableData.rowData)}
								>
									删除
								</el-dropdown-item>
							</el-dropdown-menu>
						),
					}}
				>
					<span style="color:#00a338">
						案件
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
								<el-dropdown-item
									onClick={() => handleOutputData(tableData.rowData)}
								>
									导出
								</el-dropdown-item>
								<el-dropdown-item disabled>上传</el-dropdown-item>
							</el-dropdown-menu>
						),
					}}
				>
					<span style="color:#626aef">
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
					<span style="color:var(--el-color-primary);">
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

const loadAllCasesData = async () => {
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
				// 从tableData中获取要更新的数据的index，找不到则返回-1
				var updateItemIndex = tableData.value.findIndex(
					(item) => item.caseId === cases[i].caseId
				);
				// 如果index不为-1，则为更新模式
				if (updateItemIndex !== -1) {
					// 对应的tableData更新数据
					tableData.value[updateItemIndex] = cases[i];
					// 添加原被告名称的显示文本
					tableData.value[updateItemIndex].litigantsNameShowText =
						cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames;
				} else {
					// 如果index为-1，即为新增模式，则将数据添加到tableData中
					let newData = {};
					newData = cases[i];
					// 添加原被告名称的显示文本
					newData["litigantsNameShowText"] =
						cases[i].plaintiffNames + " 诉 " + cases[i].defendantNames;

					tableData.value.push(newData);
				}
			}

			// 重新给tableData的序号赋值
			for (let i = 0; i < tableData.value.length; i++) {
				tableData.value[i].index = i + 1;
			}
		});
	}
};

// 加载单个案件数据
const loadSingleCaseData = async () => {
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("loadSingleCaseData()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		// 如果selectedRowData不为空
		if (selectedRowData.value != null) {
			// 获取当前案件的id
			let caseId = selectedRowData.value.caseId;
			// 调用后端函数，获取当前案件的数据
			let result = await pywebview.api.pushSingleCaseToDict(caseId);
			// 如果后端返回成功
			if (result == "Fail") {
				console.log("获取案件数据失败");
			} else {
				// 将该案件的数据更新到tableData中
				var updateItemIndex = tableData.value.findIndex(
					(item) => item.caseId === caseId
				);
				// 对应的tableData更新数据
				tableData.value[updateItemIndex] = result;
				tableData.value[updateItemIndex].litigantsNameShowText =
					result.plaintiffNames + " 诉 " + result.defendantNames;
			}

			// 重新给tableData的序号赋值
			for (let i = 0; i < tableData.value.length; i++) {
				tableData.value[i].index = i + 1;
			}
		} else {
			console.log("当前案件数据为空");
		}
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
	// 将编辑（新建）对话框关闭
	editDialogVisible.value = false;
	// 刷新数据
	loadSingleCaseData();
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
async function deleteData(val) {
	console.log("deleteData：当前确定要删除的案件id为" + val.caseId);
	// 将对话框隐藏
	deleteDialogVisible.value = false;

	// 获取要删除的数据的index
	var deleteItemIndex = tableData.value.findIndex(
		(item) => item.caseId === val.caseId
	);

	let deleteSuccessMessageText =
		val.litigantsNameShowText + val.causeOfAction + " 一案删除成功";

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

	// 弹出删除成功的提示
	ElMessage({
		message: deleteSuccessMessageText,
		type: "warning",
	});
}

// 输出数据的前置函数，作用是打开对话框，随后，再根据在对话框中的选择调用下面的outputToExcel或outputToTxt
function handleOutputData(val) {
	console.log("当前要输出的案件id为" + val.caseId);
	outputDialogVisible.value = true;
	// 将当前要输出的案件的对象传递给currentOutputRow，便于接下来的组件调用
	selectedRowData.value = val;
}

// 输出数据到txt
async function outputToJson(val) {
	// 将对话框隐藏
	outputDialogVisible.value = false;

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("outputToJson()：未连接后端，目前只测试前端");
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		let result = await pywebview.api.outputSingleCaseToJson(val.caseId);
		if (result == "Success") {
			ElNotification({
				title: "导出结果",
				message: "导出成功",
				type: "success",
				position: "bottom-right",
			});
		} else {
			ElNotification({
				title: "导出结果",
				message: "导出失败",
				type: "error",
				position: "bottom-right",
			});
		}
	}
}

// 输出数据到txt
async function outputToTxt(val) {
	// 将对话框隐藏
	outputDialogVisible.value = false;

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("outputToTxt()：未连接后端，目前只测试前端");
		return;
	}
	// 如果连接了后端，则调用后端的函数(实际运行环境)
	else {
		let result = await pywebview.api.outputSingleCaseToTxt(val.caseId);
		if (result == "Success") {
			ElNotification({
				title: "导出结果",
				message: "导出成功",
				type: "success",
				position: "bottom-right",
			});
		} else {
			ElNotification({
				title: "导出结果",
				message: "导出失败",
				type: "error",
				position: "bottom-right",
			});
		}
	}
}

// 唤起文书生成对话框
function handleGenerateDocuments(val) {
	chooseTemplateDialogVisible.value = true;
	selectedRowData.value = val;
}

// 收到从子组件传来的，文书生成的模板data以后，调用下面的DocumentsGenerate函数生成文书
async function documentsGenerate(data) {
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
		return;
	}
	// 如果连接了后端，则调用后端的函数,将当前案件id,以及模板id列表传到后端(实际运行环境)
	else {
		let result = await pywebview.api.documentsGenerate(
			selectedRowData.value.caseId,
			templateFileIdList
		);

		// 如果后端返回成功
		if (result == "Success") {
			ElNotification({
				title: "文书生成结果",
				message: "文书生成完毕",
				type: "success",
				position: "bottom-right",
			});
		}
		// 如果后端未返回成功，则直接输出后端返回的错误信息
		else {
			ElNotification({
				title: "文书生成结果",
				message: result,
				type: "error",
				position: "bottom-right",
			});
		}
	}
}

// 唤起文书合并对话框
function handleMergeDocuments(val) {
	// 显示文书合并对话框
	mergeFilesDialogVisible.value = true;
	selectedRowData.value = val;
}

// 打开案件文件夹
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
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleBulkLoadingData()：未连接后端，目前只测试前端");
		return;
	}
	// 如果连接了后端，则调用后端的函数
	else {
		let backendResult = await pywebview.api.inputAllCasesFromJson();
		if (backendResult == "Success") {
			// 如果后端返回成功，则刷新数据
			ElMessage({
				message: "批量加载案件成功",
				type: "success",
			});
			loadAllCasesData();
		} else if (backendResult == "Fail") {
			ElMessage({
				message: "批量加载案件失败",
				type: "error",
			});
		}
	}
}

// 批量导出案件
async function handleBulkOutputData() {
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === undefined) {
		console.log("handleBulkOutputData()：未连接后端，目前只测试前端");
		return;
	}
	// 如果连接了后端，则调用后端的函数outputAllCasesInfoToTxt
	else {
		pywebview.api.outputAllCasesToJson();
	}
}

// 测试后端输出的代码
function testOutputCase() {
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("testOutputCase()：未连接后端，目前只测试前端");
		return;
	}
	// 如果连接了后端，则调用后端的函数testCasesOutput
	else {
		pywebview.api.testCasesOutput();
	}
}

onMounted(() => {
	loadAllCasesData();
});
</script>

<style scoped></style>
