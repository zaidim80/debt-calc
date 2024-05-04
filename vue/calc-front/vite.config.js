import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    server: {
        port: 8001,
        host: true,
        watch: {usePolling: true},
    },
    plugins: [vue()],
});
