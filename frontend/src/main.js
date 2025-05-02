// ─── main.js ───
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { useToast } from 'vue-toastification' // ← 動作確認用

const app = createApp(App)
app.use(router)
app.use(Toast, {
	position : 'top-center',   // or 'bottom-center'
	timeout  : 4000,
	hideProgressBar : true,
	closeOnClick    : true,
	draggable       : false,
	transition      : 'Vue-Toastification__bounce'  // ふわっと
  })
app.mount('#app')

