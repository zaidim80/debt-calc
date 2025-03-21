<template>
    <div class="modal fade" tabindex="-1" ref="modal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Платеж</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submit">
                        <div class="row mb-3">
                            <label class="col-sm-6 col-form-label">Сумма платежа</label>
                            <div class="col-sm-6">
                                <input 
                                    type="text" 
                                    class="form-control text-end" 
                                    v-model="form.amount"
                                    required
                                    ref="amountInput"
                                    @keyup.enter="() => {if (valid) submit();}"
                                >
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-6 col-form-label">Месяц выплаты</label>
                            <div class="col-sm-6">
                                <input 
                                    type="text" 
                                    class="form-control text-end" 
                                    v-model="form.month"
                                    disabled
                                >
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="close">Отмена</button>
                    <button
                        type="submit"
                        class="btn btn-success"
                        @click="submit"
                        :disabled="!valid"
                    >Сохранить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
import axios from "axios";

export default {
    props: {
        debtId: Number,
        payment: Object,
    },
    data() {
        return {
            token: sessionStorage.getItem("token"),
            form: {
                amount: null,
                month: null,
            }
        }
    },
    mounted() {
        this.modal = new Modal(this.$refs.modal);
        this.$refs.modal.addEventListener("shown.bs.modal", () => {
            this.form = {
                amount: this.payment.amount,
                month: this.payment.date,
            }
            this.$refs.amountInput.focus();
            this.$refs.amountInput.select();
        });
    },
    computed: {
        valid() {
            return this.form.amount && this.isInt(this.form.amount) && this.form.amount > 0;
        }
    },
    methods: {
        isInt(value) {
            return !isNaN(value) && (function(x) { return (x | 0) === x; })(parseFloat(value));
        },
        close() {
            this.modal.hide();
        },
        async submit() {
            try {
                const response = await axios.post(
                    `/api/debt/${this.debtId}/pay`, 
                    { ...this.form },
                    { headers: { Authorization: `Bearer ${this.token}` }},
                );
                this.$emit("payment-added", response.data);
                this.$showToast(
                    "Информация о платеже успешно записана",
                    { type: "success", autohide: true },
                );
            } catch (error) {
                console.error("Ошибка при создании платежа:", error);
                this.$showToast(
                    "Ошибка при создании платежа: " + error,
                    { type: "error", autohide: true },
                );
            }
            this.close();
        },
        show() {
            this.modal.show();
        },
    }
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-window {
    background: white;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.modal-header {
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body {
    padding: 1rem;
}

.modal-footer {
    padding: 1rem;
    border-top: 1px solid #dee2e6;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
}
.modal-footer button.btn-success {
    background-color: #57c134;
    border-color: #57c134;
}
.modal-footer button.btn-success:hover {
    background-color: #47a12a;
    border-color: #47a12a;
}
.modal-footer button.btn-secondary {
    background-color: #dae1f2;
    border-color: #dae1f2;
    color: #000072;
}
.modal-footer button.btn-secondary:hover {
    background-color: #c2d5e9;
    border-color: #c2d5e9;
}
</style> 