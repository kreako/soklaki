<template>
  <div class="relative">
    <select
      v-model="choice"
      class="appearance-none block bg-transparent py-1 pr-3 text-gray-500 font-medium text-sm focus:outline-none focus:text-gray-900 transition-colors duration-200"
    >
      <option v-for="option in options" :value="option.value">
        {{ option.text }}
      </option>
    </select>
    <IconChevronDown
      class="h-4 absolute top-1/2 right-0 -mt-2 pointer-events-none"
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref, computed } from "vue";
import IconChevronDown from "../icons/IconChevronDown.vue";

const props = defineProps({
  modelValue: String,
  options: Array,
});

const emit = defineEmit(["update:modelValue"]);

const choice = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>
