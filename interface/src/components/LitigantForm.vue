<template>
	<el-form>
		<el-form-item v-if="litigantForm.litigantPosition === 'plaintiff'" label="原告名字">
			<el-input v-model="litigantForm.litigantName" />
		</el-form-item>
        <el-form-item v-else label="被告名字">
            <el-input v-model="litigantForm.litigantName" />
        </el-form-item>


		<el-form-item v-if="litigantForm.litigantPosition === 'plaintiff'" label="原告身份证号码">
			<el-input v-model="litigantForm.litigantIdNumber" />
		</el-form-item>

        <el-form-item v-else label="被告身份证号码">
            <el-input v-model="litigantForm.litigantIdNumber" />
        </el-form-item>


		<el-form-item v-if="litigantForm.litigantPosition === 'plaintiff'" label="原告电话号码">
			<el-input v-model="litigantForm.litigantPhoneNumber" />
		</el-form-item>

        <el-form-item v-else label="被告电话号码">
            <el-input v-model="litigantForm.litigantPhoneNumber" />
        </el-form-item>

        <el-form-item v-if="litigantForm.litigantPosition === 'plaintiff'" label="原告信息txt路径" prop="litigantInfoPath">
            <el-input v-model="litigantForm.litigantInfoPath" />
        </el-form-item>

        <el-form-item v-else label="被告信息txt路径" prop="litigantInfoPath">
            <el-input v-model="litigantForm.litigantInfoPath" />
        </el-form-item>

        <el-form-item>
            <el-row v-if="litigantForm.litigantPosition === 'plaintiff'">
                <el-col :span="18">
                    <el-button  type="primary" plain @click="sumbitCurrentlitigantInfo">提交该原告信息</el-button>
                </el-col>
                <el-col :span="6">
                    <el-button  type="info" plain @click="deleteCurrentlitigantInfo">删除该原告</el-button>
                </el-col>
            </el-row>
            
            <el-row v-else>
                <el-col :span="18">
                    <el-button  type="danger" plain @click="sumbitCurrentlitigantInfo">提交该被告信息</el-button>
                </el-col>
                <el-col :span="6">
                    <el-button  type="info"  @click="deleteCurrentlitigantInfo">删除该被告</el-button>
                </el-col>
            </el-row>
        </el-form-item>


	</el-form>
</template>


<script setup>

import { ref, onMounted} from 'vue'

const props = defineProps({
    litigantPosition: String,
})

const litigantForm = ref({
	litigantName: "",
	litigantIdNumber: "",
	litigantPhoneNumber: "",
    litigantInfoPath: "",
    litigantPosition: "",
});


const litigantFormRef = ref(null);



function sumbitCurrentlitigantInfo() {
    console.log(litigantForm.value);
}

function deleteCurrentlitigantInfo() {

    if (litigantForm.value.litigantPosition === 'plaintiff') {
        console.log("删除了一个原告");
    } else {
        console.log("删除了一个被告");
    }

}

onMounted(() => {
    // 在这里赋值
    litigantForm.value.litigantPosition = props.litigantPosition;
})

</script>
