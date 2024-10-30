<template>
    <div class="container">
        <div class="row">
            <div class="col pt-4">
                <div class="btn-group bg-body">
                    <a
                        href="#"
                        class="btn"
                        v-for="d in debts"
                        :key="d.id"
                        @click.prevent="() => { selDebt = d }"
                        :class="{ 'btn-warning': selDebt && d.id == selDebt.id }"
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
                    >
                        Выход
                    </a>
                </div>
            </div>
        </div>
        <div class="row" v-if="selDebt && details">
            <div class="col pt-4">
                <div class="bg-body p-3 rounded summary">
                    <p>
                        <span class="text-success">{{ formatInt(selDebt.amount) }}</span>₽ под 
                        <span class="text-success">{{ formatFloat(selDebt.rate) }}</span>% от 
                        <span class="text-success">{{ formatDate(selDebt.date) }}</span>
                    <br>
                        Платеж (исходный): 
                        <span class="text-success">{{ formatInt(details.default_payment) }}</span>₽
                    </p>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col pt-4">
                <div class="table-responsive table-payments bg-body p-3 rounded">
                    <div class="vtable">
                        <div class="vthead">
                            <div class="vtr">
                                <div>Месяц</div> 
                                <div>
                                    <span class="only-full">Рек.&nbsp;платеж</span>
                                    <span class="only-mobile">РП</span>
                                </div>
                                <div>Выплата</div>
                                <div class="only-full">Проценты</div>
                                <div class="only-full">Погашение</div>
                                <div class="only-full">Сумма</div>
                                <div>Остаток</div>
                            </div>
                        </div>
                        <div class="vtbody">
                            <div class="wrapper">
                                <div class="vtr text-success">
                                    <div>
                                        <span class="only-full">01.2020</span>
                                        <span class="only-mobile">01.20</span>
                                    </div>
                                    <div>
                                        <span class="only-full">10&nbsp;000,00&nbsp;₽</span>
                                        <span class="only-mobile">10000₽</span>
                                    </div>
                                    <div>
                                        <button
                                            type="button"
                                            data-loan="1"
                                            data-payment="2020-01"
                                            class="btn btn-payment btn-outline-success btn-sm"
                                        >
                                            <span class="only-full">10&nbsp;000,00&nbsp;₽</span>
                                            <span class="only-mobile">10000₽</span>
                                        </button>
                                    </div>
                                    <div class="only-full">
                                        <span class="only-full">5&nbsp;000,00&nbsp;₽</span>
                                        <span class="only-mobile">5000₽</span>
                                    </div>
                                    <div class="only-full">
                                        <span class="only-full">5&nbsp;000,00&nbsp;₽</span>
                                        <span class="only-mobile">5000₽</span>
                                    </div>
                                    <div class="only-full">
                                        <span class="only-full">10&nbsp;000,00&nbsp;₽</span>
                                        <span class="only-mobile">10000₽</span>
                                    </div>
                                    <div>
                                        <span class="only-full">495&nbsp;000,00&nbsp;₽</span>
                                        <span class="only-mobile">495000₽</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

.summary > p:last-child {
    margin-bottom: 0;
}
</style>

<script>
import axios from "axios";

export default {
    computed: {},
    data() {
        return {
            token: localStorage.getItem("token"),
            debts: [],
            selDebt: null,
            details: null,
        };
    },
    async created() {
        await this.getDebts();
        if (this.debts.length) this.selDebt = this.debts[0];
    },
    methods: {
        formatDate(date) {
            const dt = new Date(date);
            return dt.toLocaleDateString("ru-RU");
        },
        formatInt(num) { return num.toLocaleString("ru-RU"); },
        formatFloat(num) { return num.toLocaleString("ru-RU", { minimumFractionDigits: 2 }); },
        async getDebts() {
            try {
                const res = await axios.get(
                    "/api/debt",
                    { headers: { Authorization: `Bearer ${this.token}` }},
                );
                if (res.status == 200) {
                    this.debts = res.data;
                }
            } catch (e) {
                console.log(e);
                if (e.response.status == 401) this.$router.push("/login");
            }
        },
        async getDebtData() {
            try {
                const res = await axios.get(
                    "/api/debt/" + this.selDebt.id,
                    { headers: { Authorization: `Bearer ${this.token}` }},
                );
                if (res.status == 200) {
                    this.details = res.data;
                }
            } catch (e) {
                console.log(e);
                if (e.response.status == 401) this.$router.push("/login");
            }
        },
    },
    watch: {
        async selDebt(v) {
            if (v) {
                this.details = null;
                await this.getDebtData();
            }
        },
    },
};
</script>
