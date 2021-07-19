<template>
  <div class="p-4 border-t border-b border-gray-800 rounded-xl">
    <router-link :to="`/stats/c${cycle}`">
      <div class="flex flex-row items-center space-x-4">
        <div class="text-xs text-gray-700 uppercase tracking-wide font-bold">
          Cycle {{ cycle }}
        </div>
        <div class="text-xs text-gray-500">(Encore + de détails)</div>
      </div>
      <div class="mt-2">
        <StatsSummary :stats="stats" />
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import StatsSummary from "../components/StatsSummary.vue";

const props = defineProps({
  cycle: Number,
  stats: Object,
});
</script>
