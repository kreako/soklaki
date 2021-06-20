<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <slot></slot>
  </div>
</template>

<script setup>
const props = defineProps({
  loading: Boolean,
});
</script>
