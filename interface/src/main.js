// 导入Vue
import { createApp } from 'vue'
// 导入App.vue
import App from './App.vue'

// 导入Element
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建Vue实例app
const app = createApp(App)

// app使用Element
app.use(ElementPlus)

// 将app挂载到id为vueapp的dom上
app.mount('#vueapp')
