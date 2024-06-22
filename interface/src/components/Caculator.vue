<script setup>
import {ref, onUpdated} from "vue";
import {
	litigationFeeCaculator,
	executionFeeCaculator,
	preservationFeeCaculator,
} from "../js/caculator.js";

const caculator = ref({
	amount: 0,
	result: 0,
	caseType: false,
	caseProcedureType: null,
	administrativeCaseType: null,
});

const ButtonConfig = ref({
	LitigationFeeButtonDisabledStatus: false,
	ExecutionFeeDisabledStatus: false,
	PreservationFeeDisabledStatus: false,
});

const InputboxConfig = ref({
	FeeInputDisabledStatus: false,
});

const temp = ref(0);

// 计算诉讼费
const countLitigationFee = () => {
	console.log("计算诉讼费");
	// 如果是行政案件，根据《诉讼费用交纳办法》第十三条（五）1.商标、专利、海事行政案件每件交纳100元；2.其他行政案件每件交纳50元。
	if (caculator.value.caseType == "1") {
        if (caculator.value.administrativeCaseType == 1) {
		    caculator.value.result = 50;
        } else {
            caculator.value.result = 100;
        }
	}
	// 如果是民事案件，调用诉讼费计算函数
	else {
		caculator.value.result = litigationFeeCaculator(caculator.value.amount);
	}
};

// 计算执行费
const countExecutionFee = () => {
	console.log("计算执行费");
	caculator.value.result = executionFeeCaculator(caculator.value.amount);
};

// 计算保全费
const countPreservationFee = () => {
	console.log("计算保全费");
	caculator.value.result = preservationFeeCaculator(caculator.value.amount);
};

// 监听案件类型是否发生变化
function ChangeInputStatus() {
	// true = 行政案件 false = 民事案件
	if (caculator.value.caseType == true) {
		// 行政案件无须输入标的额，因为诉讼费是固定的
		InputboxConfig.value.FeeInputDisabledStatus = true;
		// 按钮状态，行政案件没有保全费和执行费
		ButtonConfig.value.ExecutionFeeDisabledStatus = true;
		ButtonConfig.value.PreservationFeeDisabledStatus = true;
        // 将案件标的额清零,把当前的值保留到temp中，等回到民事案件的时候再恢复
        temp.value = caculator.value.amount;
        caculator.value.amount = 0;
        // 清除此前的计算结果
        caculator.value.result = 0; 

	} else {
		InputboxConfig.value.FeeInputDisabledStatus = false;
		ButtonConfig.value.ExecutionFeeDisabledStatus = false;
		ButtonConfig.value.PreservationFeeDisabledStatus = false;
        // 恢复案件标的额
        caculator.value.amount = temp.value;
        // 清除此前的计算结果
        caculator.value.result = 0;
	}
}
</script>

<template>
	<el-form>
		<!-- 下面是案件类型选择，民事或行政 -->
		<el-form-item>
			<el-text>请选择案件类型：</el-text>
			<el-switch
				v-model="caculator.caseType"
				inline-prompt
				active-text="行政案件"
				inactive-text="民事案件"
				style="--el-switch-on-color: #bbc4eb; --el-switch-off-color: #ecc897"
				@change="ChangeInputStatus"
			></el-switch>
		</el-form-item>
		<!-- 下面是当行政案件的时候选择 -->
		<el-form-item v-if="caculator.caseType == true">
			<el-radio
				v-model="caculator.administrativeCaseType"
				value="1"
				size="large"
				>商标、专利、海事案件</el-radio
			>
			<el-radio
				v-model="caculator.administrativeCaseType"
				value="2"
				size="large"
				>其他案件</el-radio
			>
		</el-form-item>
		<!-- 下面是输入案件标的额的输入框 -->
		<el-form-item>
			<el-text>请输入案件标的额：</el-text>
			<el-input
				style="width: 240px"
				v-model="caculator.amount"
				class="input-with-select"
				placeholder="人民币元"
				:disabled="InputboxConfig.FeeInputDisabledStatus"
			>
				<template #prepend>
					<el-select
						v-model="caculator.caseProcedureType"
						placeholder="请选择"
						style="width: 100px"
						:disabled="InputboxConfig.FeeInputDisabledStatus"
					>
						<el-option label="普通程序" value="1"></el-option>
						<el-option label="简易程序" value="2"></el-option>
					</el-select>
				</template>
			</el-input>
		</el-form-item>

		<!-- 下面是计算的按钮 -->
		<el-form-item>
			<el-row>
				<el-button
					type="success"
					plain
					@click="countLitigationFee"
					:disabled="ButtonConfig.LitigationFeeButtonDisabledStatus"
					>计算诉讼费</el-button
				>
				<el-button
					type="danger"
					plain
					@click="countExecutionFee"
					:disabled="ButtonConfig.ExecutionFeeDisabledStatus"
					>计算执行费</el-button
				>
				<el-button
					type="info"
					plain
					@click="countPreservationFee"
					:disabled="ButtonConfig.ExecutionFeeDisabledStatus"
					>计算保全费</el-button
				>
			</el-row>
		</el-form-item>

		<!-- 下面是计算结果 -->
		<el-form-item>
			<el-card>
				<el-text class="mx-1" type="primary"
					>计算结果：{{ caculator.result }}元</el-text
				>
			</el-card>
		</el-form-item>
	</el-form>
</template>
