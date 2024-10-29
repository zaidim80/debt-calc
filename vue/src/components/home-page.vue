<template>
    <div class="container">
        <ul class="nav nav-tabs">
            <li
                class="nav-item"
                v-for="d in debts"
                :key="d.id"
            >
                <a
                    href="#"
                    class="nav-link"
                    @click.prevent="() => { selectedDebt = d.id }"
                    :class="{ 'active': d.id == selectedDebt }"
                >
                    {{ d.name }}
                </a>
            </li>
        </ul>
        <div class="tab-content">
            <div id="vaulina" class="tab-pane active pt-4">
                <p>
                    <strong>
                        <span class="only-full">500&nbsp;000,00&nbsp;₽</span>
                        <span class="only-mobile">500000₽</span> под 7,5%
                    </strong>
                </p>
                <p>Платеж (исходный): 
                    <span class="only-full">10&nbsp;000&nbsp;₽</span>
                    <span class="only-mobile">10000₽</span>
                </p>
                <div class="table-responsive table-payments">
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
main > .container {
    padding: 96px 15px 0;
}
</style>

<script>
export default {
    computed: {},
    data() {
        return {
            debts: [
                {
                    id: 1,
                    name: "Дом-В",
                    amount: 500000,
                    period: 60,
                    date: "01.01.2019",
                    rate: 7.5,
                },
                {
                    id: 2,
                    name: "Дом-З",
                    amount: 1200000,
                    period: 90,
                    date: "01.01.2019",
                    rate: 7,
                },
            ],
            selectedDebt: null,
        };
    },
    created() {
        this.selectedDebt = this.debts[0].id;
    },
};
</script>
