import { createRouter, createWebHistory } from "vue-router";

import HomePage from "@/pages/HomePage.Vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomePage },
    { path: "/login", component: () => import("@/pages/LoginPage.vue") },
    { path: "/signup", component: () => import("@/pages/SignupPage.vue") },
    {
      path: "/products",
      component: () => import("@/pages/customer/CustomerProductsPage.vue"),
    },
    {
      path: "/checkout",
      component: () => import("@/pages/customer/CheckoutCustomerPage.vue"),
    },
    {
      path: "/orders",
      component: () => import("@/pages/customer/MyOrdersPage.vue"),
    },
    {
      path: "/manager/sections",
      name: "ManagerSections",
      component: () => import("@/pages/manager/SectionsManagerPage.vue"),
    },
    {
      path: "/manager/products",
      name: "ManagerProducts",
      component: () => import("@/pages/manager/ProductsManagerPage.vue"),
    },
  ],
});

export default router;
