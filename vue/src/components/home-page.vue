<template>
    <div class="container">
        <nav-panel :debts="debts" :selection="selDebt" @selected="s => selDebt = s" @exit="exit" />
        <info-panel v-if="selDebt" :selection="selDebt" :details="details" />
        <payments-tab v-if="selDebt" :selection="selDebt" :details="details" />
    </div>
</template>

<script>
import axios from "axios";

import NavPanel from "./home/nav-panel.vue";
import InfoPanel from "./home/info-panel.vue";
import PaymentsTab from "./home/payments-tab.vue";

export default {
    components: {
        NavPanel,
        InfoPanel,
        PaymentsTab,
    },
    data() {
        return {
            token: sessionStorage.getItem("token"),
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
        exit() {
            sessionStorage.removeItem("token");
            this.token = null;
            this.$router.push("/login");
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

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    flex: 1 1 100%;
}
@media (max-width: 577px) {
}
</style>
