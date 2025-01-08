<template>
    <div>
        <div class="row nav offcanvas-lg offcanvas-end" ref="mainnav">
            <div class="offcanvas-header">
                <button type="button" class="btn-close" @click="hideMenu"></button>
            </div>
            <div class="offcanvas-body">
                <div class="col pt-4">
                    <div class="btn-group bg-body">
                        <a
                            href="#"
                            class="btn"
                            v-for="d in debts"
                            :key="d.id"
                            @click.prevent="() => { hideMenu(); $emit('selected', d); }"
                            :class="{ 'btn-primary': selection && d.id == selection.id }"
                        >
                            {{ d.name }}
                        </a>
                    </div>
                </div>
                <div class="col pt-4 text-end">
                    <div class="btn-group bg-body">
                        <a
                            href="#"
                            class="btn"
                        >
                            Пользователи
                        </a>
                        <a
                            href="#"
                            class="btn"
                            @click.prevent="() => { hideMenu(); $emit('exit'); }"
                        >
                            Выход
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <button class="btn btn-primary d-lg-none" type="button" @click="showMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
    </div>
</template>

<script>
import { Offcanvas } from 'bootstrap';

export default {
    props: {
        debts: Array,
        selection: Object,
    },
    data() {
        return {
            menu: null,
        };
    },
    mounted() {
        this.menu = new Offcanvas(this.$refs.mainnav);
    },
    methods: {
        showMenu() {
            this.menu.show();
        },
        hideMenu() {
            this.menu.hide();
        },
    },
};
</script>

<style scoped>
.btn {
    padding: 0.3rem 1.5rem 0.5rem 1.5rem;
    border: none;
    border-top: 0.5rem solid #dae1f2;
    border-radius: 0;
}
:not(.btn-check) + .btn:active, .btn:first-child:active {
    border-top: 0.5rem solid #ffa45f;
}
.btn-primary, .btn-primary:first-child {
    color: #fff;
    background: #ff7c1a;
    border: none;
    border-top: 0.5rem solid #ff5d1d;
}
.navbar-toggler-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='white' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}
@media (max-width: 577px) {
    .btn-group {
        display: flex;
        flex-direction: column;
    }
    .nav.row {
        margin: 0;
    }
    .offcanvas-body {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .offcanvas-body .btn {
        border-top: none !important;
        padding: 0.5rem 1.5rem 0.5rem 1.5rem;
    }
    .offcanvas-body .col {
        flex: 0 0 auto;
    }
}
</style>