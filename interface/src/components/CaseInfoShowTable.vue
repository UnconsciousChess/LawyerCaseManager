<template>
	<!-- 下面是正式展示案件信息栏目 -->
	<el-descriptions class="margin-top" :column="2" style="max-width: 800px" 
		border>
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

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">前期风险收费金额</div>
			</template>
			{{ showText.riskAgentUpfrontFee }} 元
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div class="cell-item">后期风险收费比例</div>
			</template>
			{{ showText.riskAgentPostFeeRate }} %
		</el-descriptions-item>
	</el-descriptions>

	<!-- <el-button @click="showText.showTextCreate()">
		刷新案件信息
	</el-button> -->

	<!-- 下面是诉讼请求等折叠栏 -->
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
	propId : Number,
})


const showText = ref({});

function showTextInitialize(prop){	
	// 遍历propData.propShowTextList，找到对应的案件信息
	let Index = propData.propShowTextList.findIndex((item) => item.id == propData.propId);
	// 将对应的案件信息赋值给showText
	showText.value = propData.propShowTextList[Index];
}

// 在挂载时调用showTextInitialize来初始化showText
onMounted(() => {
	showTextInitialize(propData);
});


// 	showTextCreate: function () {


// 		// 下面是需要转换的字段
// 		if (caseFormModel.riskAgentStatus == true) {
// 			this.riskAgentStatus = "√";
// 		} else {
// 			this.riskAgentStatus = "X";
// 		}

// 		if (caseFormModel.mediationIntention == true) {
// 			this.mediationIntention = "√";
// 		} else {
// 			this.mediationIntention = "X";
// 		}

// 		if (caseFormModel.caseType == 1) {
// 			this.caseType = "民事案件";
// 		} else if (caseFormModel.caseType == 2) {
// 			this.caseType = "行政案件";
// 		} else {
// 			this.caseType = "执行案件";
// 		}


// 		// 委托阶段转换
// 		if (caseFormModel.caseAgentStage.length == 0) {
// 			this.caseAgentStage = "无";
// 		} else {
// 			this.caseAgentStage = "";
// 			// 遍历数组并转换为字符串
// 			caseFormModel.caseAgentStage.forEach(stage => {
// 				if (stage == '1') {
// 					this.caseAgentStage += "一审立案阶段" + "、";
// 				}
// 				else if (stage == '2') {
// 					this.caseAgentStage += "一审诉讼阶段" + "、";
// 				}
// 				else if (stage == '3') {
// 					this.caseAgentStage += "二审阶段" + "、";
// 				}
// 				else if (stage == '4') {
// 					this.caseAgentStage += "执行阶段" + "、";
// 				}
// 				else if (stage == '5') {
// 					this.caseAgentStage += "再审阶段" + "、";
// 				}
// 			})
// 			// 如果最后一个字符是顿号，则去掉最后一个字符
// 			if (this.caseAgentStage.charAt(this.caseAgentStage.length - 1) == "、") {
// 				this.caseAgentStage = this.caseAgentStage.substring(0, this.caseAgentStage.length - 1);
// 			}
// 		}
// 	},

// // 
// });



</script>