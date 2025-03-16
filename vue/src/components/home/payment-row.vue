<template>
    <div class="vtr" :class="monthClass">
        <div>
            <span class="only-full">{{ monthFull }}</span>
            <span class="only-mobile">{{ monthMobile }}</span>
        </div>
        <div class="only-full">
            <span class="currency">{{ formatNum(this.data.default) }} ₽</span>
        </div>
        <div class="active-cell">
            <span class="currency" @click="editPayment">
                <payment-icon :payment-id="data.payment_id" />
                {{ formatNum(this.data.amount) }} ₽
            </span>
        </div>
        <div class="only-full">
            <span class="currency">{{ formatNum(this.data.interest) }} ₽</span>
        </div>
        <div class="only-full">
            <span class="currency">{{ formatNum(this.data.redemption) }} ₽</span>
        </div>
        <div class="only-full">
            <span class="currency">{{ formatNum(this.data.total) }} ₽</span>
        </div>
        <div>
            <span class="currency">{{ formatNum(this.data.remainder) }} ₽</span>
        </div>
    </div>
</template>

<script>
import { format } from "date-fns";
import PaymentIcon from './payment-log.vue'

export default {
    components: {
        PaymentIcon,
    },
    props: {
        data: {
            type: Object,
            required: true
        },
        canPay: {
            type: Boolean,
            required: true
        }
    },
    methods: {
        formatNum(num) {
            return num.toLocaleString("ru-RU", { minimumFractionDigits: 0 });
        },
        editPayment() {
            this.$emit("payment", this.data);
        },
    },
    computed: {
        monthFull() {
            const r = /(\d{4})-(\d{2})/.exec(this.data.date);
            return r ? `${r[2]}.${r[1]}` : this.data.date;
        },
        monthMobile() {
            const r = /\d{2}(\d{2})-(\d{2})/.exec(this.data.date);
            return r ? `${r[2]}.${r[1]}` : this.data.date;
        },
        monthClass() {
            const today = format(new Date(), "yyyy-MM");
            const payed = this.data.amount > 0;
            return (
                today < this.data.date ? "future" : (
                    today > this.data.date ? (payed ? "success" : "danger") : "current"
                )
            );
        },
    },
    watch: {
    },
};
</script>

<style scoped>
.only-mobile {
    display: none !important;
}
.vtr {
    display: flex;
    flex-direction: row;
    flex: 1 1 100%;
}
.vtr > div {
    flex: 0 0 170px;
    overflow: hidden;
    padding: 0 6px;
    box-sizing: border-box;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}
.vtr {
    background-color: #4646b905;
    color: #000072;
}
.vtr:nth-child(odd) {
    background-color: #4646b911;
}
.vtr.current {
    background-color: #dae1f2;
}
.vtr.danger {
    background-color: #ff5d1d05;
    color: #e24320;
}
.vtr:nth-child(odd).danger {
    background-color: #ff5d1d11;
}
.vtr.success {
    background-color: #57c13405;
    color: #1b6e00;
}
.vtr:nth-child(odd).success {
    background-color: #57c13411;
}
.vtr > div:nth-child(1) {
    flex: 0 0 100px;
    padding-left: 1.5rem;
    justify-content: flex-start;
}
.vtr > div:nth-child(7) {
    padding-right: calc(1.5rem - 5px);
    flex: 1 1 auto;
}
.active-cell > span {
    display: flex;
    border: 1px solid #00007240;
    border-radius: 5px;
    margin: 4px 0;
    flex: 1 1 auto;
    height: calc(100% - 8px);
    cursor: pointer;
    align-items: center;
    justify-content: flex-end;
    padding: 0 8px;
    position: relative;
}
.active-cell > span:hover {
    background: #00007240;
}
.active-cell > span >>> i {
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
    position: absolute;
    top: 4px;
    left: 8px;
}
.active-cell > span:hover >>> i {
    opacity: 1;
    visibility: visible;
}
.vtr.success .active-cell > span {
    border: 1px solid #1b6e0040;
}
.vtr.success .active-cell > span:hover {
    background: #1b6e0040;
}
.vtr.danger .active-cell > span {
    border: 1px solid #e2432040;
}
.vtr.danger .active-cell > span:hover {
    background: #e2432040;
}

@media (max-width: 1201px) {
    .vtr > div {
        flex: 0 0 165px;
    }
    .vtr > div:nth-child(1) {
        flex: 0 0 95px;
    }
}

@media (max-width: 993px) {
    .vtr > div {
        flex: 0 0 115px;
    }
    .vtr > div:nth-child(1) {
        flex: 0 0 80px;
    }

}

@media (max-width: 769px) {
    .vtr > div {
        flex: 0 0 100px;
    }
    .vtr > div:nth-child(1) {
        flex: 0 0 100px;
    }
    .vtr > div:nth-child(3) {
        flex: 0 0 110px;
    }
    .vtr > div:nth-child(4) {
        display: none;
    }

}

@media (max-width: 577px) {
    .only-full {
        display: none !important;
    }
    .only-mobile {
        display: inline !important;
    }
    .vtr > div:nth-child(3) {
        flex: 1 1 100px;
    }
    .vtr > div:nth-child(7) {
        flex: 0 0 120px;
    }
}
</style>