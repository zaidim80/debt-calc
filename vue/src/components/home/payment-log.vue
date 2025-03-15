<template>
    <i class="bi bi-receipt" ref="log" title="<i class='bi bi-arrow-repeat'></i>"></i>
</template>

<script>
import { format } from "date-fns";
import { Tooltip } from "bootstrap";
import axios from "axios";

export default {
    props: {
        paymentId: {
            type: Number,
            default: null,
        },
    },
    data() {
        return {
            token: sessionStorage.getItem("token"),
            tooltip: null,
            calledHistory: false,
        }
    },
    async mounted() {
        this.tooltip = new Tooltip(this.$refs.log, { html: true });
        this.$refs.log.addEventListener("shown.bs.tooltip", async () => {
            if (!this.calledHistory) {
                this.calledHistory = true;
                setTimeout(() => {this.calledHistory = false}, 5000);
                if (this.paymentId) {
                    this.tooltip.setContent({ '.tooltip-inner': '<i class="bi bi-arrow-repeat"></i>' });
                    try {
                        const response = await axios.get(
                            `/api/payment/${this.paymentId}/history`, 
                            { headers: { Authorization: `Bearer ${this.token}` }},
                        );
                        if (response.data.length > 0) {
                            this.tooltip.setContent({ '.tooltip-inner': this.formatHitory(response.data) });
                        } else {
                            this.tooltip.setContent({ '.tooltip-inner': 'нет истории платежей' });
                        }
                    } catch (error) {
                        this.tooltip.setContent({ '.tooltip-inner': String(error) });
                    }
                } else {
                    this.tooltip.setContent({ '.tooltip-inner': 'нет платежей' });
                }
            }
        });
    },
    methods: {
        formatNum(num) {
            return num.toLocaleString("ru-RU", { minimumFractionDigits: 0 });
        },
        formatDate(date) {
            return format(new Date(date), "dd.MM.yyyy");
        },
        logItemHtml(item) {
            return `<div class="history-item">` +
                `<span class="history-date">${this.formatDate(item.date)}</span>` +
                `<span class="history-amount">${this.formatNum(item.amount)} ₽</span>` +
                `<span class="history-author">${item.author.name}</span>` +
            `</div>`
        },
        formatHitory(history) {
            return history.map(this.logItemHtml).join("\n");
        },
    },
}
</script>

<style>
.tooltip-inner {
    min-width: 100px;
    max-width: 300px;
    overflow: hidden;
}
.tooltip-inner i.bi.bi-arrow-repeat:before {
    animation: spin-icon 1s linear infinite;
}
.tooltip-inner .history-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    flex-wrap: nowrap;
    white-space: nowrap;
    overflow: hidden;
    min-width: 300px;
}
.tooltip-inner .history-date {
    flex: 0 0 80px;
    text-align: left;
}
.tooltip-inner .history-amount {
    flex: 0 0 80px;
    text-align: right;
}
.tooltip-inner .history-author {
    flex: 0 0 140px;
    text-align: left;
    padding-left: 8px;
}

@keyframes spin-icon {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
