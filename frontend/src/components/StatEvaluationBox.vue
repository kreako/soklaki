<template>
  <router-link
    :to="link"
    :class="{
      'bg-gray-500': status === 'Empty',
      'bg-red-500': status === 'NotAcquired',
      'bg-yellow-500': status === 'InProgress',
      'bg-green-500': status === 'Acquired',
      'bg-pink-500': status === 'TipTop',
    }"
    class="w-5 h-5 rounded-md align-middle block mx-auto"
  ></router-link>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  link: String,
  status: String,
});
</script>
