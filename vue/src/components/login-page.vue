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
                    type="password"
                    class="form-control"
                >
                <label for="floatingPassword">Пароль</label>
            </div>
            <button
                @click.prevent="login"
                class="btn btn-primary w-100 py-2"
            >
                Войти
            </button>
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
                    localStorage.setItem("token", res.data.access_token);
                    this.$router.push("/");
                }
            } catch (error) {
                console.error('Error registering user:', error);
            }
        },
    },
};
</script>

<style scoped>
.form-signin {
    max-width: 320px;
    padding: 1rem;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.form-signin form {
    width: 100%;
    display: flex;
    flex-direction: column;
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
</style>
