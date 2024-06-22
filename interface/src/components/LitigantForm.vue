<template>
	<el-form :model="litigantForm" label-width="auto" style="max-width: 700px">
		<el-form-item
			v-if="litigantForm.litigantPosition === 'plaintiff'"
			label="原告名字"
		>
			<el-input v-model="litigantForm.litigantName" />
		</el-form-item>
		<el-form-item v-else label="被告名字">
			<el-input v-model="litigantForm.litigantName" />
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantPosition === 'plaintiff'"
			label="原告身份证号码"
		>
			<el-row width="50">
				<el-col :span="18">
					<el-input v-model="litigantForm.litigantIdNumber" />
				</el-col>
				<el-col :span="6">
					<el-button type="info" @click="checkIdNumber">校验证件号码</el-button>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item v-else label="被告身份证号码">
			<el-row width="50">
				<el-col :span="18">
					<el-input v-model="litigantForm.litigantIdNumber" />
				</el-col>
				<el-col :span="6">
					<el-button type="info" @click="checkIdNumber">校验证件号码</el-button>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantPosition === 'plaintiff'"
			label="原告电话号码"
		>
			<el-input v-model="litigantForm.litigantPhoneNumber" />
		</el-form-item>

		<el-form-item v-else label="被告电话号码">
			<el-input v-model="litigantForm.litigantPhoneNumber" />
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantPosition === 'plaintiff'"
			label="原告地址"
		>
			<el-input v-model="litigantForm.litigantAddress" />
		</el-form-item>

		<el-form-item v-else label="被告地址">
			<el-input v-model="litigantForm.litigantAddress" />
		</el-form-item>

		<el-form-item label="是否采取txt导入信息" prop="litigantInfoPath">
			<el-switch
				v-model="litigantForm.litigantInfoByPath"
				active-text="是"
				inactive-text="否"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantPosition === 'plaintiff'"
			label="原告信息txt路径"
			prop="litigantInfoPath"
		>
			<el-input v-model="litigantForm.litigantInfoPath" />
		</el-form-item>

		<el-form-item v-else label="被告信息txt路径" prop="litigantInfoPath">
			<el-input v-model="litigantForm.litigantInfoPath" />
		</el-form-item>

		<el-form-item>
			<el-row :gutter="60" v-if="litigantForm.litigantPosition === 'plaintiff'">
				<el-col :span="6">
					<el-button type="success" plain @click="sumbitCurrentlitigantInfo"
						>提交该原告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="danger" plain @click="deleteCurrentlitigantInfo"
						>删除该原告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="info" plain @click="checkInfo">检验信息</el-button>
				</el-col>
			</el-row>

			<el-row :gutter="60" v-else>
				<el-col :span="6">
					<el-button type="success" @click="sumbitCurrentlitigantInfo"
						>提交该被告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="danger" @click="deleteCurrentlitigantInfo"
						>删除该被告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="info" @click="checkInfo">检验信息</el-button>
				</el-col>
			</el-row>
		</el-form-item>
	</el-form>
</template>

<script setup>
import {ref, onMounted, onBeforeUpdate} from "vue";

import {checkIdNumberValid, checkEnterpriseIdNumberValid} from "../js/check.js";

const props = defineProps({
	litigantPosition: String,
	litigantIndex: Number,
});

const litigantForm = ref({
	litigantName: "",
	litigantIdNumber: "",
	litigantPhoneNumber: "",
	litigantAddress: "",
	litigantInfoPath: "",
	litigantPosition: "",
	litigantIndex: 0,
	litigantInfoByPath: false,
});

const litigantFormRef = ref(null);

function checkIdNumber() {
	// console.log(litigantForm.value.litigantIdNumber)
	let result = checkIdNumberValid(litigantForm.value.litigantIdNumber);
	if (result == false) {
		console.log("该身份号码不合法");
	} else {
		console.log("该身份号码合法");
	}
}

function sumbitCurrentlitigantInfo() {
	if (litigantForm.value.litigantPosition === "plaintiff") {
		console.log("提交了一个原告");
	} else {
		console.log("提交了一个被告");
	}
	console.log(litigantForm.value);
}

function deleteCurrentlitigantInfo() {
	if (litigantForm.value.litigantPosition === "plaintiff") {
		console.log("删除了一个原告");
	} else {
		console.log("删除了一个被告");
	}
}

function checkInfo() {
	console.log("检验信息");
}

onMounted(() => {
	// 在这里赋值
	litigantForm.value.litigantPosition = props.litigantPosition;
	// litigantForm.value.litigantIndex = props.litigantIndex;
});

onBeforeUpdate(() => {});
</script>
