<script setup>
import { ref, provide, onMounted, onUpdated,watchEffect} from "vue";

// 局部注册LitigantForm组件
import LitigantForm from "./LitigantForm.vue";

// 当事人表单实例（原告）
const litigantFormPlaintiff = ref(null);
// 当事人表单实例（被告）
const litigantFormDefendant = ref(null);

// 定义表单数据
const caseForm = ref({
	caseId: "", //案件ID

	caseCourtCode: "", //法院案号
	causeOfAction: "", //案由
	litigationAmount: "", //标的额
	caseAgentStage: [], //委托阶段
	caseType: 0, //案件类型
	courtName: "", //管辖法院
	mediationIntention: false, //调解意愿
	caseFolderGeneratedPath: "", //案件文件夹生成路径

	riskAgentStatus: true, //风险收费
	riskAgentUpfrontFee: "", //前期风险收费金额
	riskAgentPostFeeRate: "", //后期风险收费比例

	factAndReason: "", //事实与理由
	claimText: "", //诉讼请求
	rejectMediationReasonText: "", //拒绝调解理由

	plaintiffs: [], //原告列表
	defendants: [], //被告列表

	inputCaseInfoByFilePath: "", //案件信息文件路径（用于文件导入模式）
});

const componentsConfig = ref({
	inputInfoByFile: true,
	inputCaseInfoByFilePathDisabled: false,
	inputInfoByFileSwitchStatus: true,
});

// 表单引用
const caseFormRef = ref(null);
// 通过前端输入案件信息的输入框是否启用的状态，初始为false，即采用文件导入模式
const inputInfoByFrontEndStatus = ref(false);

// 设定表单的校验规则
const caseFormRules = ref({
	caseCourtCode: [{ required: true, message: "请输入法院案号", trigger: "blur" }],
	causeOfAction: [{ required: true, message: "请输入案由", trigger: "blur" }],
	litigationAmount: [
		{ required: true, message: "请输入标的额", trigger: "blur" },
		{ type: "number", message: "请输入数字", trigger: "blur" },
	],
	riskAgentUpfrontFee: [
		{ required: true, message: "请输入前期风险收费金额", trigger: "blur" },
	],
	riskAgentPostFeeRate: [
		{ required: true, message: "请输入后期风险收费比例", trigger: "blur" },
	],
	caseAgentStage: [
		{ required: true, message: "请选择委托阶段", trigger: "change" },
	],
	caseType: [{ required: true, message: "请选择案件类型", trigger: "change" }],
	courtName: [{ required: true, message: "请输入管辖法院", trigger: "blur" }],
	claimText: [{ required: true, message: "请输入诉讼请求", trigger: "blur" }],
	factAndReason: [
		{ required: true, message: "请输入事实与理由", trigger: "blur" },
	],
	rejectMediationReasonText: [
		{ required: true, message: "请输入拒绝调解理由", trigger: "blur" },
	],
	caseFolderGeneratedPath: [
		{ required: true, message: "请输入案件文件夹生成路径", trigger: "blur" },
	],
});



// 接收父组件传递的方法
const propData = defineProps({
	propCaseData: Object,
	propMode: String,
})


// 向父组件传递数据的事件
const emit = defineEmits([
	"updateCaseData"
]) 



// 监听案件信息的输入方式是否发生变化，文件/前端输入
function ChangeInputStatus() {
	if (componentsConfig.value.inputInfoByFile == true) {
		inputInfoByFrontEndStatus.value = false;
		console.log("关闭前端输入信息模式，开启文件读入模式");
		// 重置文本框状态
		componentsConfig.value.inputCaseInfoByFilePathDisabled = false;
		caseForm.value.inputCaseInfoByFilePath = "";
		componentsConfig.value.inputInfoByFile = true;
	} else {
		// 启用其他输入框
		inputInfoByFrontEndStatus.value = true;
		console.log("关闭文件读入模式，开启前端输入信息模式");
		componentsConfig.value.inputInfoByFile = false;
	}
}

