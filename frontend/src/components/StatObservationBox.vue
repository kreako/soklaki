<template>
  <router-link
    :to="link"
    :class="observations > 0 ? 'bg-green-500' : 'bg-gray-500'"
    class="w-5 h-5 rounded-md block mx-auto"
  >
    <div class="flex items-center justify-center h-full text-xs">
      {{ observations }}
    </div>
  </router-link>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  link: String,
  observations: Number,
});
</script>
