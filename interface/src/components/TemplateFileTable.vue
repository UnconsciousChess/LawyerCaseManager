<script setup>
import { ref, onMounted } from 'vue';

// 初始化模板文件数据
const templateFilesData = ref([]);

// const templateFilesData = ref([
//     {
//         templateFileId: "KCSDHIP",
//         templateFileName: '民事起诉状.docx',
//         templateFileDir: '\\test\\TestData\\被告.txt',
//         templateFileType: 'copyFile',
//         templateFileStage: '立案'
//     },
// ]);

const currentDeleteRow = ref(null);
const dialogDeleteDataVisible = ref(false);
const dialogEditDataVisible = ref(false);

async function GetTemplateFileData() {
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("GetTemplateData()：未连接后端，目前只测试前端");
    }
    // 从后端获取数据(实际运行环境)
    else {
        await pywebview.api.BackEndGetTemplateFileData().then((templateFiles) => {
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
                        templateFileDir: templateFiles[i].templateFileDir,
                        templateFileType: templateFiles[i].templateFileType,
                        templateFileStage: templateFiles[i].templateFileStage
                    });

                }
            }
            // 读取完以后打印一下数据（测试）
            console.log(templateFilesData.value)

        })
    }
}

// 读取文件列表txt
async function handleAddData() {
    console.log("handleAddData()：添加模板文件");
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("handleAddData()：未连接后端，目前只测试前端");
    }
    // 从后端获取数据(实际运行环境)
    else {
        await pywebview.api.BackEndAddTemplateFileData().then((result) => {
            if (result === "Success") {
                console.log("handleAddData():添加模板文件成功");
                // 如果添加成功，重新调用GetTemplateFileData获取数据
                GetTemplateFileData();
            }
            else if (result === "Cancel") {
                console.log("handleAddData():取消添加模板文件");
            }
            else {
                console.log("handleAddData():添加模板文件失败");
            }

        })
    }

}

// 导出模板文件列表到txt
async function handleOutputData() {
    console.log("handleOutputData()：导出当前文件列表");
    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("handleOutputData()：未连接后端，目前只测试前端");
    }
    // 从后端获取数据(实际运行环境)
    else {
        await pywebview.api.BackEndOutputTemplateFileData().then((result) => {
            if (result === "Success") {
                console.log("handleOutputData()：导出当前文件列表成功");
            }
            else if (result === "Cancel") {
                console.log("handleOutputData()：取消导出当前文件列表");
            }
            else {
                console.log("handleOutputData()：导出当前文件列表失败");
            }

        })
    }
}

// 编辑数据
function handleEditData(val) {
    console.log("handleEditData()：编辑模板文件");
    // 打开编辑数据的对话框
    dialogEditDataVisible.value = true;
}

// 删除数据的前置函数，作用是打开对话框，提示是否删除，最终确认后调用下面的deleteData
function handleDeleteData(val) {
    // 打开对话框
    dialogDeleteDataVisible.value = true;
    // 将当前要删除的案件的对象传递给currentDeleteRow，便于接下来的组件调用
    currentDeleteRow.value = val;
}

// 具体删除数据的函数
async function deleteData(val) {
    // console.log("当前要删除的案件id为" + val.caseId);

    // 将对话框隐藏
    dialogDeleteDataVisible.value = false;

    // 获取要删除的数据的index
    var deleteItemIndex = templateFilesData.value.findIndex(
        (item) => item.templateFileId === val.templateFileId
    );

    // 删除tableData中对应数组index的数据
    templateFilesData.value.splice(deleteItemIndex, 1);

    // 如果未连接后端，则只测试前端
    if (typeof pywebview === 'undefined') {
        console.log("deleteData()：未连接后端，目前只测试前端");
    }
    // 将对应的id传递给后端(实际运行环境)
    else {
        pywebview.api.BackEndDeleteTemplateFileData(val.templateFileId);
    }

}


// 加载页面时先调用一次GetTemplateFileData()获取数据
onMounted(() => {
    GetTemplateFileData();
});

</script>

<template>

    <el-table :data="templateFilesData" style="width: 100%" empty-text="暂无模板文件信息">
        <el-table-column prop="templateFileId" label="ID" width="100"></el-table-column>
        <el-table-column prop="templateFileName" label="文件名" width="180"></el-table-column>
        <el-table-column prop="templateFileDir" label="文件路径" width="280"></el-table-column>
        <el-table-column prop="templateFileType" label="生成方式" width="100"></el-table-column>
        <el-table-column prop="templateFileStage" label="所属阶段" width="100"></el-table-column>
        <el-table-column label="操作" width="300">
            <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEditData(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDeleteData(row)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-divider></el-divider>

    <div>
        <el-button color="#9EC1DD" @click="handleAddData">添加模板文件</el-button>
        <el-button color="#48C9B0" @click="handleOutputData">导出当前文件列表</el-button>
    </div>

    <!-- 下面是操作按钮以后的对话框 -->


    <!-- 编辑对话框 -->
    <el-dialog title="编辑" v-model="dialogEditDataVisible" width="500" align-center>
        
        
    </el-dialog>
    <!-- 删除对话框 -->
    <el-dialog title="注意" v-model="dialogDeleteDataVisible" width="400" align-center>
        <span>确认删除当前模板吗？</span>
        <template #footer>
            <div>
                <el-button @click="dialogDeleteDataVisible = false">取消</el-button>
                <el-button type="danger" @click="deleteData(currentDeleteRow)">确定</el-button>
            </div>
        </template>
    </el-dialog>

</template>