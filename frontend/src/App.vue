<template>
  <main class="layout">
    <header>
      <h1>RPC Hub Dashboard</h1>
      <p class="subtitle">低耦合，高扩展的模块化平台示例</p>
    </header>
    <section class="grid">
      <ServiceList
        title="已注册服务"
        :services="services"
        @select="handleServiceSelect"
        @refresh="fetchServices"
      />
      <section class="panel">
        <h2>{{ activeService?.name ?? '选择一个服务' }}</h2>
        <div v-if="activeService" class="service-details">
          <p><strong>模块:</strong> {{ activeService.module }}</p>
          <p><strong>权限:</strong> {{ activeService.permissions.join(', ') || '公开' }}</p>
          <pre>{{ activeService.config }}</pre>
        </div>
        <div v-else class="placeholder">请选择一个服务查看详情。</div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import ServiceList from './components/ServiceList.vue'

const services = ref([])
const activeService = ref(null)

async function fetchServices() {
  const { data } = await axios.get('/api/services')
  services.value = data
}

function handleServiceSelect(service) {
  activeService.value = service
}

onMounted(() => {
  fetchServices()
})
</script>

<style scoped>
.layout {
  font-family: 'Segoe UI', sans-serif;
  padding: 2rem;
  color: #222;
}

header {
  margin-bottom: 2rem;
}

.subtitle {
  margin-top: 0.5rem;
  color: #666;
}

.grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr 2fr;
}

.panel {
  border: 1px solid #dedede;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
  min-height: 240px;
}

.service-details pre {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.placeholder {
  color: #999;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
