import { createApp } from 'vue';
import { createMemoryHistory, createRouter } from 'vue-router';

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import App from './app.vue';
import './style.css';

import HomePage from './components/home-page.vue';
import LoginPage from './components/login-page.vue';

const routes = [
    { path: '/', component: HomePage, },
    { path: '/login', component: LoginPage, },
];

const router = createRouter({
    history: createMemoryHistory(),
    routes,
});

createApp(App)
    .use(router)
    .mount('#app');
