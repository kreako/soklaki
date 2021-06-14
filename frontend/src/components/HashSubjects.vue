<template>
  <div v-if="subjects.length > 0" class="group flex flex-row space-x-2">
    <div v-for="subject in subjects" class="text-sm text-gray-700">
      #{{ subjectById(subject.subject_id).title }}
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();

const props = defineProps({
  subjects: Array,
});

const subjectById = computed(() => store.getters.subjectById);
</script>
