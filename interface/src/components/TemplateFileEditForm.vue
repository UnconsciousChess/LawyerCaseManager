<script setup>
import { ref, onMounted,onUpdated,defineProps,defineEmits } from 'vue';

const templateFileEditData = ref({
    
    templateFileId: "",
    templateFileName: "",
    templateFileDir: "",
    templateFileType: "",
    templateFileStage: "",

})

// 从父组件传递过来的数据
const propData = defineProps({
    templateFile : Object
})

// 向父组件传递数据的事件
const emit = defineEmits([
    "updateTemplateFileData"
])

const templateFileTypeOptions = [
    {
        value: "directCopy",
        label: "直接复制",
    },

    {
        value: "docxtpl",
        label: "模板渲染",
    },
]

const templateFileStageOptions = [
    {
        value: '委托',    
        label: '委托阶段',
    },

    {
        value: '立案',
        label: "立案阶段",
    },

    {
        value: '审理',
        label: "审理阶段",
    },

    {
        value: '执行',
        label: "执行阶段",
    },

    {
        value: '归档',
        label: "归档阶段",
    },
]

function chooseTemplateFile(){
    console.log("chooseTemplateFile()：选择模板文件")
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("chooseTemplateFile()：未连接后端，目前只测试前端");
    }
    // 从后端获取数据(实际运行环境)
    else {
        pywebview.api.backEndChooseTemplateFile().then((result) => {
            if (result.res === "Success") {
                console.log("chooseTemplateFile():选择模板文件成功");
                // 如果返回结果成功，则变更当前表单的路径为新选择的路径,表单的templateFileName也对应变更
                templateFileEditData.value.templateFileDir = result.templateFileDir
                templateFileEditData.value.templateFileName = result.templateFileName
            }
            else if (result.res === "Cancel") {
                console.log("chooseTemplateFile():取消选择模板文件");
            }
            else {
                console.log("chooseTemplateFile():选择模板文件失败");
            }

        })
    }

}

function  updateTemplateFile(){
    console.log("updateTemplateFile()：更新模板文件信息")
    // 向父组件传递数据，事件名称为updateTemplateFileData，传递的数据为templateFileEditData.value
    emit("updateTemplateFileData",templateFileEditData.value)
}

function renderTemplateFileEditData(propData){
    console.log(propData.templateFile)
    // 赋值
    templateFileEditData.value.templateFileId = propData.templateFile.templateFileId
    templateFileEditData.value.templateFileName = propData.templateFile.templateFileName
    templateFileEditData.value.templateFileDir = propData.templateFile.templateFileDir
    templateFileEditData.value.templateFileType = propData.templateFile.templateFileType
    templateFileEditData.value.templateFileStage = propData.templateFile.templateFileStage
}


// 下面是生命周期钩子
onMounted(() => {
    console.log("加载TemplateFileEditForm.vue")
    renderTemplateFileEditData(propData);
})

onUpdated(() => {
    console.log("更新TemplateFileEditForm.vue")
    renderTemplateFileEditData(propData);
})  


</script>

<template>
    <el-form v-model="templateFileEditData" width="500px">
        <el-form-item label="模板文件id">
            <el-input disabled v-model="templateFileEditData.templateFileId" style="max-width: 200px">
            </el-input>
        </el-form-item>

        <el-form-item label="模板文件名">
            <el-input disabled v-model="templateFileEditData.templateFileName" style="max-width: 200px">
            </el-input>
        </el-form-item>

        <el-form-item label="模板文件路径">
            <el-input disabled v-model="templateFileEditData.templateFileDir" style="max-width: 400px">
            </el-input>
            <el-button type="danger" @click="chooseTemplateFile()">更改-浏览</el-button>
        </el-form-item>

        <el-form-item label="模板生成模式">
            <el-select v-model="templateFileEditData.templateFileType" style="width: 120px">
                <el-option v-for="item in templateFileTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
        </el-form-item>

        <el-form-item label="模板所属阶段">
            <el-select v-model="templateFileEditData.templateFileStage" style="width: 120px">
                <el-option v-for="item in templateFileStageOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="updateTemplateFile()">更新</el-button>
        </el-form-item>

    </el-form>
</template>