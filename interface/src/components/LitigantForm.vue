<template>
	<el-form>
		<el-form-item label="原告名字">
			<el-input v-model="litigantForm.plaintiffName" />
		</el-form-item>
		<el-form-item label="原告身份证号">
			<el-input v-model="litigantForm.plaintiffIdNumber" />
		</el-form-item>
		<el-form-item label="原告电话号码">
			<el-input v-model="litigantForm.plaintiffPhoneNumber" />
		</el-form-item>
	</el-form>
</template>


<script setup>

import { ref, onMounted , reactive} from 'vue'


const litigantForm = ref({
	plaintiffName: "",
	plaintiffIdNumber: "",
	plaintiffPhoneNumber: "",
});


const litigantFormRef = ref(null);

</script>
