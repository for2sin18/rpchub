<template>
  <section class="panel">
    <header class="panel-header">
      <h2>{{ title }}</h2>
      <button type="button" @click="$emit('refresh')">刷新</button>
    </header>
    <ul class="service-list">
      <li
        v-for="service in services"
        :key="service.name"
        @click="$emit('select', service)"
      >
        <strong>{{ service.name }}</strong>
        <small>{{ service.module }}</small>
      </li>
    </ul>
  </section>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  services: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.panel {
  border: 1px solid #dedede;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.service-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.service-list li {
  border-bottom: 1px solid #f0f0f0;
  padding: 0.75rem 0;
  cursor: pointer;
}

.service-list li:last-child {
  border-bottom: none;
}

.service-list strong {
  display: block;
}

.service-list small {
  color: #666;
}
</style>