// ====== 下面是和子组件【案件当事人信息表单】相关的方法 ======

// 新增原告方法
function onAddPlaintiff() {
	caseForm.value.plaintiffs.push({
		litigantName: "",
		litigantIdNumber: "",
		litigantPhoneNumber: "",
		litigantPosition: "plaintiff",
		id: Date.now()
	});
	console.log("新增了一个原告");
}

// 新增被告方法
function onAddDefendant() {
	caseForm.value.defendants.push({
		litigantName: "",
		litigantIdNumber: "",
		litigantPhoneNumber: "",
		litigantPosition: "defendant",
		id: Date.now()
	});
	console.log("新增了一个被告");
}

// 删除原告方法
function reducePlaintiff(id) {
	console.log("当前原告的id为" + id);
	// 在原告列表中找到该原告的位置
	var index = caseForm.value.plaintiffs.findIndex((plaintiff) => plaintiff.id === id);
	caseForm.value.plaintiffs.splice(index, 1);
}

// 删除被告方法
function reduceDefendant(id) {
	console.log("当前被告的id为" + id);
	// 在被告列表中找到该被告的位置
	var index = caseForm.value.defendants.findIndex((defendant) => defendant.id === id);
	caseForm.value.defendants.splice(index, 1);
}

const getCurrentplaintiffData = (plaintiffData, id) => {
	// 在原告列表中找到该原告的序号，并保存到index中
	var index = caseForm.value.plaintiffs.findIndex((plaintiff) => plaintiff.id === id)
	// 赋值
	caseForm.value.plaintiffs[index].litigantName = plaintiffData.litigantName;
	caseForm.value.plaintiffs[index].litigantIdNumber = plaintiffData.litigantIdNumber;
	caseForm.value.plaintiffs[index].litigantPhoneNumber = plaintiffData.litigantPhoneNumber;
};

const getCurrentDefendantData = (defendantData, id) => {
	// console.log(defendantData);
	// 在被告列表中找到该被告的位置
	var index = caseForm.value.defendants.findIndex((defendant) => defendant.id === id);
	// console.log("当前被告的位置为" + index);

	// 赋值
	caseForm.value.defendants[index].litigantName = defendantData.litigantName;
	caseForm.value.defendants[index].litigantIdNumber = defendantData.litigantIdNumber;
	caseForm.value.defendants[index].litigantPhoneNumber = defendantData.litigantPhoneNumber;
};

// 将该方法提供给子组件
provide("reducePlaintiff", reducePlaintiff);
provide("reduceDefendant", reduceDefendant);
provide("getCurrentplaintiffData", getCurrentplaintiffData);
provide("getCurrentDefendantData", getCurrentDefendantData);

// ====== 下面是和webview的交互部分的方法 ======

// 选中“选择文件按钮”,调用后端python来弹出文件选择框
async function promptFileSelection() {
	console.log("选择文件按钮");
	// 判断是否有pywebview对象
	if (typeof pywebview === "undefined") {
		console.log("未链接到后端");
		return;
	}
	// 调用后端的方法，弹出文件选择框
	else {
		caseForm.value.inputCaseInfoByFilePath =
			await pywebview.api.GetFilepath();
		// 读取完毕以后禁用文本框
		componentsConfig.value.inputCaseInfoByFilePathDisabled = true;
	}

}

