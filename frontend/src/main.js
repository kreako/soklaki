import { createApp } from "vue";
import App from "./App.vue";
import "./index.css";
import { router } from "./routes";
import { store } from "./store";
import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";
import { version } from "../package.json";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  release: "soklaki@" + version,
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0,
});

const app = createApp(App).use(router).use(store);

app.config.errorHandler = (err, vm, info) => {
  Sentry.captureException(err);
};

app.mount("#app");

window.addEventListener("error", (event) => {
  Sentry.captureException(event);
});
window.addEventListener("unhandledrejection", (event) => {
  Sentry.captureException(event);
});
