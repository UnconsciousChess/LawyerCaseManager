<!-- 组合式Vue -->
<script setup>
import AppMenu from "./components/Menu.vue";
</script>

<template>
	<el-container>
		<el-header>
			<!-- 调用组件AppMenu，插入到el-header里面 -->
			<AppMenu />
		</el-header>
		<el-main>
			<RouterView />
		</el-main>
	</el-container>
</template>
