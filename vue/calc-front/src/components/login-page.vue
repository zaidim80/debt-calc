<template>
    <main class="form-signin w-100 m-auto">
        <form>
            <h2>Вход</h2>
            <div class="form-floating">
                <input type="email" class="form-control" id="floatingInput" placeholder="Имя пользователя">
                <label for="floatingInput">Имя пользователя</label>
            </div>
            <div class="form-floating">
                <input type="password" class="form-control" id="floatingPassword" placeholder="Пароль">
                <label for="floatingPassword">Пароль</label>
            </div>
            <button class="btn btn-primary w-100 py-2 mt-2" type="submit">Войти</button>
        </form>
    </main>
</template>

<style scoped>
.form-signin {
    max-width: 480px;
    padding: 2rem 3rem;
    background: #fff;
    border-radius: .5rem;
}
.form-signin .form-floating:focus-within {
    z-index: 2;
}
.form-signin input[type="email"] {
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
