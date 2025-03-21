import { createApp } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./custom.scss";
import { Toast } from "bootstrap";

import App from "./App.vue";
import "./style.css";

const app = createApp(App);

app.config.globalProperties.$showToast = function (message, options = {}) {
    // Создаем элемент Toast
    const toastElement = document.createElement("div");
    let icon = "bi-info-circle";
    toastElement.classList.add("toast");
    if (options.type === "success") {
        toastElement.classList.add("text-bg-success");
        icon = "bi-check-circle";
    } else if (options.type === "error") {
        toastElement.classList.add("text-bg-danger");
        icon = "bi-exclamation-octagon";
    }
    // Задаем содержимое Toast
    toastElement.innerHTML = `
        <div class="d-flex align-items-center ps-3">
            <i class="fs-3 bi ${icon}"></i>
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    // Добавляем Toast в контейнер
    const toastContainer = document.getElementById("toast-container");
    toastContainer.appendChild(toastElement);
    // Инициализируем Toast с помощью Bootstrap
    const toast = new Toast(toastElement, {
        autohide: options.autohide !== undefined ? options.autohide : true,
        delay: options.delay || 3000,
    });
    // Показываем Toast
    toast.show();
    // Удаляем Toast после скрытия
    toastElement.addEventListener("hidden.bs.toast", () => {
        toastElement.remove();
    });
};

import HomePage from "./components/home-page.vue";
import LoginPage from "./components/login-page.vue";

const routes = [
    { path: "/", component: HomePage, meta: { requiresAuth: true }, },
    { path: "/login", component: LoginPage, },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const token = sessionStorage.getItem("token");
    if (to.matched.some((route) => route.meta.requiresAuth)) {
        if (token) { next(); } else { next("/login"); }
    } else {
        next();
    }
});

app.use(router);
app.mount("#app");
