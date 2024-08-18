<script setup>
const templateFileEditData = ref({
	id: "",
	fileName: "",
	dir: "",
	renderType: "",
	renderStage: "",
	multiRenderOption: "",
});

// 从父组件传递过来的数据
const propData = defineProps({
	templateFile: Object,
});

// 向父组件传递数据的事件
const emit = defineEmits(["updateTemplateFileData"]);

const renderTypeOptions = [
	{
		value: "directCopy",
		label: "直接复制",
	},

	{
		value: "docxtpl",
		label: "模板渲染",
	},
];

const renderStageOptions = [
	{
		value: "委托",
		label: "委托阶段",
	},

	{
		value: "立案",
		label: "立案阶段",
	},

	{
		value: "审理",
		label: "审理阶段",
	},

	{
		value: "执行",
		label: "执行阶段",
	},

	{
		value: "归档",
		label: "归档阶段",
	},
];

const multiRenderOptions = [
	{
		value: "",
		label: "无",
	},

	{
		value: "Us",
		label: "按我方当事人逐个渲染",
	},
	{
		value: "Opponents",
		label: "按对方当事人逐个渲染",
	},
	{
		value: "Courts",
		label: "按法院逐个渲染",
	},
    {
        value: "CourtsAndUs",
        label: "按法院和我方当事人逐个渲染"        
    },
    {
        value: "CourtsAndOpponents",
        label: "按法院和对方当事人逐个渲染"        
    },

    
];

function chooseTemplateFile() {
	console.log("chooseTemplateFile()：选择模板文件");
	// 如果未连接后端，则只测试前端
	if (typeof pywebview === "undefined") {
		console.log("chooseTemplateFile()：未连接后端，目前只测试前端");
	}
	// 从后端获取数据(实际运行环境)
	else {
		pywebview.api.backEndChooseTemplateFile().then((result) => {
			if (result.res === "Success") {
				console.log("chooseTemplateFile():选择模板文件成功");
				// 如果返回结果成功，则变更当前表单的路径为新选择的路径,表单的fileName也对应变更
				templateFileEditData.value.dir = result.dir;
				templateFileEditData.value.fileName = result.fileName;
			} else if (result.res === "Cancel") {
				console.log("chooseTemplateFile():取消选择模板文件");
			} else {
				console.log("chooseTemplateFile():选择模板文件失败");
			}
		});
	}
}

function updateTemplateFile() {
	console.log("updateTemplateFile()：更新模板文件信息");
	// 向父组件传递数据，事件名称为updateTemplateFileData，传递的数据为templateFileEditData.value
	emit("updateTemplateFileData", templateFileEditData.value);
}

function renderTemplateFileEditData(propData) {
	console.log(propData.templateFile);
	// 赋值
	templateFileEditData.value.id = propData.templateFile.id;
	templateFileEditData.value.fileName = propData.templateFile.fileName;
	templateFileEditData.value.dir = propData.templateFile.dir;
	templateFileEditData.value.renderType = propData.templateFile.renderType;
	templateFileEditData.value.renderStage = propData.templateFile.renderStage;
	templateFileEditData.value.multiRenderOption =
		propData.templateFile.multiRenderOption;
}

// 下面是生命周期钩子
onMounted(() => {
	console.log("加载TemplateFileEditForm.vue");
	renderTemplateFileEditData(propData);
});

onUpdated(() => {
	console.log("更新TemplateFileEditForm.vue");
	renderTemplateFileEditData(propData);
});
</script>

<template>
	<el-form v-model="templateFileEditData" width="500px">
		<el-row>
			<el-form-item label="模板id">
				<el-input
					disabled
					v-model="templateFileEditData.id"
					style="max-width: 80px;margin-right: 10px"
				>
				</el-input>
			</el-form-item>

			<el-form-item label="文件名">
				<el-input
					disabled
					v-model="templateFileEditData.fileName"
					style="max-width: 150px;margin-right: 5px"
				>
				</el-input>
			</el-form-item>

		</el-row>

		<el-form-item label="文件路径">
			<el-input
				disabled
				v-model="templateFileEditData.dir"
				style="max-width: 300px; margin-right: 10px"
			>
			</el-input>
			<el-button type="danger" @click="chooseTemplateFile()">更改</el-button>
		</el-form-item>

		<el-row>
			<el-form-item label="生成模式">
				<el-select
					v-model="templateFileEditData.renderType"
					style="width: 100px;margin-right:15px;"
				>
					<el-option
						v-for="item in renderTypeOptions"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					/>
				</el-select>
			</el-form-item>

			<el-form-item label="所属阶段">
				<el-select
					v-model="templateFileEditData.renderStage"
					style="width: 100px"
				>
					<el-option
						v-for="item in renderStageOptions"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					/>
				</el-select>
			</el-form-item>
		</el-row>

		<el-row v-if="templateFileEditData.renderType == 'docxtpl'">
			<el-form-item label="循环渲染属性">
				<el-select
					v-model="templateFileEditData.multiRenderOption"
					style="width: 240px;margin-right: 10px;"
				>
					<el-option
						v-for="item in multiRenderOptions"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					></el-option>
				</el-select>
			</el-form-item>
		</el-row>

        <el-button type="success" @click="updateTemplateFile()" style="margin-top: 10px;">更新当前模板文件属性</el-button>
	</el-form>
</template>
