<template>
    <div class="row">
        <div class="col pt-4">
            <div class="summary">
                <p>
                    <span class="text-success">{{ formatInt(selection.amount) }}</span>₽ под 
                    <span class="text-success">{{ formatFloat(selection.rate) }}</span>% от 
                    <span class="text-success">{{ formatDate(selection.date) }}</span>
                <br>
                    Платеж (исходный): 
                    <span class="text-success">{{ details ? formatInt(details.default_payment) : "-" }}</span>₽
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        selection: Object,
        details: Object,
    },
    methods: {
        formatDate(date) {
            const dt = new Date(date);
            return dt.toLocaleDateString("ru-RU");
        },
        formatInt(num) { return num.toLocaleString("ru-RU"); },
        formatFloat(num) { return num.toLocaleString("ru-RU", { minimumFractionDigits: 2 }); },
    },
};
</script>

<style scoped>
.summary {
    background: #fff;
    padding: 1rem 1.5rem;
    color: #8a8abe;
}
.summary > p:last-child {
    margin-bottom: 0;
}
</style>