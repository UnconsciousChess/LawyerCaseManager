<!-- 组合式Vue -->
<script setup>
import {ref, computed} from "vue";
// 导入router部分
// import {useRoute,useRouter} from "vue-router";

const activeIndex = ref("1");
// 默认不显示About的dialog
const aboutDialog = ref({
	visible: false,
});
</script>

<template>
	<el-menu
		:default-active="activeIndex"
		:router="true"
		class="el-menu-demo"
		mode="horizontal"
	>
		<el-menu-item index="/">律师小只工具箱</el-menu-item>
		<el-sub-menu index="2">
			<template #title>文书生成器</template>
			<el-menu-item index="/case-info-form">案件信息录入</el-menu-item>
			<el-menu-item disabled>模板文件选择</el-menu-item>
			<el-menu-item disabled>归档材料生成</el-menu-item>
			<el-menu-item disabled>还没有想好的功能1</el-menu-item>
			<el-menu-item disabled>还没有想好的功能2</el-menu-item>
		</el-sub-menu>
		<el-sub-menu index="3">
			<template #title>其他工具</template>
			<el-sub-menu index="">
				<template #title>各类计算器</template>
				<el-menu-item index="/caculator">诉讼费用计算器</el-menu-item>
				<el-menu-item index="" disabled>人身损害计算器</el-menu-item>
				<el-menu-item index="" disabled>劳动案件计算器</el-menu-item>
			</el-sub-menu>
			<el-menu-item index="" disabled>还没有想好的功能3</el-menu-item>
		</el-sub-menu>
		<el-menu-item @click="aboutDialog.visible = true">关于</el-menu-item>
	</el-menu>

	<el-dialog
		v-model="aboutDialog.visible"
		title="关于本程序"
		width="300"
		draggable
	>
		<p>Version:0.2</p>
		<p>一只肥猫开发ing.....ZZzzzz</p>
	</el-dialog>
</template>
