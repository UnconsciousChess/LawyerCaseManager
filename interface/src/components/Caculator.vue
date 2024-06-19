<script setup>
import { ref, onMounted, reactive } from 'vue'
import { litigationFeeCaculator, executionFeeCaculator, preservationFeeCaculator } from '../js/caculator.js'


const caculator = ref({
    amount: 0,
    result: 0,
});


const countLitigationFee = () => {
    console.log("计算诉讼费");
    caculator.value.result = litigationFeeCaculator(caculator.value.amount);

}

const countExecutionFee = () => {
    console.log("计算执行费");
    caculator.value.result = executionFeeCaculator(caculator.value.amount);

}

const countPreservationFee = () => {
    console.log("计算保全费");
    caculator.value.result = preservationFeeCaculator(caculator.value.amount);
}
</script>



<template>
    <el-space wrap>
        <el-input aria-label="输入标的额" v-model="caculator.amount" />
    <el-row>
        <el-button type="success" plain @click="countLitigationFee">计算诉讼费</el-button>
        <el-button type="danger" plain @click="countExecutionFee">计算执行费</el-button>
        <el-button type="info" plain @click="countPreservationFee">计算保全费</el-button>
    </el-row>
        <el-text class="mx-1" type="primary">计算结果：{{ caculator.result }}元</el-text>
    </el-space>



</template>