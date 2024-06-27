<template>
	<!-- 原告表单 -->
	<el-form
		:model="litigantForm"
		label-width="180px"
		:style="{
			'max-width': '700px',
			'background-color': '#FFEEBB',
		}"
		v-if="litigantForm.litigantPosition === 'plaintiff'"
	>
		<el-form-item label="是否采取文件导入信息">
			<el-switch
				v-model="litigantForm.litigantInfoByPath"
				style="--el-switch-on-color: #ffc105; --el-switch-off-color: #c4c4c4"
				active-text="是"
				inactive-text="否"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == true"
			label="原告信息文件路径"
		>
			<el-input
				v-model="litigantForm.litigantInfoPath"
				style="max-width: 500px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="原告名字"
		>
			<el-input
				v-model="litigantForm.litigantName"
				prop="litigantName"
				style="max-width: 300px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="原告身份证号码"
		>
			<el-row width="70" :gutter="50">
				<el-col :span="20">
					<el-input
						v-model="litigantForm.litigantIdNumber"
						style="max-width: 400px"
					/>
				</el-col>
				<el-col :span="4">
					<el-button color="#EFBA1B" @click="checkIdNumber"
						>校验证件号码</el-button
					>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="原告电话号码"
		>
			<el-input
				v-model="litigantForm.litigantPhoneNumber"
				style="max-width: 400px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="原告地址"
		>
			<el-input
				v-model="litigantForm.litigantAddress"
				style="max-width: 400px"
			/>
		</el-form-item>

		<el-form-item>
			<el-row :gutter="60">
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
		</el-form-item>

		<!-- 下面是调试显示部分 -->
		<!-- <el-form-item>
			<ul>
				<li v-for="(value, key) in litigantForm">{{ key }} : {{ value }}</li>
			</ul>
		</el-form-item> -->
	</el-form>

	<!-- 被告表单 -->
	<el-form
		:model="litigantForm"
		label-width="180px"
		:style="{
			'max-width': '700px',
			'background-color': '#E6F4FF',
		}"
		v-if="litigantForm.litigantPosition === 'defendant'"
	>
		<el-form-item label="是否采取文件导入信息">
			<el-switch
				v-model="litigantForm.litigantInfoByPath"
				active-text="是"
				inactive-text="否"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == true"
			label="被告信息文件路径"
		>
			<el-input
				v-model="litigantForm.litigantInfoPath"
				style="max-width: 500px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="被告名字"
		>
			<el-input
				v-model="litigantForm.litigantName"
				prop="litigantName"
				style="max-width: 300px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="被告身份证号码"
		>
			<el-row width="50" :gutter="50">
				<el-col :span="20">
					<el-input
						v-model="litigantForm.litigantIdNumber"
						style="max-width: 300px"
					/>
				</el-col>
				<el-col :span="4">
					<el-button color="#216CF3" @click="checkIdNumber"
						>校验证件号码</el-button
					>
				</el-col>
			</el-row>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="被告电话号码"
		>
			<el-input
				v-model="litigantForm.litigantPhoneNumber"
				style="max-width: 400px"
			/>
		</el-form-item>

		<el-form-item
			v-if="litigantForm.litigantInfoByPath == false"
			label="被告地址"
		>
			<el-input
				v-model="litigantForm.litigantAddress"
				style="max-width: 400px"
			/>
		</el-form-item>

		<el-form-item>
			<el-row :gutter="60">
				<el-col :span="6">
					<el-button type="success" plain @click="sumbitCurrentlitigantInfo"
						>提交该被告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="danger" plain @click="deleteCurrentlitigantInfo"
						>删除该被告</el-button
					>
				</el-col>
				<el-col :span="6">
					<el-button type="info" plain @click="checkInfo"
						>该功能未完善</el-button
					>
				</el-col>
			</el-row>
		</el-form-item>
	</el-form>
</template>

<script setup>
import {ref, onMounted, inject, onUpdated} from "vue";

import {checkIdNumberValid, checkEnterpriseIdNumberValid} from "../js/check.js";

// 导入按钮图案
// import { check } from 'element-plus/icons';

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
	litigantIsOurClient: false,
	litigantRepresentative: "",
	litigantRepresentativeIdNumber: "",
	id: 0,
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

async function sumbitCurrentlitigantInfo() {
	// 原告
	if (litigantForm.value.litigantPosition === "plaintiff") {
		// 通过文件导入
		if (litigantForm.value.litigantInfoByPath == true) {
			console.log("调用pywebview读取原告信息文件");

			// 用returnData接收pywebview返回的数据，这里的returnData已经被pywebview转换为js对象
			const returnData = await pywebview.api.inputLitigantFromTxt(
				litigantForm.value.litigantInfoPath,
				litigantForm.value.litigantPosition
			);

			// 遍历对象并赋值给litigantForm
			for (let key in returnData) {
				litigantForm.value[key] = returnData[key];
			}

			console.log("文件信息读取完毕，提交了一个原告");
			// 调用父组件的方法将通过文件导入的数据传递给父组件
			getCurrentplaintiffData(litigantForm.value, litigantForm.value.id)
			return;

		// 通过表单直接输入
		} else {
			// 这里要写检验函数
			console.log("表单信息检验无误，提交了一个原告");
			getCurrentplaintiffData(litigantForm.value, litigantForm.value.id);
			return;
		}

		// 被告
	} else {
		// 通过文件导入
		if (litigantForm.value.litigantInfoByPath == true) {
			console.log("调用pywebview读取被告信息文件");
			// 用returnData接收pywebview返回的数据，这里的returnData已经被pywebview转换为js对象
			const returnData = await pywebview.api.inputLitigantFromTxt(
				litigantForm.value.litigantInfoPath,
				litigantForm.value.litigantPosition
			);

			// 遍历对象并赋值给litigantForm
			for (let key in returnData) {
				litigantForm.value[key] = returnData[key];
			}

			console.log("文件信息读取完毕，提交了一个被告");
			// 调用父组件的方法将通过文件导入的数据传递给父组件
			getCurrentDefendantData(litigantForm.value, litigantForm.value.id);
			return


		// 通过表单直接输入
		} else {
			// 这里要写检验函数
			console.log("提交了一个被告");
			getCurrentDefendantData(litigantForm.value, litigantForm.value.id);
			return;
		}
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
