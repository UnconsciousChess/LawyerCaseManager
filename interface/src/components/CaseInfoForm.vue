<!-- 组合式Vue -->
<script setup>
import { ref, onMounted , reactive} from 'vue'
// import { FormInstance } from 'element-plus'

// 导入自写部分
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
	plaintiffInfoPath: "",
	defendantInfoPath: "",
	factAndReason: "",
	caseFolderGeneratedPath: "",
	claimText: "",
	rejectMediationReasonText: "",
});



const caseFormRef = ref(null);



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
	plaintiffInfoPath: [
		{ required: true, message: "请输入原告信息txt路径", trigger: "blur" },
	],
	defendantInfoPath: [
		{ required: true, message: "请输入被告信息txt路径", trigger: "blur" },
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




// 提交函数方法
function onSubmit() {
    // if(!caseForm.value) return
    caseFormRef.value.validate((valid) => {
        if (valid) {
            console.log("表单校验通过");
	        console.log(caseForm.value);
	        // pywebview.api.generateCaseFolder(caseForm.value);   #关于pywebview的部分在组合前后端的时候再使用
        } 
        else {
            console.log("表单校验失败");
            return false;
        }
    })
}

// 新增原告方法
function onAddPlaintiff() {
	console.log("新增一个原告");
}

// 新增被告方法
function onAddDefendant() {
	console.log("新增一个被告");
}

</script>

<template>
    <el-form
        v-bind:model="caseForm"
        v-bind:rules="caseFormRules"
        label-width="auto"
        style="max-width: 500px"
        ref="caseFormRef"
    >
        <el-form-item label="法院案号" prop="caseCourtCode">
            <el-input v-model.trim="caseForm.caseCourtCode" />
        </el-form-item>

        <el-form-item label="案由" prop="causeOfAction">
            <el-input v-model.trim="caseForm.causeOfAction" />
        </el-form-item>

        <el-form-item label="标的额" prop="litigationAmount">
            <el-input v-model.number="caseForm.litigationAmount" />
        </el-form-item>

        <el-row>
            <el-col :span="12">
                <el-form-item label="风险收费" >
                    <el-switch v-model="caseForm.riskAgentStatus" />
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
                    <el-input v-model.number="caseForm.riskAgentUpfrontFee" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="后期风险收费比例" prop="riskAgentPostFeeRate">
                    <el-input v-model.number="caseForm.riskAgentPostFeeRate" />
                </el-form-item>
            </el-col>
        </el-row>

        <el-form-item>
            委托阶段：
            <el-checkbox-group
                v-model="caseForm.caseAgentStage"
                id="caseAgentStage"
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
            <el-radio-group v-model="caseForm.caseType" id="caseType">
                <el-radio value=1>民事案件</el-radio>
                <el-radio value=2>行政案件</el-radio>
                <el-radio value=3>执行案件</el-radio>
            </el-radio-group>
        </el-form-item>

        <el-form-item label="管辖法院" prop="courtName">
            <el-input v-model="caseForm.courtName" />
        </el-form-item>

        <hr />

        <el-form-item label="原告信息txt路径" prop="plaintiffInfoPath">
            <el-input v-model="caseForm.plaintiffInfoPath" />
        </el-form-item>

        <el-form-item label="被告信息txt路径" prop="defendantInfoPath">
            <el-input v-model="caseForm.defendantInfoPath" />
        </el-form-item>

        <el-form-item label="诉讼请求" prop="claimText">
            <el-input v-model="caseForm.claimText" type="textarea" />
        </el-form-item>

        <el-form-item label="事实与理由" prop="factAndReason">
            <el-input v-model="caseForm.factAndReason" type="textarea" />
        </el-form-item>

        <el-form-item label="拒绝调解理由">
            <el-input
                v-model="caseForm.rejectMediationReasonText"
                type="textarea"
            />
        </el-form-item>

        <el-form-item label="案件文件夹生成路径" prop="caseFolderGeneratedPath">
            <el-input v-model="caseForm.caseFolderGeneratedPath" />
        </el-form-item>

        <el-form-item>
            <el-button type="danger" @click="onSubmit(ruleFormRef)">一键生成</el-button>
            <el-button type="warning" disabled> 一键上传（功能开发中）</el-button>
        </el-form-item>

        <hr />

        <el-form-item>
            <el-button type="primary" plain @click="onAddPlaintiff">新增原告</el-button>
            <el-button type="info" plain @click="onAddDefendant"
                >新增被告</el-button
            >
        </el-form-item>

    </el-form>

    <!-- 导入当事人表格部件 -->
    <LitigantForm />

    <hr />
    <ul>
        <p>案件信息</p>
        <li v-for="(item, key) in caseForm" >
            {{ key }}  - {{ item }} 
        </li>
    </ul>
</template>