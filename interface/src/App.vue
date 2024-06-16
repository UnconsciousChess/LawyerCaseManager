<!-- 组合式Vue -->
<script setup>
import CaseInfoForm from './components/CaseInfoForm.vue'
</script>


<template>
	<el-container>
		<el-header>
			<h1>案件信息表单</h1>
		</el-header>
		<el-main>
			<!-- 调用案件表单组件CaseInfoForm，插入到el-main里面 -->
			<CaseInfoForm/>
		</el-main>
	</el-container>
</template>