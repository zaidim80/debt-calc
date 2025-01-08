<template>
    <div class="vtr" :class="monthClass">
        <div>
            <span class="only-full">{{ monthFull }}</span>
            <span class="only-mobile">{{ monthMobile }}</span>
        </div>
        <div class="only-full">
            <span class="currency">{{ formatNum(this.data.default) }} ₽</span>
        </div>
        <div>
            <span class="currency">{{ formatNum(this.data.amount) }} ₽</span>
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

export default {
    props: {
        data: Object,
    },
    methods: {
		formatNum(num) {
			return num.toLocaleString('ru-RU', { minimumFractionDigits: 0 });
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
	color: #882700;
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