<template>
	<!-- 原告表单 -->
	<div
		v-if="
			litigantForm.litigantPosition === 'plaintiff' &&
			showDescriptionListAndHideForm == false
		"
	>
		<el-card
			shadow="never"
			:style="{'margin-top': '10px', 'margin-bottom': '10px'}"
		>
			<el-form
				:model="litigantForm"
				label-width="180px"
				:style="{
					'max-width': '700px',
					// 'background-color': '#FFEEBB',
				}"
			>
				<el-form-item label="是否采取文件导入信息">
					<el-switch
						v-model="getInfoByPath"
						style="
							--el-switch-on-color: #ffc105;
							--el-switch-off-color: #c4c4c4;
						"
						active-text="是"
						inactive-text="否"
					/>
				</el-form-item>

				<el-form-item v-if="getInfoByPath == true" label="原告信息文件路径">
					<el-input
						v-model="litigantForm.litigantInfoPath"
						style="max-width: 500px"
					/>
				</el-form-item>

				<div v-if="getInfoByPath == false">
					<el-form-item label="是否我方">
						<el-switch
							v-model="litigantForm.isOurClient"
							active-text="是"
							inactive-text="否"
						/>
					</el-form-item>

					<el-form-item label="原告名字">
						<el-input
							v-model="litigantForm.litigantName"
							prop="litigantName"
							style="max-width: 300px"
						/>
					</el-form-item>

					<el-form-item label="原告身份证号码">
						<el-row width="70" :gutter="50">
							<el-col :span="20">
								<el-input
									v-model="litigantForm.litigantIdCode"
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

					<el-form-item label="原告电话号码">
						<el-input
							v-model="litigantForm.litigantPhoneNumber"
							style="max-width: 400px"
						/>
					</el-form-item>

					<el-form-item label="原告地址">
						<el-input
							v-model="litigantForm.litigantAddress"
							style="max-width: 400px"
						/>
					</el-form-item>

					<div v-if="litigantForm.litigantType == 'Company'">
						<el-form-item label="法定代表人姓名">
							<el-input
								v-model="litigantForm.legalRepresentative"
								style="max-width: 300px"
							/>
						</el-form-item>

						<el-form-item label="法定代表人身份证号码">
							<el-row width="50" :gutter="50">
								<el-col :span="20">
									<el-input
										v-model="litigantForm.legalRepresentativeIdCode"
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
					</div>
				</div>

				<el-form-item>
					<el-button
						type="success"
						plain
						@click="sumbitCurrentlitigantInfo"
						style="margin-right: 15px"
						>提交</el-button
					>

					<el-button
						type="danger"
						plain
						@click="deleteCurrentlitigantInfo"
						style="margin-right: 15px"
						>删除</el-button
					>
				</el-form-item>

				<!-- 下面是调试显示部分 -->
				<!-- <el-form-item>
			<ul>
				<li v-for="(value, key) in litigantForm">{{ key }} : {{ value }}</li>
			</ul>
		</el-form-item> -->
			</el-form>
		</el-card>
	</div>

	<!-- 被告表单 -->
	<div
		v-if="
			litigantForm.litigantPosition === 'defendant' &&
			showDescriptionListAndHideForm == false
		"
	>
		<el-card
			shadow="hover"
			:style="{'margin-top': '10px', 'margin-bottom': '10px'}"
		>
			<el-form
				:model="litigantForm"
				label-width="180px"
				:style="{
					'max-width': '700px',
					// 'background-color': '#E6F4FF',
				}"
			>
				<el-form-item label="是否采取文件导入信息">
					<el-switch
						v-model="getInfoByPath"
						active-text="是"
						inactive-text="否"
					/>
				</el-form-item>

				<el-form-item v-if="getInfoByPath == true" label="被告信息文件路径">
					<el-input
						v-model="litigantForm.litigantInfoPath"
						style="max-width: 500px"
					/>
				</el-form-item>

				<div v-if="getInfoByPath == false">
					<el-form-item label="是否我方">
						<el-switch
							v-model="litigantForm.isOurClient"
							active-text="是"
							inactive-text="否"
						/>
					</el-form-item>

					<el-form-item label="被告名字">
						<el-input
							v-model="litigantForm.litigantName"
							prop="litigantName"
							style="max-width: 300px"
						/>
					</el-form-item>

					<el-form-item label="被告身份证号码">
						<el-row width="50" :gutter="50">
							<el-col :span="20">
								<el-input
									v-model="litigantForm.litigantIdCode"
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

					<el-form-item label="被告电话号码">
						<el-input
							v-model="litigantForm.litigantPhoneNumber"
							style="max-width: 400px"
						/>
					</el-form-item>

					<el-form-item label="被告地址">
						<el-input
							v-model="litigantForm.litigantAddress"
							style="max-width: 400px"
						/>
					</el-form-item>

					<div v-if="litigantForm.litigantType == 'Company'">
						<el-form-item label="法定代表人姓名">
							<el-input
								v-model="litigantForm.legalRepresentative"
								style="max-width: 300px"
							/>
						</el-form-item>

						<el-form-item label="法定代表人身份证号码">
							<el-row width="50" :gutter="50">
								<el-col :span="20">
									<el-input
										v-model="litigantForm.legalRepresentativeIdCode"
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
					</div>
				</div>

				<el-form-item>
					<el-button
						type="success"
						plain
						@click="sumbitCurrentlitigantInfo"
						style="margin-right: 15px"
						>提交</el-button
					>

					<el-button
						type="danger"
						plain
						@click="deleteCurrentlitigantInfo"
						style="margin-right: 15px"
						>删除</el-button
					>
				</el-form-item>
			</el-form>
		</el-card>
	</div>

	<!-- 下面是提交完成以后显示原被告信息部分 -->

	<!-- 原告部分 -->
	<div
		v-if="
			litigantForm.litigantPosition === 'plaintiff' &&
			showDescriptionListAndHideForm == true
		"
	>
		<el-card :style="{'margin-top': '10px', 'margin-bottom': '10px'}">
			<el-descriptions
				title="原告信息"
				:column="1"
				border
				:style="{
					'margin-top': '20px',
					'margin-bottom': '20px',
				}"
			>
				<el-descriptions-item label="原告名称">{{
					litigantForm.litigantName
				}}</el-descriptions-item>
				<el-descriptions-item label="原告证件号码">{{
					litigantForm.litigantIdCode
				}}</el-descriptions-item>
				<el-descriptions-item label="原告电话号码">{{
					litigantForm.litigantPhoneNumber
				}}</el-descriptions-item>
				<el-descriptions-item label="原告地址">{{
					litigantForm.litigantAddress
				}}</el-descriptions-item>
				<el-descriptions-item label="是否我方">{{
					isOurClientMessage
				}}</el-descriptions-item>
				<el-descriptions-item label="原告类型">{{
					litigantTypeMessage
				}}</el-descriptions-item>
				<el-descriptions-item
					v-if="litigantForm.litigantType == 'Company'"
					label="原告法定代表人姓名"
					>{{ litigantForm.legalRepresentative }}</el-descriptions-item
				>
				<el-descriptions-item
					v-if="litigantForm.litigantType == 'Company'"
					label="原告法定代表人身份证号码"
					>{{ litigantForm.legalRepresentativeIdCode }}</el-descriptions-item
				>
			</el-descriptions>

			<el-button
				type="danger"
				plain
				@click="showDescriptionListAndHideForm = false"
				>编辑与删除</el-button
			>
		</el-card>
	</div>

	<!-- 被告部分 -->
	<div
		v-if="
			litigantForm.litigantPosition === 'defendant' &&
			showDescriptionListAndHideForm == true
		"
	>
		<el-card
			:style="{
				'margin-top': '10px',
				'margin-bottom': '10px',
			}"
		>
			<el-descriptions
				title="被告信息"
				:column="1"
				border
				:style="{
					'margin-top': '20px',
					'margin-bottom': '20px',
				}"
			>
				<el-descriptions-item label="被告名称">{{
					litigantForm.litigantName
				}}</el-descriptions-item>
				<el-descriptions-item label="被告证件号码">{{
					litigantForm.litigantIdCode
				}}</el-descriptions-item>
				<el-descriptions-item label="被告电话号码">{{
					litigantForm.litigantPhoneNumber
				}}</el-descriptions-item>
				<el-descriptions-item label="被告地址">{{
					litigantForm.litigantAddress
				}}</el-descriptions-item>
				<el-descriptions-item label="是否我方">{{
					isOurClientMessage
				}}</el-descriptions-item>
				<el-descriptions-item label="被告类型">{{
					litigantTypeMessage
				}}</el-descriptions-item>
				<el-descriptions-item
					v-if="litigantForm.litigantType == 'Company'"
					label="被告法定代表人姓名"
					>{{ litigantForm.legalRepresentative }}</el-descriptions-item
				>
				<el-descriptions-item
					v-if="litigantForm.litigantType == 'Company'"
					label="被告法定代表人身份证号码"
					>{{ litigantForm.legalRepresentativeIdCode }}</el-descriptions-item
				>
			</el-descriptions>

			<el-button
				type="danger"
				plain
				@click="showDescriptionListAndHideForm = false"
				>编辑与删除</el-button
			>
		</el-card>
	</div>
