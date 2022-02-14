<template>
<div>
  <apexchart type="bar" height="350" :options="chartOptions" :series="bargraphseries"></apexchart>
</div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts';

export default {
  name: 'BarGraph',
  props: ['bargraphseries'],
  data() {
    return {
      options: {
        chart: {
          id: 'vuechart-example',
        },
        xaxis: {
          categories: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        },
      },
      chartOptions: {
        chart: {
          type: 'bar',
          height: 350,
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded',
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent'],
        },
        xaxis: {
          categories: [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            '11',
            '12',
            '13',
            '14',
          ],
        },
        yaxis: {
          title: {
            text: 'Temperature',
          },
        },
        fill: {
          opacity: 1,
          colors: [
            function ({ value }) {
              if (value < 100.4) {
                return '#12DF44';
              }
              return '#EA0C0C';
            },
          ],
        },
        tooltip: {
          y: {
            formatter(val) {
              return val;
            },
          },
        },
      },
    };
  },
};
</script>
