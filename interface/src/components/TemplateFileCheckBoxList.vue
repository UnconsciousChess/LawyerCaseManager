<template>
	<el-table
		:data="templateFilesData"
		style="width: 100%"
		empty-text="暂无模板文件信息"
		@selection-change="handleSelectionChange"
	>
		<el-table-column type="selection" width="55" />

		<el-table-column
			prop="templateFileName"
			label="文件名"
			width="410"
		></el-table-column>

		<el-table-column
			prop="templateFileStage"
			label="所属阶段"
			width="100"
		></el-table-column>
	</el-table>

	<div style="margin-top: 20px">
		<el-button type="success" @click="handleEmitGenerate">
			生成全部勾选文书
		</el-button>
	</div>
</template>

<script setup>


const templateFilesData = ref([]);
const multipleSelection = ref(null);

const handleSelectionChange = (val) => {
	multipleSelection.value = val
};


// 定义一个generate事件
const emit = defineEmits([
	"generate"
]);


// 将选中的对象，传递multipleSelection到父组件去
function handleEmitGenerate(){
	emit("generate",multipleSelection.value)
};


// 从后端中获取模板文件数据，作为数据加载到本组件里面
async function GetTemplateFileData() {
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("GetTemplateData()：未连接后端，目前只测试前端");
    }
    // 从后端获取数据(实际运行环境)
    else {
        await pywebview.api.backEndPushTemplateFileDataToFrontEnd().then((templateFiles) => {
            console.log("GetTemplateFileData()：从后端获取数据");

            for (let i = 0; i < templateFiles.length; i++) {
                // 对比id，如果有重复的数据则不添加
                if (templateFilesData.value.findIndex((item) => item.templateFileId === templateFiles[i].templateFileId) !== -1) {
                    continue;
                }
                else {
                    templateFilesData.value.push({
						templateFileId: templateFiles[i].templateFileId,
                        templateFileName: templateFiles[i].templateFileName,
                        templateFileStage: templateFiles[i].templateFileStage,
                    });

                }
            }
            // 读取完以后打印数据（测试）
            // console.log(templateFilesData.value)
        })
    }
}


onMounted(() =>{
	GetTemplateFileData();
})
</script>
