<template>
	<el-form :model="litigantForm" label-width="150px" style="max-width: 700px">
		<el-form-item label="是否采取txt导入信息">
			<el-switch
				v-model="litigantForm.litigantInfoByPath"
				active-text="是"
				inactive-text="否"
			/>
		</el-form-item>

		<el-form-item
			v-if="
				litigantForm.litigantPosition === 'plaintiff' &&
				litigantForm.litigantInfoByPath == true
			"
			label="原告信息txt路径"
		>
			<el-input v-model="litigantForm.litigantInfoPath" />
		</el-form-item>

		<el-form-item
			v-else-if="
				litigantForm.litigantPosition === 'defendant' &&
				litigantForm.litigantInfoByPath == true
			"
			label="被告信息txt路径"
		>
			<el-input v-model="litigantForm.litigantInfoPath" />
		</el-form-item>

		<el-form-item
			v-if="
				litigantForm.litigantPosition === 'plaintiff' &&
				litigantForm.litigantInfoByPath == false
			"
			label="原告名字"
		>
			<el-input v-model="litigantForm.litigantName" prop="litigantName" />
		</el-form-item>

		<el-form-item
			v-else-if="
				litigantForm.litigantPosition === 'defendant' &&
				litigantForm.litigantInfoByPath == false
			"
			label="被告名字"
		>
			<el-input v-model="litigantForm.litigantName" prop="litigantName" />
		</el-form-item>

		<el-form-item
			v-if="
				litigantForm.litigantPosition === 'plaintiff' &&
				litigantForm.litigantInfoByPath == false
			"
			label="原告身份证号码"
		>
			<el-row width="70">
				<el-col :span="16">
					<el-input v-model="litigantForm.litigantIdNumber" />
				</el-col>
				<el-col :span="6">
					<el-button type="info" @click="checkIdNumber">校验证件号码</el-button>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item
			v-else-if="
				litigantForm.litigantPosition === 'defendant' &&
				litigantForm.litigantInfoByPath == false
			"
			label="被告身份证号码"
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

		<el-form-item
			v-if="
				litigantForm.litigantPosition === 'plaintiff' &&
				litigantForm.litigantInfoByPath == false
			"
			label="原告电话号码"
		>
			<el-input v-model="litigantForm.litigantPhoneNumber" />
		</el-form-item>

		<el-form-item
			v-else-if="
				litigantForm.litigantPosition === 'defendant' &&
				litigantForm.litigantInfoByPath == false
			"
			label="被告电话号码"
		>
			<el-input v-model="litigantForm.litigantPhoneNumber" />
		</el-form-item>

		<el-form-item
			v-if="
				litigantForm.litigantPosition === 'plaintiff' &&
				litigantForm.litigantInfoByPath == false
			"
			label="原告地址"
		>
			<el-input v-model="litigantForm.litigantAddress" />
		</el-form-item>

		<el-form-item
			v-else-if="
				litigantForm.litigantPosition === 'defendant' &&
				litigantForm.litigantInfoByPath == false
			"
			label="被告地址"
		>
			<el-input v-model="litigantForm.litigantAddress" />
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
					<el-button type="info" plain @click="checkInfo"
						>该功能未完善</el-button
					>
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
					<el-button type="info" @click="checkInfo">该功能未完善</el-button>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item>
			<ul>
				<li v-for="(value, key) in litigantForm">
					{{ key }} : {{ value }}
				</li>
			</ul>
		</el-form-item>
	</el-form>
</template>

<script setup>
import {ref, onMounted, inject, onUpdated} from "vue";

import {checkIdNumberValid, checkEnterpriseIdNumberValid} from "../js/check.js";

// 从父组件中获取方法
const reducePlaintiff = inject("reducePlaintiff");
const reduceDefendant = inject("reduceDefendant");
const getCurrentplaintiffData = inject("getCurrentplaintiffData");
const getCurrentDefendantData = inject("getCurrentDefendantData");

const props = defineProps({
	litigantPosition: String,
	id: Number,
});

const litigantForm = ref({
	litigantName: "",
	litigantIdNumber: "",
	litigantPhoneNumber: "",
	litigantAddress: "",
	litigantInfoPath: "",
	litigantPosition: "",
	litigantInfoByPath: true,
	id : 0,

});



// 检查身份证号码是否合法
function checkIdNumber() {
	let result = checkIdNumberValid(litigantForm.value.litigantIdNumber);
	// 下面是测试部分，后面将控制台打印改为弹窗提示
	if (result == false) {
		console.log("该身份号码不合法");
	} else {
		console.log("该身份号码合法");
	}
}

function sumbitCurrentlitigantInfo() {
	if (litigantForm.value.litigantPosition === "plaintiff") {
		console.log("提交了一个原告");
		getCurrentplaintiffData(litigantForm.value, litigantForm.value.id);
	} else {
		console.log("提交了一个被告");
		getCurrentDefendantData(litigantForm.value, litigantForm.value.id);
	}
}

function deleteCurrentlitigantInfo() {
	if (litigantForm.value.litigantPosition === "plaintiff") {
		reducePlaintiff(litigantForm.value.id);
		console.log("删除了一个原告");
	} else {
		reduceDefendant(litigantForm.value.id);
		console.log("删除了一个被告");
	}
}

function checkInfo() {
	console.log("该功能未完善");
	console.log(litigantForm.value);
}

onMounted(() => {
	// 在这里赋值
	litigantForm.value.litigantPosition = props.litigantPosition;
	litigantForm.value.id = props.id;
	
});



// 将litigantForm暴露给父组件
defineExpose({
	litigantForm,
});
</script>