// 提交案件信息到后端的方法
function onSubmit() {
	// 先判断目前是采取何种形式提交信息

	// 如果采取的是文件上传
	if (componentsConfig.value.inputInfoByFile == true) {
		console.log("onSubmit()：当前导入模式为-从文件中导入案件信息");
		// 将案件信息传递给父组件
		emit("updateCaseData", caseForm.value);

		// 判断是否有pywebview对象，如果有则将案件信息的字典传递给后端，如果没有就提示未链接到后端
		if (typeof pywebview === "undefined") {
			console.log("onSubmit()：未链接到后端");
			return;
		}
		else {
			// 如果是文件路径输入模式，则将文件的路径以及文件夹生成路径传递给后端
			pywebview.api.inputCaseFromTxt(caseForm.value.inputCaseInfoByFilePath); //关于pywebview的部分在组合前后端的时候再使用
			return;
		}

	}

	// 如果采取的是前端输入
	else {
		console.log("onSubmit()：当前导入模式为-从前端表单中导入案件信息");
		// 先校验表单
		caseFormRef.value.validate((valid) => {
			if (valid) {	//如果表单校验通过
				console.log("onSubmit()：表单校验通过");
				// 遍历原告列表，将原告的名字连接为一个字符串
				let plaintiffsName = "";
				for (let i = 0; i < caseForm.value.plaintiffs.length; i++) {
					plaintiffsName += caseForm.value.plaintiffs[i].litigantName + "、";
				}
				// 去掉最后一个顿号
				plaintiffsName = plaintiffsName.substring(0, plaintiffsName.length - 1);

				// 遍历被告列表，将被告的名字连接为一个字符串
				let defendantsName = "";
				for (let i = 0; i < caseForm.value.defendants.length; i++) {
					defendantsName += caseForm.value.defendants[i].litigantName + "、";
				}
				// 去掉最后一个顿号
				defendantsName = defendantsName.substring(0, defendantsName.length - 1);

				// 将原告和被告的名字赋值给案件信息的字典
				caseForm.value.litigantsName = plaintiffsName + " 诉 " + defendantsName;

				// 将案件信息的字典传递给父组件
				emit("updateCaseData", caseForm.value);

				// 判断是否有pywebview对象，如果有则将案件信息的字典传递给后端，如果没有就提示未链接到后端
				if (typeof pywebview === "undefined") {
					console.log("onSubmit()：未链接到后端");
					return;
				}
				else {
					// 将案件信息的字典传递给后端
					pywebview.api.inputCaseFromFrontEndForm(caseForm.value);
					return;
				}

			} else {
				console.log("onSubmit()：表单校验失败");
				return;
			}
		});
	}
}


