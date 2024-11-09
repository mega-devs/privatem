import { createApp } from 'vue'
import router from "./router";
import store from "./store";
import App from './App.vue'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-icons/font/bootstrap-icons.css"

let app = createApp(App)
// app.config.globalProperties.back_url = "http://127.0.0.1:5000"
app.use(store).use(router).mount('#app')
