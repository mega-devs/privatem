import { createApp } from 'vue'
import router from "./router";
import store from "./store";
import App from './App.vue'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-icons/font/bootstrap-icons.css"

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

let app = createApp(App)
// app.config.globalProperties.back_url = "http://127.0.0.1:5000"


const vuetify = createVuetify({
  components,
  directives,
})

app.use(store)
app.use(router)
app.use(vuetify)
app.mount('#app')



// import { createApp } from 'vue';
// import router from './router';
// import store from './store';
// import App from './App.vue';

// import 'bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap-icons/font/bootstrap-icons.css';

// import * as Sentry from '@sentry/vue';

// let app = createApp(App);

// // Initializing Sentry
// Sentry.init({
//   app,
//   dsn: "https://eb3e92615a5e2798aac8e9b55e7b6b30@o4508331533074432.ingest.de.sentry.io/4508331555422288",
//   integrations: [
//     Sentry.browserTracingIntegration({ router }),
//     Sentry.replayIntegration(),
//   ],
//   // Tracing
//   tracesSampleRate: 1.0, // Capture 100% of the transactions
//   // Set 'tracePropagationTargets' to control for which URLs distributed tracing should be enabled
//   tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
//   // Session Replay
//   replaysSessionSampleRate: 0.1, // Set the sample rate at 10%
//   replaysOnErrorSampleRate: 1.0, // 100% sample rate on errors
// });

// // Use Vuex store, Vue router, and mount the app
// app.use(store).use(router).mount('#app');
