<template>
  <div class="group flex flex-row items-center space-x-2">
    <div
      v-if="kind === 'container1'"
      class="uppercase tracking-wide text-gray-700"
    >
      {{ object.rank }}.
      {{ object.text }}
    </div>
    <div v-else-if="kind === 'container2'" class="text-gray-700">
      {{ object.rank }}.
      {{ object.text }}
    </div>
    <div v-else class="">
      {{ object.rank }}.
      {{ object.text }}
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
  socle: Object,
  objectId: Number,
  kind: String,
});

const emit = defineEmit(["edit"]);

const object = computed(() => {
  if (props.kind === "competency") {
    return props.socle.competencies[props.objectId];
  } else {
    return props.socle.containers[props.objectId];
  }
});

const edit = () => {
  emit("edit");
};
</script>
