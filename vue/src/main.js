import { createApp } from "vue";
import { createWebHistory, createRouter } from "vue-router";

import "bootstrap/dist/css/bootstrap.min.css";
import "./custom.scss";
import "bootstrap";

import App from "./App.vue";
import "./style.css";

import HomePage from "./components/home-page.vue";
import LoginPage from "./components/login-page.vue";

const routes = [
    { path: "/", component: HomePage, meta: { requiresAuth: true }, },
    { path: "/login", component: LoginPage, },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token");
    if (to.matched.some((route) => route.meta.requiresAuth)) {
        if (token) { next(); } else { next("/login"); }
    } else {
        next();
    }
});

createApp(App)
    .use(router)
    .mount('#app');
