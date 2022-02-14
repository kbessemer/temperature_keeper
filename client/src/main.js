import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import vuetify from '@/plugins/vuetify';
import VueApexCharts from 'vue-apexcharts';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VueApexCharts);

Vue.component('apexchart', VueApexCharts);

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
