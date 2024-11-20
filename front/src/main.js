import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

Sentry.init({
  app,
  dsn: "https://<your-public-key>@o<organization-id>.ingest.sentry.io/<project-id>",
  integrations: [
    new BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracePropagationTargets: ["localhost", /^\//],
    }),
  ],
  tracesSampleRate: 1.0, // rate for monitoring
});

app.use(router).mount("#app");

// import { createApp } from 'vue'
// import router from "./router";
// import store from "./store";
// import App from './App.vue'

// import "bootstrap"
// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap-icons/font/bootstrap-icons.css"

// let app = createApp(App)
// // app.config.globalProperties.back_url = "http://127.0.0.1:5000"
// app.use(store).use(router).mount('#app')
