<template>
  <div
    v-if="enable"
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
    <div class="absolute top-14 left-6 right-0 flex justify-center items-end">
      <div class="text-7xl text-teal-500">
        {{ value }}
      </div>
      <div class="text-2xl text-teal-700">%</div>
    </div>
  </div>
  <div
    v-else
    class="
      bg-gray-100
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
        text-sm text-gray-400
        font-bold
        flex
        justify-center
      "
    >
      {{ label }}
    </div>
    <div
      class="absolute top-14 inset-x-0 right-0 flex justify-center items-end"
    >
      <div class="text-7xl text-gray-200">_</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  label: String,
  value: Number,
  enable: Boolean,
});
</script>
