import { createRouter, createWebHistory } from "vue-router";

import HomePage from "@/pages/HomePage.Vue";
import SignupPage from "@/pages/SignupPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomePage },
    { path: "/login", component: import("@/pages/LoginPage.vue") },
    { path: "/signup", component: SignupPage },
  ],
});

export default router;
