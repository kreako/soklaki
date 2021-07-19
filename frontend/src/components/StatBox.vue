<template>
  <div
    class="
      bg-gray-800
      h-40
      border-2 border-gray-200
      shadow-2xl
      rounded-xl
      p-2
      relative
    "
  >
    <div
      class="
        absolute
        top-0
        inset-x-0
        text-sm text-white
        font-bold
        flex
        justify-center
      "
    >
      {{ label }}
    </div>
    <div class="absolute top-14 inset-x-0 flex justify-center items-end">
      <div class="text-7xl text-pink-500">
        {{ value }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  label: String,
  value: Number,
});
</script>
