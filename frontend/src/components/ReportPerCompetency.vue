<template>
  <div v-if="evaluation">
    <div class="flex flex-row items-center">
      <div class="font-serif flex-grow">
        <div
          v-if="evaluation.status === 'NotAcquired'"
          class="flex flex-row items-center space-x-4"
        >
          <div>Maîtrise insuffisante</div>
          <div class="bg-red-800 h-1 w-3"></div>
        </div>
        <div
          v-else-if="evaluation.status === 'InProgress'"
          class="flex flex-row items-center space-x-4"
        >
          <div>Maîtrise fragile</div>
          <div class="bg-yellow-500 h-1 w-3"></div>
        </div>
        <div
          v-else-if="evaluation.status === 'Acquired'"
          class="flex flex-row items-center space-x-4"
        >
          <div>Maîtrise satisfaisante</div>
          <div class="bg-green-800 h-1 w-3"></div>
        </div>
        <div
          v-else-if="evaluation.status === 'TipTop'"
          class="flex flex-row items-center space-x-4"
        >
          <div>Très bonne maîtrise</div>
          <div class="bg-green-500 h-1 w-3"></div>
        </div>
        <div v-else class="flex flex-row items-center space-x-4">
          <div>Non évalué</div>
          <div class="bg-blue-800 h-1 w-3"></div>
        </div>
      </div>
      <div v-if="observations > 1" class="text-sm">
        {{ observations }} observations
      </div>
      <div v-else-if="observations === 1" class="text-sm">1 observation</div>
    </div>
    <div class="whitespace-pre-line">
      {{ evaluation.comment }}
    </div>
  </div>
  <div v-else class="flex flex-row items-center space-x-4">
    <div>Non évalué</div>
    <div class="bg-blue-800 h-1 w-3"></div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  evaluation: Object,
  observations: Number,
});
</script>