</template>

<script setup>
import {checkIdNumberValid, checkEnterpriseIdNumberValid} from "../js/check.js";

// 从父组件中获取方法
const reducePlaintiff = inject("reducePlaintiff");
const reduceDefendant = inject("reduceDefendant");
const getCurrentplaintiffData = inject("getCurrentplaintiffData");
const getCurrentDefendantData = inject("getCurrentDefendantData");

const props = defineProps({
	litigant: Object,
	showDescriptionList: Boolean,
});

const litigantForm = ref({});

const getInfoByPath = ref(false);

const showDescriptionListAndHideForm = ref(null);


const isOurClientMessage = computed(() => {
	if (litigantForm.value.isOurClient == true) {
		return "是";
	} else {
		return "否";
	}
});

const litigantTypeMessage = computed(() => {
	if (litigantForm.value.litigantType == "Company") {
		return "法人";
	} 
	else if (litigantForm.value.litigantType == "Person") {
		return "自然人";
	}
	else {
		return "非法人组织";
	}
});

// 检查身份证号码是否合法
function checkIdNumber() {
	let result = checkIdNumberValid(litigantForm.value.litigantIdCode);
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
			getCurrentplaintiffData(litigantForm.value, litigantForm.value.id);

			// 隐藏表单，显示描述列表
			showDescriptionListAndHideForm.value = true;

			return;

			// 通过表单直接输入
		} else {
			// 这里要写检验函数
			console.log("表单信息检验无误，提交了一个原告");
			getCurrentplaintiffData(litigantForm.value, litigantForm.value.id);

			// 隐藏表单，显示描述列表
			showDescriptionListAndHideForm.value = true;
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

			// 隐藏表单，显示描述列表
			showDescriptionListAndHideForm.value = true;
			return;

			// 通过表单直接输入
		} else {
			// 这里要写检验函数
			console.log("提交了一个被告");
			getCurrentDefendantData(litigantForm.value, litigantForm.value.id);

			// 隐藏表单，显示描述列表
			showDescriptionListAndHideForm.value = true;
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
	// 赋值
	litigantForm.value.litigantName = props.litigant.litigantName;
	litigantForm.value.litigantIdCode = props.litigant.litigantIdCode;
	litigantForm.value.litigantPhoneNumber = props.litigant.litigantPhoneNumber;
	litigantForm.value.litigantAddress = props.litigant.litigantAddress;
	litigantForm.value.litigantPosition = props.litigant.litigantPosition;
	litigantForm.value.legalRepresentative = props.litigant.legalRepresentative;
	litigantForm.value.legalRepresentativeIdCode =
		props.litigant.legalRepresentativeIdCode;
	litigantForm.value.litigantType = props.litigant.litigantType;
	litigantForm.value.isOurClient = props.litigant.isOurClient;
	litigantForm.value.id = props.litigant.id;

	showDescriptionListAndHideForm.value = props.showDescriptionList;
});

// 将litigantForm暴露给父组件
defineExpose({
	litigantForm,
});
</script>
