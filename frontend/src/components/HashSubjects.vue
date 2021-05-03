<template>
  <div class="group flex flex-row space-x-2">
    <div v-for="subject in subjects" class="text-sm text-gray-700">
      #{{ subjectById(subject.subject_id).title }}
    </div>
    <button @click="edit" class="text-gray-200 group-hover:text-gray-700">
      <IconPencil class="hover:text-teal-500 h-3" />
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed } from "vue";
import { useStore } from "vuex";
import IconPencil from "../icons/IconPencil.vue";

const store = useStore();

const props = defineProps({
  subjects: Array,
});
const emit = defineEmit(["edit"]);

const subjectById = computed(() => store.getters.subjectById);
const edit = () => {
  emit("edit");
};
</script>
