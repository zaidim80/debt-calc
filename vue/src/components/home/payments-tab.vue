<template>
    <div class="row for-table">
            <div class="col pt-4 pb-4 for-table">
                <div class="table-responsive table-payments">
                    <div class="vtable">
                        <div class="vthead">
                            <div class="vtr">
                                <div>Месяц</div> 
                                <div class="only-full">Рек.&nbsp;платеж</div>
                                <div>Выплата</div>
                                <div class="only-full">Проценты</div>
                                <div class="only-full">Погашение</div>
                                <div class="only-full">Сумма</div>
                                <div>Остаток</div>
                            </div>
                        </div>
                        <div class="vtbody" v-if="details">
                            <div class="wrapper">
                                <payment-row v-for="row in details.schedule" :id="row.id" :data="row" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script>
import PaymentRow from "./payment-row.vue";

export default {
    components: {
        PaymentRow,
    },
    props: {
        selection: Object,
        details: Object,
    },
    methods: {
    },
    watch: {
    },
};
</script>

<style scoped>
.for-table {
    display: flex;
    flex-direction: column;
    flex: 1 1 100%;
}
.table-responsive {
	flex: 1 1 100%;
	display: flex;
	flex-direction: column;
    background: #fff;
}
.only-mobile {
	display: none !important;
}
.vtable {
	display: flex;
	flex: 1 1 100%;
	flex-direction: column;
    padding: 1rem 0;
}
.vtable > .vthead {
	flex: 0 0 auto;
    color: #000072;
    font-weight: 500;
}
.vtable > .vtbody {
	flex: 1 1 100%;
	position: relative;
}
.vtable > .vtbody > .wrapper {
	overflow-y: scroll;
	display: block;
	position: absolute;
	left: 0;
	top: 0;
	right: 0;
	bottom: 0;
}
.vtable > .vtbody > .wrapper::-webkit-scrollbar {
    width: 5px !important;
    height: 5px !important;
}
.vtable > .vtbody > .wrapper::-webkit-scrollbar-track {
    background: #fff !important;
}
.vtable > .vtbody > .wrapper::-webkit-scrollbar-thumb {
    background-color: #dae1f2 !important;
    border: none !important;
    border-radius: 2px !important;
}
.vtable > .vthead > .vtr {
	display: flex;
	flex-direction: row;
	flex: 1 1 100%;
}
.vtable > .vthead > .vtr > div {
	flex: 0 0 170px;
	overflow: hidden;
	padding: 0 6px;
	box-sizing: border-box;
	height: 42px;
	display: flex;
	align-items: center;
	justify-content: flex-end;
}
.vtable > .vthead > .vtr > div:nth-child(1) {
	flex: 0 0 100px;
	padding-left: 1.5rem;
	justify-content: flex-start;
}
.vtable > .vthead > .vtr > div:nth-child(7) {
	padding-right: 1.5rem;
	flex: 1 1 auto;
}

@media (max-width: 1201px) {
	.vtable > .vthead > .vtr > div {
		flex: 0 0 165px;
	}
	.vtable > .vthead > .vtr > div:nth-child(1) {
		flex: 0 0 95px;
	}

}

@media (max-width: 993px) {
	.vtable > .vthead > .vtr > div {
		flex: 0 0 115px;
	}
	.vtable > .vthead > .vtr > div:nth-child(1) {
		flex: 0 0 80px;
	}

}

@media (max-width: 769px) {
	.vtable > .vthead > .vtr > div {
		flex: 0 0 100px;
	}
	.vtable > .vthead > .vtr > div:nth-child(1) {
		flex: 0 0 75px;
	}
	.vtable > .vthead > .vtr > div:nth-child(3) {
		flex: 0 0 110px;
	}
	.vtable > .vthead > .vtr > div:nth-child(4) {
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
	.vtable > .vthead > .vtr > div:nth-child(3) {
		flex: 1 1 100px;
	}
	.vtable > .vthead > .vtr > div:nth-child(7) {
		flex: 0 0 120px;
	}
}
</style>