function caseFormInfoInitiation(propData) {

	// 已有案件内容以后的编辑模式
	if (propData.propMode == "edit") {
		console.log("当前CaseInfoform为编辑模式")

		if (propData.propCaseData == null) {
			console.log("没有传递过来案件信息");
			return;
		}
		// 如果有传递过来的案件信息，则将其赋值给表单
		let caseData = propData.propCaseData

		console.log(caseData);
		caseForm.value.caseId = caseData.caseId;
		caseForm.value.caseCourtCode = caseData.caseCourtCode
		caseForm.value.causeOfAction = caseData.causeOfAction;
		caseForm.value.litigationAmount = caseData.litigationAmount;
		caseForm.value.caseAgentStage = caseData.caseAgentStage;
		caseForm.value.caseType = caseData.caseType.toString();
		caseForm.value.courtName = caseData.courtName;
		caseForm.value.mediationIntention = caseData.mediationIntention;
		caseForm.value.caseFolderGeneratedPath = caseData.caseFolderGeneratedPath;
		caseForm.value.riskAgentStatus = caseData.riskAgentStatus;
		
		// 如果原告不为空，则将其赋值给表单
		if (caseData.plaintiffs != null) {
			caseForm.value.plaintiffs = caseData.plaintiffs;
		}
		// 如果被告不为空，则将其赋值给表单
		if (caseData.defendants != null) {
			caseForm.value.defendants = caseData.defendants;

		}

		// 如果风险代理人状态为true，则将风险代理人的前期风险收费金额和后期风险收费比例赋值给表单
		if (caseData.riskAgentStatus == true) {
			caseForm.value.riskAgentUpfrontFee = caseData.riskAgentUpfrontFee;
			caseForm.value.riskAgentPostFeeRate = caseData.riskAgentPostFeeRate;
		} else {
			caseForm.value.riskAgentUpfrontFee = "";
			caseForm.value.riskAgentPostFeeRate = "";
		}

		caseForm.value.factAndReason = caseData.factAndReason;
		caseForm.value.claimText = caseData.claimText;
		caseForm.value.rejectMediationReasonText = caseData.rejectMediationReasonText;

		// 因为是编辑模式，所以不显示文件导入模式的开关
		componentsConfig.value.inputInfoByFileSwitchStatus = false;
		// 因为是编辑模式，所以默认打开前端输入状态
		inputInfoByFrontEndStatus.value = true;
		// 因为是编辑模式，所以默认不需要文件导入
		componentsConfig.value.inputInfoByFile = false;

		// console.log("案件信息已经传递过来了");
		// console.log(caseForm.value);
	}

	// 新建案件的创建模式
	else if  (propData.propMode == "create") {
		console.log("当前CaseInfoform为新建案件模式")

		// 因为是新建模式，因此显示文件导入模式的开关
		componentsConfig.value.inputInfoByFileSwitchStatus = true;
		// 因为是编辑模式，所以默认关闭前端输入状态，
		inputInfoByFrontEndStatus.value = false;
		// 因为是编辑模式，所以默认需要文件导入
		componentsConfig.value.inputInfoByFile = true;

		// 所有信息回归初始值（似乎引起了bug）
		caseForm.value.caseId = "";
		caseForm.value.caseCourtCode = "";
		caseForm.value.causeOfAction = "";
		caseForm.value.litigationAmount = "";
		caseForm.value.caseAgentStage = [];
		caseForm.value.caseType = "";
		caseForm.value.courtName = "";
		caseForm.value.mediationIntention = true;
		caseForm.value.caseFolderGeneratedPath = "";
		caseForm.value.riskAgentStatus = false;

		caseForm.value.riskAgentUpfrontFee = "";
		caseForm.value.riskAgentPostFeeRate = "";

		caseForm.value.factAndReason = "";
		caseForm.value.claimText = "";
		caseForm.value.rejectMediationReasonText = "";

		caseForm.value.plaintiffs = [];
		caseForm.value.defendants = [];

	}
}

// ====== 下面是在挂载时调用的方法 ======
onMounted(() => {
	caseFormInfoInitiation(propData);
});

// ====== 下面是在更新时调用的方法 ======
watchEffect(() => {
	console.log("案件信息表单已经更新");
	caseFormInfoInitiation(propData);
});

</script>

