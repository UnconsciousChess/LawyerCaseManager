// 导入App.vue
import App from './App.vue'
// 导入router
import {createMemoryHistory, createRouter} from 'vue-router'


// 导入组件
import CaseInfoForm from './components/CaseInfoForm.vue'
import Caculator from './components/Caculator.vue'
import Blank from './components/Blank.vue'
import CaseInfoShow from './components/CaseInfoShowTable.vue'
import TemplateFileTable from './components/TemplateFileTable.vue'
import TemplateFileEditForm from './components/TemplateFileEditForm.vue'

// 设置路由
const routes = [
  {path: '/', component: Blank },
  {path: '/caculator', component:Caculator},
  {path: '/case-info-table', component: CaseInfoShow},
  {path: '/template-file', component: TemplateFileTable},
  {path: '/test',component: TemplateFileEditForm},
]

// 创建router的实例
const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

// 创建Vue实例app
const app = createApp(App)

// app使用router
app.use(router)

// 将app挂载到id为vueapp的dom上
app.mount('#vueapp')
