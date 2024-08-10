<template>
	<!-- 下面是正式展示案件信息栏目 -->
	<el-descriptions class="margin-top" :title="showText.title" :column="2" style="max-width: 800px" border>
		<el-descriptions-item>
			<template #label>
				<div class="cell-item">案由</div>
			</template>
			{{ showText.causeOfAction }}
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">标的额</div>
			</template>
			{{ showText.litigationAmount }} 元
		</el-descriptions-item>

		<!-- <el-descriptions-item>
			<template #label>
				<div class="cell-item">管辖法院</div>
			</template>
			{{ showText.courtName }}
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">法院案号</div>
			</template>
			{{ showText.caseCourtCode }}
		</el-descriptions-item> -->

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">委托阶段</div>
			</template>
			{{ showText.caseAgentStage }}
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">案件类型</div>
			</template>
			{{ showText.caseType }}
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">风险收费</div>
			</template>
			{{ showText.riskAgentStatus }}
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">调解意愿</div>
			</template>
			{{ showText.mediationIntention }}
		</el-descriptions-item>

		<el-descriptions-item v-if="showText.riskAgentStatus == '是'">
			<template #label>
				<div class="cell-item">前期风险收费金额</div>
			</template>
			{{ showText.riskAgentUpfrontFee }} 元
		</el-descriptions-item>

		<el-descriptions-item v-if="showText.riskAgentStatus == '是'">
			<template #label>
				<div class="cell-item">后期风险收费比例</div>
			</template>
			{{ showText.riskAgentPostFeeRate }} %
		</el-descriptions-item>


		<el-descriptions-item v-if="showText.riskAgentStatus == '否'">
			<template #label>
				<div class="cell-item">固定收费标准</div>
			</template>
			{{ showText.agentFixedFee }}
		</el-descriptions-item>


	</el-descriptions>

	<!-- 下面是诉讼请求、事实与理由、拒绝调解理由等折叠栏 -->
	<div class="demo-collapse" style="max-width: 800px">
		<el-collapse>
			<el-collapse-item title="诉讼请求" name="1">
				<el-text>
					{{ showText.claimText }}
				</el-text>
			</el-collapse-item>
			<el-collapse-item title="事实与理由" name="2">
				<el-text>
					{{ showText.factAndReason }}
				</el-text>
			</el-collapse-item>
			<el-collapse-item title="拒绝调解理由" name="3">
				<el-text>
					{{ showText.rejectMediationReasonText }}
				</el-text>
			</el-collapse-item>
		</el-collapse>
	</div>
</template>

<script setup>

// 定义案件信息展示的数据
const propData = defineProps({
	propShowTextList: Array,
	propId: String,
})


const showText = ref({});

function showTextInitialize(prop) {
	// 遍历propData.propShowTextList，找到对应的案件信息
	let Index = prop.propShowTextList.findIndex((item) => item.caseId == prop.propId);
	// 将对应的案件信息赋值给showText
	showText.value.title = prop.propShowTextList[Index].title;
	showText.value.causeOfAction = prop.propShowTextList[Index].causeOfAction;
	showText.value.litigationAmount = prop.propShowTextList[Index].litigationAmount;
	showText.value.caseType = prop.propShowTextList[Index].caseType;
	showText.value.stages = prop.propShowTextList[Index].stages;
	showText.value.caseAgentStage = prop.propShowTextList[Index].caseAgentStage;
	showText.value.riskAgentUpfrontFee = prop.propShowTextList[Index].riskAgentUpfrontFee;
	showText.value.riskAgentPostFeeRate = prop.propShowTextList[Index].riskAgentPostFeeRate;
	showText.value.claimText = prop.propShowTextList[Index].claimText;
	showText.value.factAndReason = prop.propShowTextList[Index].factAndReason;
	showText.value.rejectMediationReasonText = prop.propShowTextList[Index].rejectMediationReasonText;
	showText.value.agentFixedFee = prop.propShowTextList[Index].agentFixedFee;
	showText.value.caseId = prop.propShowTextList[Index].caseId;

	// 下面是需要转换的字段

	// 转换调解意愿为【同意调解】或【拒绝调解】
	if (prop.propShowTextList[Index].mediationIntention == true) {
		showText.value.mediationIntention = "同意调解";
	} else {
		showText.value.mediationIntention = "拒绝调解";
	}

	// 转换风险代理状态为【是】或【否】
	if (prop.propShowTextList[Index].riskAgentStatus == true) {
		showText.value.riskAgentStatus = "是";
	} else {
		showText.value.riskAgentStatus = "否";
	}

	// 转换案件类型为【民事案件】、【行政案件】或【执行案件】
	if (prop.propShowTextList[Index].caseType == 1) {
		showText.value.caseType = "民事案件";
	} else if (prop.propShowTextList[Index].caseType == 2) {
		showText.value.caseType = "行政案件";
	} else if (prop.propShowTextList[Index].caseType == 3) {
		showText.value.caseType = "执行案件";
	}


	// 转换案件阶段为【一审立案阶段】、【一审诉讼阶段】、【二审阶段】、【执行阶段】、【再审阶段】
	if (prop.propShowTextList[Index].caseAgentStage.length == 0) {
		showText.value.caseAgentStage = "无";
	} else {
		showText.value.caseAgentStage = "";
		// 遍历数组并转换为字符串
		prop.propShowTextList[Index].caseAgentStage.forEach(stage => {
			if (stage == '1') {
				showText.value.caseAgentStage += "一审立案阶段" + "、";
			}
			else if (stage == '2') {
				showText.value.caseAgentStage += "一审诉讼阶段" + "、";
			}
			else if (stage == '3') {
				showText.value.caseAgentStage += "二审阶段" + "、";
			}
			else if (stage == '4') {
				showText.value.caseAgentStage += "执行阶段" + "、";
			}
			else if (stage == '5') {
				showText.value.caseAgentStage += "再审阶段" + "、";
			}
		})
		// 如果最后一个字符是顿号，则去掉最后一个字符
		if (showText.value.caseAgentStage.charAt(showText.value.caseAgentStage.length - 1) == "、") {
			showText.value.caseAgentStage = showText.value.caseAgentStage.substring(0, showText.value.caseAgentStage.length - 1);
		}
	}


}

// 在挂载时调用showTextInitialize来初始化showText
onMounted(() => {
	showTextInitialize(propData);
});



</script>