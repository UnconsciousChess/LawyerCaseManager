<!-- 组合式Vue -->
<script setup>
import {ref, onMounted, reactive} from "vue";

const activeIndex = ref('1')

const dialogVisible = ref(false)


</script>

<template>
	<el-menu
		:default-active="activeIndex"
		class="el-menu-demo"
		mode="horizontal"
		@select="handleSelect"
	>
		<el-menu-item index="1">文书生成器</el-menu-item>
		<el-sub-menu index="2">
			<template #title>杂项文书生成</template>
			<el-menu-item index="2-1">案件信息录入</el-menu-item>
			<el-menu-item index="2-2">文件选择</el-menu-item>
			<el-menu-item index="2-3">生成结构</el-menu-item>
		</el-sub-menu>
        <el-sub-menu index="3">
            <template #title>其他工具</template>
            <el-sub-menu index="3-1">
                <template #title>各类计算器</template>
                <el-menu-item index="3-1-1" disabled>诉讼费用计算器</el-menu-item>
                <el-menu-item index="3-1-2" disabled>人身损害计算器</el-menu-item>
                
            </el-sub-menu>
            <el-menu-item index="3-2" disabled>还没有想好的功能</el-menu-item>
        </el-sub-menu>
        <el-menu-item @click="dialogVisible=true" index="5">关于</el-menu-item>
	</el-menu>


	<el-dialog
		v-model="dialogVisible"
		title="关于本程序"
		width="300"
		:before-close="handleClose"
  	>
    <span>一只肥猫开发ing.....ZZzzzz</span>
  	</el-dialog>
	
</template>
