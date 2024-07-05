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

		<el-descriptions-item>
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
		</el-descriptions-item>

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

import { ref, onMounted } from "vue";

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
	showText.value = prop.propShowTextList[Index];
}

// 在挂载时调用showTextInitialize来初始化showText
onMounted(() => {
	showTextInitialize(propData);
});


</script>