<template>
	<el-form v-bind:model="caseForm" v-bind:rules="caseFormRules" label-width="150" style="max-width: 700px"
		ref="caseFormRef">


		<el-form-item>
			<el-button type="primary" plain @click="onAddPlaintiff">新增原告</el-button>
			<el-button type="info" plain @click="onAddDefendant">新增被告</el-button>
			<el-button type="danger" @click="onSubmit(ruleFormRef)">提交案件信息</el-button>
		</el-form-item>

		<el-form-item v-if="componentsConfig.inputInfoByFileSwitchStatus" label="文件导入模式">
			<el-switch @change="ChangeInputStatus" v-model="componentsConfig.inputInfoByFile" />
		</el-form-item>

		<el-form-item v-if="!inputInfoByFrontEndStatus" label="案件信息文件路径">
			<el-input v-model="caseForm.inputCaseInfoByFilePath"
				:disabled="componentsConfig.inputCaseInfoByFilePathDisabled" placeholder="仅支持txt文件和xlsx文件"
				style="max-width: 300px" />
			<el-button v-if="!inputInfoByFrontEndStatus" @click="promptFileSelection">选择文件
			</el-button>
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="法院案号" prop="caseCourtCode">
			<el-input v-model.trim="caseForm.caseCourtCode" style="width: 240px" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="案由" prop="causeOfAction">
			<el-input v-model.trim="caseForm.causeOfAction" style="width: 240px" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="标的额" prop="litigationAmount">
			<el-input v-model.number="caseForm.litigationAmount" placeholder="计价单位：人民币元" style="width: 240px" />
		</el-form-item>

		<el-row>
			<el-col :span="12">
				<el-form-item v-if="inputInfoByFrontEndStatus" label="风险收费">
					<el-switch v-model="caseForm.riskAgentStatus" />
				</el-form-item>
			</el-col>
			<el-col :span="12">
				<el-form-item v-if="inputInfoByFrontEndStatus" label="调解意愿">
					<el-switch v-model="caseForm.mediationIntention" />
				</el-form-item>
			</el-col>
		</el-row>

		<el-row>
			<el-col :span="12">
				<el-form-item v-if="inputInfoByFrontEndStatus" label="前期风险收费金额" prop="riskAgentUpfrontFee">
					<el-input v-model.number="caseForm.riskAgentUpfrontFee" />
				</el-form-item>
			</el-col>
			<el-col :span="12">
				<el-form-item v-if="inputInfoByFrontEndStatus" label="后期风险收费比例" prop="riskAgentPostFeeRate">
					<el-input v-model.number="caseForm.riskAgentPostFeeRate" />
				</el-form-item>
			</el-col>
		</el-row>

		<el-form-item v-if="inputInfoByFrontEndStatus">
			委托阶段：
			<el-checkbox-group v-model="caseForm.caseAgentStage" id="caseAgentStage">
				<el-checkbox value="1" name="type"> 一审立案阶段 </el-checkbox>
				<el-checkbox value="2" name="type"> 一审开庭阶段 </el-checkbox>
				<el-checkbox value="3" name="type"> 二审阶段 </el-checkbox>
				<el-checkbox value="4" name="type"> 执行阶段 </el-checkbox>
				<el-checkbox value="5" name="type"> 再审阶段 </el-checkbox>
			</el-checkbox-group>
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus">
			案件类型：
			<el-radio-group v-model="caseForm.caseType" id="caseType">
				<el-radio value="1">民事案件</el-radio>
				<el-radio value="2">行政案件</el-radio>
				<el-radio value="3">执行案件</el-radio>
			</el-radio-group>
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="管辖法院" prop="courtName">
			<el-input v-model="caseForm.courtName" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="诉讼请求" prop="claimText">
			<el-input v-model="caseForm.claimText" type="textarea" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="事实与理由" prop="factAndReason">
			<el-input v-model="caseForm.factAndReason" type="textarea" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="拒绝调解理由">
			<el-input v-model="caseForm.rejectMediationReasonText" type="textarea" />
		</el-form-item>

		<el-form-item v-if="inputInfoByFrontEndStatus" label="案件文件夹生成路径" prop="caseFolderGeneratedPath">
			<el-input v-model="caseForm.caseFolderGeneratedPath" style="max-width: 400px" />
		</el-form-item>

	</el-form>

	<!-- 当事人表格组件 -->

	<!-- 原告部分 -->
	<div v-for="plaintiff in caseForm.plaintiffs" :key="plaintiff.id">
		<LitigantForm ref="litigantFormPlaintiff" :litigant="plaintiff"  />
	</div>

	<!-- 被告部分 -->
	<div v-for="defendant in caseForm.defendants" :key="defendant.id">
		<LitigantForm ref="litigantFormDefendant" :litigant="defendant"  />
	</div>

	<!-- 下面的是用于测试，直接展示从表格中输入的数据 -->
	<div>
		<ul>
			<p>案件信息</p>
			<li v-for="(item, key) in caseForm">{{ key }} - {{ item }}</li>
		</ul>
	</div>
</template>


<style>
/* 展示信息表格的css */
.cell-item {
	display: flex;
	align-items: center;
}

.margin-top {
	margin-top: 20px;
}

.el-descriptions {
	margin-top: 20px;
}
</style>
