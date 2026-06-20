<template>
  <section class="panel chart-panel">
    <div class="panel-title">{{ title }}</div>
    <div ref="chartRef" class="chart"></div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title: { type: String, required: true },
  option: { type: Object, required: true }
})

const chartRef = ref(null)
let chart = null

function renderChart() {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  chart.setOption(props.option, true)
}

onMounted(() => {
  renderChart()
  window.addEventListener('resize', renderChart)
})

watch(() => props.option, renderChart, { deep: true })
onBeforeUnmount(() => {
  window.removeEventListener('resize', renderChart)
  chart?.dispose()
})
</script>
