<template>
	<el-container>
		<el-header>
			<h1>案件信息表单</h1>
		</el-header>
		<el-main>
			<el-form :model="form" label-width="auto" style="max-width: 600px">
				<el-form-item label="法院案号">
					<el-input v-model="caseForm.caseCourtCode" />
				</el-form-item>

				<el-form-item label="案由">
					<el-input v-model="caseForm.causeOfAction" />
				</el-form-item>

				<el-form-item label="标的额">
					<el-input v-model="caseForm.litigationAmount" />
				</el-form-item>

				<el-row>
					<el-col :span="12">
						<el-form-item label="风险收费">
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
						<el-form-item label="前期风险收费金额">
							<el-input v-model="caseForm.riskAgentUpfrontFee" />
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="后期风险收费比例">
							<el-input v-model="caseForm.riskAgentPostFeeRate" />
						</el-form-item>
					</el-col>
				</el-row>

				<el-form-item label="委托阶段" id="caseAgentStage">
					<el-checkbox-group v-model="caseForm.caseAgentStage">
						<el-checkbox value=1 name="type"> 一审立案阶段 </el-checkbox>
						<el-checkbox value=2 name="type"> 一审开庭阶段 </el-checkbox>
						<el-checkbox value=3 name="type"> 二审阶段 </el-checkbox>
						<el-checkbox value=4 name="type"> 执行阶段 </el-checkbox>
						<el-checkbox value=5 name="type"> 再审阶段 </el-checkbox>
					</el-checkbox-group>
				</el-form-item>

				<el-form-item label="案件类型" id="caseType">
					<el-radio-group v-model="caseForm.caseType">
						<el-radio value=1>民事案件</el-radio>
						<el-radio value=2>行政案件</el-radio>
						<el-radio value=3>执行案件</el-radio>
					</el-radio-group>
				</el-form-item>

				<el-form-item label="管辖法院">
					<el-input v-model="caseForm.courtName" />
				</el-form-item>

				<hr />

				<el-form-item label="原告信息txt路径">
					<el-input v-model="caseForm.plaintiffInfoPath" />
				</el-form-item>

				<el-form-item label="被告信息txt路径">
					<el-input v-model="caseForm.defendantInfoPath" />
				</el-form-item>

				<el-form-item label="诉讼请求">
					<el-input v-model="caseForm.claimText" type="textarea" />
				</el-form-item>

				<el-form-item label="事实与理由">
					<el-input v-model="caseForm.factAndReason" type="textarea" />
				</el-form-item>

				<el-form-item label="拒绝调解理由">
					<el-input v-model="caseForm.rejectMediationReasonText" type="textarea" />
				</el-form-item>

				<el-form-item label="案件文件夹生成路径">
					<el-input v-model="caseForm.caseFolderGeneratedPath" />
				</el-form-item>

				<el-form-item>
					<el-button type="danger" @click="onSubmit">一键生成</el-button>
					<el-button type="warning" disabled>
						一键上传（功能开发中）</el-button>
				</el-form-item>

				<hr />

				<el-form-item>
					<el-button type="primary" @click="onAddPlaintiff">新增原告</el-button>
				</el-form-item>
			</el-form>
		</el-main>
	</el-container>
</template>

<style>
/* 这里留空，后面要另外加css再写 */
</style>

<script>

export default {
	data() {
		return {
			caseForm: {
				caseCourtCode: "",
				causeOfAction: "",
				litigationAmount: "",
				riskAgentStatus: true,
				riskAgentUpfrontFee: "",
				riskAgentPostFeeRate: "",
				caseAgentStage: [],
				caseType: "",
				courtName: "",
        		mediationIntention: true,
				plaintiffInfoPath: "",
				defendantInfoPath: "",
				factAndReason: "",
				caseFolderGeneratedPath: "",
				claimText: "",
				rejectMediationReasonText: "",
			},
		};
	},

	// methods
	methods:{
		// 选择提交表单按钮以后，将表单数据通过pywebview.api.XXXmethod()传递给后端
		async onSubmit() {
			
			// XXXX...

			// 在此传递到后端之前可以做一些表单验证
			pywebview.api.generateCaseFolder(this.caseForm);
			console.log("提交表单");
			console.log(this.caseForm);
		},


		onAddPlaintiff() {
			console.log("新增一个原告");
		},
	},


};

</script>
