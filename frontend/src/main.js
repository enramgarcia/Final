import { createApp } from 'vue';
import 'bootstrap/dist/css/bootstrap.css';
import App from "@/App";
import { createRouter, createWebHistory } from "vue-router";

import CalendarComp from "@/components/CalendarComp";
import SettingsComp from "@/components/SettingsComp";
import AdminLogin from "@/components/AdminLogin";

const routes = [
  { path: '/', component: CalendarComp },
  { path: '/settings', component: SettingsComp },
  { path: '/admin/login', component: AdminLogin }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


const app = createApp(App)

app.use(router)
app.mount("#app")
