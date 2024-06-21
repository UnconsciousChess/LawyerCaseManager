<!-- 组合式Vue -->
<script setup>
import { ref, onMounted , reactive, onUpdated,onBeforeUpdate,nextTick} from 'vue'


// 局部注册LitigantForm组件
import LitigantForm from './LitigantForm.vue'


// 定义表单数据
const caseForm = ref({
	caseCourtCode: "",
	causeOfAction: "",
	litigationAmount: "",
	riskAgentStatus: true,
	riskAgentUpfrontFee: "",
	riskAgentPostFeeRate: "",
	caseAgentStage: [],
	caseType: 0,
	courtName: "",
	mediationIntention: false,
	factAndReason: "",
	caseFolderGeneratedPath: "",
	claimText: "",
	rejectMediationReasonText: "",
    plaintiffs: [],
    defendants: [],
    inputInfoByTxt: false,
    inputCaseInfoByTxtPath: "",
});

// ===下面是定义的变量 ===
// 表单引用
const caseFormRef = ref(null);
//  通过txt文件导入案件信息的输入框是否禁用的状态
const inputInfoByTxtDisableStatus = ref(true);
// 通过前端输入案件信息的输入框是否禁用的状态（和通过txt文件导入的状态相反）
const inputInfoByFrontEndStatus = ref(false);


