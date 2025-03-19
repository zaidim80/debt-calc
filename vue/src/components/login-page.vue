<template>
    <main class="form-signin w-100 m-auto">
        <form>
            <img class="mb-2 m-auto" src="../assets/rabbit.svg" alt="" width="160" height="160">
            <div class="form-floating">
                <input
                    v-model="username"
                    type="text"
                    class="form-control"
                >
                <label for="floatingInput">Имя пользователя</label>
            </div>
            <div class="form-floating">
                <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                >
                <label for="floatingPassword">Пароль</label>
                <button 
                    type="button" 
                    class="btn btn-link position-absolute end-0 top-50 translate-middle-y pe-3"
                    @click="showPassword = !showPassword"
                >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
            </div>
            <button
                @click.prevent="login"
                class="btn btn-primary w-100 py-2"
            >
                Войти
            </button>
            <div v-if="error" class="alert alert-danger mt-3">
                {{ error }}
            </div>
        </form>
    </main>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            username: "",
            password: "",
            error: null,
            showPassword: false,
        };
    },
    methods: {
        async login() {
            try {
                const formData = new FormData();
                formData.append("username", this.username);
                formData.append("password", this.password);
                const res = await axios.post("/api/token", formData);
                if (res.status == 200 && res.data.access_token) {
                    sessionStorage.setItem("token", res.data.access_token);
                    this.$router.push("/");
                } else {
                    this.error = res?.data?.detail || "Неизвестная ошибка";
                }
            } catch (error) {
                this.error = error?.response?.data?.detail || "Неизвестная ошибка";
            }
        },
    },
};
</script>

<style scoped>
.form-signin {
    max-width: 320px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.form-signin form {
    padding: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 12px;
}
.form-signin .form-floating:focus-within {
    z-index: 2;
}
.form-signin input[type="text"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
.form-floating .btn-link {
    color: #6c757d;
    text-decoration: none;
    padding: 0;
    z-index: 3;
}
.form-floating .btn-link:hover {
    color: #0d6efd;
}
</style>
