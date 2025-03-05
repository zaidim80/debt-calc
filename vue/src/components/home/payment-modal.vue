<template>
    <div class="modal-overlay" v-if="show" @click.self="close">
        <div class="modal-window">
            <div class="modal-header">
                <h5>Добавить платёж</h5>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="submit">
                    <div class="mb-3">
                        <label class="form-label">Сумма платежа</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            v-model="form.amount"
                            step="0.01"
                            required
                        >
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Дата платежа</label>
                        <input 
                            type="date" 
                            class="form-control" 
                            v-model="form.payment_date"
                            required
                        >
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Комментарий</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            v-model="form.description"
                        >
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="close">Отмена</button>
                        <button type="submit" class="btn btn-primary">Сохранить</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        show: Boolean,
        debtId: Number,
        payment: Object,
    },
    data() {
        return {
            form: {
                amount: null,
                payment_date: new Date().toISOString().split("T")[0],
                description: "",
            }
        }
    },
    methods: {
        close() {
            this.$emit('update:show', false);
        },
        async submit() {
            try {
                await this.$axios.post('/payment/', {
                    debt_id: this.debtId,
                    ...this.form
                });
                this.close();
                this.$emit('payment-added');
            } catch (error) {
                console.error('Ошибка при создании платежа:', error);
                // Здесь можно добавить обработку ошибок
            }
        }
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
</style> 