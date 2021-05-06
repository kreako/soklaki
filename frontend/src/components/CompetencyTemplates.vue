<template>
  <div v-if="templates.length > 0" class="group">
    <div v-for="template in templates" class="text-sm text-gray-700">
      {{ templateById(template.id).text }}
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
  templates: Array,
});
const emit = defineEmit(["edit"]);

const templateById = computed(() => store.getters.templateById);
const edit = () => {
  emit("edit");
};
</script>