// 设定表单的校验规则
const caseFormRules = ref({
	caseCourtCode: [
		{ required: true, message: "请输入法院案号", trigger: "blur" },
	],
	causeOfAction: [
		{ required: true, message: "请输入案由", trigger: "blur" },
	],
	litigationAmount: [
		{ required: true, message: "请输入标的额", trigger: "blur" },
        { type: "number", message: "请输入数字", trigger: "blur"},
   
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
	caseType: [
		{ required: true, message: "请选择案件类型", trigger: "change" },
	],
	courtName: [
		{ required: true, message: "请输入管辖法院", trigger: "blur" },
	],
	claimText: [
		{ required: true, message: "请输入诉讼请求", trigger: "blur" },
	],
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



onUpdated(

    // 监听案件信息的输入方式是否发生变化
    function ChangeInputStatus()  {
        if (caseForm.value.inputInfoByTxt == true) {
            inputInfoByTxtDisableStatus.value = false;
            inputInfoByFrontEndStatus.value = true;
            console.log("启用了输入框")
        }
        else {
            // 将txt输入框禁用，其他输入框启用
            inputInfoByTxtDisableStatus.value = true;
            inputInfoByFrontEndStatus.value = false;
            console.log("禁用了输入框")
        }
    }
)



// 提交案件信息函数
function onSubmit() {
    // 先判断目前是采取何种形式上传

    // 如果采取的是txt文件上传
    if (caseForm.value.inputInfoByTxt == true) {
        console.log("从txt文件中导入案件信息");
        // console.log(caseForm.value.inputCaseInfoByTxtPath);
        // 将txt文件的路径以及文件夹生成路径传递给后端
        pywebview.api.inputFromTxt(caseForm.value.inputCaseInfoByTxtPath);   //关于pywebview的部分在组合前后端的时候再使用 
        return
    }
    // 如果采取的是前端输入
    else {
        // 则先校验表单
        caseFormRef.value.validate((valid) => {
            if (valid) {
                console.log("表单校验通过");
                // 将案件信息的字典传递给后端
                pywebview.api.inputFromFrontEndForm(caseForm.value);   //关于pywebview的部分在组合前后端的时候再使用
                return true;
            } 
            else {
                console.log("表单校验失败");
                return false;
            }
        })
    }
}

// 新增原告方法
const onAddPlaintiff = () => {
    caseForm.value.plaintiffs.push({
        litigantName: "",
        litigantIdNumber: "",
        litigantPhoneNumber: "",
        litigantInfoPath: "",
        litigantPosition: "plaintiff",

    });
	console.log("新增了一个原告");
}

// 新增被告方法
function onAddDefendant() {
    caseForm.value.defendants.push({
        litigantName: "",
        litigantIdNumber: "",
        litigantPhoneNumber: "",
        litigantInfoPath: "",
        litigantPosition: "defendant",
    });
	console.log("新增了一个被告");
}

// 输出案件信息到excel的方法
function outputToExcel() {
    console.log("输出案件信息到excel");
    pywebview.api.OutputCaseInfoToExcel(caseForm.value.caseFolderGeneratedPath);   
}

// 输出案件信息到txt文本的方法
function outputToTxt() {
    console.log("输出案件信息到txt文本");
    pywebview.api.OutputCaseInfoToTxt(caseForm.value.caseFolderGeneratedPath);   
}

</script>

<template>
    <el-form
        v-bind:model="caseForm"
        v-bind:rules="caseFormRules"
        label-width="auto"
        style="max-width: 700px"
        ref="caseFormRef"
    >
        <el-form-item label="法院案号" prop="caseCourtCode">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model.trim="caseForm.caseCourtCode" />
        </el-form-item>

        <el-form-item label="案由" prop="causeOfAction">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model.trim="caseForm.causeOfAction" />
        </el-form-item>

        <el-form-item label="标的额" prop="litigationAmount">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model.number="caseForm.litigationAmount" />
        </el-form-item>

        <el-row>
            <el-col :span="12">
                <el-form-item label="风险收费" >
                    <el-switch :disabled="inputInfoByFrontEndStatus" v-model="caseForm.riskAgentStatus" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="调解意愿">
                    <el-switch v-model="caseForm.mediationIntention" />
                </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="12">
                <el-form-item label="前期风险收费金额" prop="riskAgentUpfrontFee">
                    <el-input :disabled="inputInfoByFrontEndStatus" v-model.number="caseForm.riskAgentUpfrontFee" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="后期风险收费比例" prop="riskAgentPostFeeRate">
                    <el-input :disabled="inputInfoByFrontEndStatus" v-model.number="caseForm.riskAgentPostFeeRate" />
                </el-form-item>
            </el-col>
        </el-row>

        <el-form-item>
            委托阶段：
            <el-checkbox-group
                v-model="caseForm.caseAgentStage"
                id="caseAgentStage"
                :disabled="inputInfoByFrontEndStatus"
            >
                <el-checkbox value=1 name="type"> 一审立案阶段 </el-checkbox>
                <el-checkbox value=2 name="type"> 一审开庭阶段 </el-checkbox>
                <el-checkbox value=3 name="type"> 二审阶段 </el-checkbox>
                <el-checkbox value=4 name="type"> 执行阶段 </el-checkbox>
                <el-checkbox value=5 name="type"> 再审阶段 </el-checkbox>
            </el-checkbox-group>
        </el-form-item>

        <el-form-item>
            案件类型：
            <el-radio-group 
                v-model="caseForm.caseType" 
                id="caseType"
                :disabled="inputInfoByFrontEndStatus"
            >
                <el-radio value=1>民事案件</el-radio>
                <el-radio value=2>行政案件</el-radio>
                <el-radio value=3>执行案件</el-radio>
            </el-radio-group>
        </el-form-item>

        <el-form-item label="管辖法院" prop="courtName">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model="caseForm.courtName" />
        </el-form-item>

        <el-form-item label="诉讼请求" prop="claimText">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model="caseForm.claimText" type="textarea" />
        </el-form-item>

        <el-form-item label="事实与理由" prop="factAndReason">
            <el-input :disabled="inputInfoByFrontEndStatus" v-model="caseForm.factAndReason" type="textarea" />
        </el-form-item>

        <el-form-item label="拒绝调解理由">
            <el-input
                :disabled="inputInfoByFrontEndStatus"
                v-model="caseForm.rejectMediationReasonText"
                type="textarea"
            />
        </el-form-item>

        <el-form-item label="从文件中导入案件信息">
                    <el-switch v-model="caseForm.inputInfoByTxt" />
        </el-form-item>
        
        <el-form-item  label="案件信息TXT文件路径" >
            <el-input ref="inputCaseInfoByTxtPathInput" :disabled="inputInfoByTxtDisableStatus" v-model="caseForm.inputCaseInfoByTxtPath" />
        </el-form-item>

        <el-form-item label="案件文件夹生成路径" prop="caseFolderGeneratedPath">
            <el-input v-model="caseForm.caseFolderGeneratedPath" />
        </el-form-item>

        <el-form-item>
            <el-button type="danger" @click="onSubmit(ruleFormRef)">提交案件信息</el-button>
            <el-button type="warning" disabled> 一键上传（功能开发中）</el-button>
            <el-button type="primary" @click="outputToExcel()">输出案件信息到excel</el-button>
            <el-button type="success" @click="outputToTxt()">输出案件信息到Txt文本</el-button>
        </el-form-item>

        <hr />

        <el-form-item>
            <el-button type="primary" plain @click="onAddPlaintiff">新增原告</el-button>
            <el-button type="info" plain @click="onAddDefendant">新增被告</el-button>
        </el-form-item>

    </el-form>

    <!-- 导入当事人表格部件 -->
    <LitigantForm litigantPosition="plaintiff" v-for="(item,index) in caseForm.plaintiffs"/>
    <LitigantForm litigantPosition="defendant" v-for="(item,index) in caseForm.defendants"/>

    <hr />
    <!-- 下面的是用于测试，直接展示从表格中输入的数据 -->
    <ul>
        <p>案件信息</p>
        <li v-for="(item, key) in caseForm" >
            {{ key }}  -   {{ item }} 
        </li>
    </ul>
</template>