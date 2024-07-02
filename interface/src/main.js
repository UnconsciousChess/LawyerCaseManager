// 导入Vue
import { createApp } from 'vue'
// 导入App.vue
import App from './App.vue'
// 导入router
import {createMemoryHistory, createRouter} from 'vue-router'
// 导入Element
import ElementPlus from 'element-plus'
// 导入Element样式
import 'element-plus/dist/index.css'


// 导入组件
import CaseInfoForm from './components/CaseInfoForm.vue'
import Caculator from './components/Caculator.vue'
import Blank from './components/Blank.vue'
import CaseInfoShow from './components/CaseInfoShow.vue'
import TemplateFileForm from './components/TemplateFileForm.vue'

// 设置路由
const routes = [
  {path: '/', component: Blank },
  {path: '/case-info-form', component: CaseInfoForm},
  {path: '/caculator', component:Caculator},
  {path: '/case-info-list', component: CaseInfoShow},
  {path: '/template-file', component: TemplateFileForm},
]

// 创建router的实例
const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

// 创建Vue实例app
const app = createApp(App)

// app使用Element
app.use(ElementPlus)
// app使用router
app.use(router)


// 将app挂载到id为vueapp的dom上
app.mount('#vueapp')
