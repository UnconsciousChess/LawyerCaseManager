<script setup>
import AppMenu from "./components/Menu.vue";
</script>


<style>
</style>


<template>
	<el-container>
		<el-header>
			<!-- 调用组件AppMenu，作为菜单控件插入到el-header里面 -->
			<AppMenu />
		</el-header>
		<el-main>
			<RouterView />
		</el-main>
	</el-container>
</template>

