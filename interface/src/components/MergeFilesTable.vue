<template>
	<div style="margin-bottom: 20px">
		<el-button type="danger" @click="getFilesData"> 刷新数据 </el-button>
		<el-select
			v-model="value"
			placeholder="选择预设模板"
			style="width: 130px; margin-left: 100px"
		>
			<el-option
				v-for="item in options"
				:key="item.value"
				:label="item.label"
				:value="item.value"
			></el-option>
		</el-select>
	</div>

	<el-table
		:data="filesData"
		style="width: 100%"
		empty-text="文件夹中无文件"
		v-loading="loading"
		element-loading-text="合并中..."
		element-loading-background="#f4fff4"
		@selection-change="handleSelectionChange"
	>
		<el-table-column type="selection" width="55" />
		<el-table-column
			prop="fileName"
			label="文件名"
			width="200"
		></el-table-column>
		<el-table-column
			prop="fileDir"
			label="文件路径"
			width="500"
		></el-table-column>
	</el-table>

	<div style="margin-top: 30px">
		<el-button type="primary" @click="handleMerge"> 合并为pdf </el-button>
	</div>
</template>

<script setup>
// 导入测试数据

import {folder1, folder2} from "./test/data.js";

// 从父组件接收数据
const props = defineProps({
	caseId: String,
});

// 表格数据，代表案件文件夹中的文件名
const filesData = ref([]);

const value = ref("");

// 加载状态
const loading = ref(false);

const options = [
	{value: "1", label: "委托材料"},
	{value: "2", label: "起诉材料"},
	{value: "3", label: "归档材料"},
	{value: "4", label: "其他材料"},
];

// 选中的文件
const multipleSelection = ref(null);

const handleSelectionChange = (val) => {
	multipleSelection.value = val;
};

// 从后端获取当前案件下的所有文件并加载到前端
async function getFilesData() {
	// 如果未连接后端，则只测试前端，导入测试数据
	if (typeof pywebview === "undefined") {
		if (filesData.value.length === 0) {
			filesData.value.push(folder1, folder2);
		}
		console.log("getFileData()：未连接后端，目前只测试前端");
	}
	// 从后端获取数据(实际运行环境)
	else {
		// 得到一个result，
		// 当正常运行时，result是一个数组，数组中的每个元素是一个对象，对象中包含文件名和文件路径
		// 当运行错误时，result是一个字符串，字符串中包含错误信息
		let result = await pywebview.api.backEndGetCaseFolderFiles(props.caseId);
		if (typeof result === "string") {
			console.log("getFilesData()：", result);
			return;
		} else {
			// 将result中的每个对象的文件名和文件路径分别存入filesData中
			filesData.value = [];
			for (let i = 0; i < result.length; i++) {
				filesData.value.push({
					fileName: result[i].name,
					fileDir: result[i].path,
				});
			}
		}
	}
}

async function handleMerge() {
	// 如果未选中文件，则提示未选中文件
	if (multipleSelection.value === null) {
		console.log("未选中文件");
		return;
	}
	// 将选中的文件编成一个数组
	let selectedFilesDir = [];
	for (let i = 0; i < multipleSelection.value.length; i++) {
		selectedFilesDir.push(multipleSelection.value[i].fileDir);
	}

	// 开始loading
	loading.value = true;

	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("handleMerge()：未连接后端，目前只测试前端");
	}
	// 如果已经连接到后端，则传递给后端（实际运行环境）
	else {
		console.log("选中的文件路径：", selectedFilesDir);
		// 将从前端传输过来的caseId，以及选中的文件路径传递给后端，进行合并
		let result = await pywebview.api.backEndMergeFiles(
			props.caseId,
			selectedFilesDir
		);

		// 根据后端返回的结果，判断是否合并成功，并输出到前端
		if (result === "success") {
			console.log("合并成功");
		} else {
			console.log("合并失败");
		}

		// 结束loading
		loading.value = false;
		return;
	}
}

onMounted(() => {
	getFilesData();
});

watchEffect(() => {
	console.log("MergeFilesTable已经更新");
	getFilesData();
});
</script>
