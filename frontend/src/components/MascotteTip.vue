<template>
    <div class="flex flex-col p-2 text-teal-900 text-sm sm:text-base" :class="{ bordered: border }">
        <div class="self-center flex flex-row items-center">
            <!--
            <Mascotte class="h-8 mr-4" />

            -->
            <div class="font-bold">
                <slot name="title"></slot>
            </div>
        </div>
        <div class="mt-2">
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'
import Mascotte from './Mascotte.vue'

defineProps({
  border: {
      type: Boolean,
      default: false,
  },
})
</script>

<style scoped>
.bordered {
    @apply border-teal-200 border rounded-md
}
</style>