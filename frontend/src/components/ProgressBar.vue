<template>
  <div ref="main" class="mr-4 w-full h-5 bg-gray-200 relative">
    <div
      :style="`width: ${width}px`"
      class="absolute left-0 top-1 h-3 bg-teal-700"
    ></div>
    <div v-if="label != null" class="absolute right-1 text-gray-700 text-sm">
      {{ label }}
    </div>
  </div>
</template>
<script setup>
import { defineProps, computed, ref, watch } from "vue";
import { useElementSize } from "@vueuse/core";

const props = defineProps({
  current: Number,
  total: Number,
  label: {
    type: String,
    default: null,
  },
});

const main = ref(null);

const width = computed(() => {
  if (main.value == null) {
    return 3;
  }
  if (props.total == 0) {
    // divide by 0 ?
    return 3;
  }
  const mainWidth = main.value.getBoundingClientRect().width;
  let w = Math.floor((props.current * mainWidth) / props.total);
  if (w < 3) {
    w = 3;
  }
  return w;
});
</script>
