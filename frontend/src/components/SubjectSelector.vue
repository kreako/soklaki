<template>
  <div class="grid grid-cols-1 max-h-46 overflow-y-auto mt-2 bg-gray-50">
    <div
      v-for="subject in subjects"
      :key="subject.id"
      class="px-2 flex flex-row items-center gap-2"
    >
      <button class="group flex flex-row" @click="$emit('select', subject.id)">
        <IconPlusCircle
          class="w-4 text-gray-300 group-hover:text-gray-600 mr-2"
        />
        <div>{{ subject.title }}</div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmit, defineProps, ref, computed } from "vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

defineEmit(["select"]);

const props = defineProps({
  subjects: Array,
});
</script>
