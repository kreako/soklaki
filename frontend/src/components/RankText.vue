<template>
  <div class="group flex flex-row items-center justify-start space-x-2">
    <div
      v-if="kind === 'container1'"
      class="uppercase tracking-wide text-gray-700 text-left"
    >
      {{ object.rank }}.
      {{ object.text }}
    </div>
    <div v-else-if="kind === 'container2'" class="text-gray-700 text-left">
      {{ object.rank }}.
      {{ object.text }}
    </div>
    <div v-else class="text-left">
      {{ object.rank }}.
      {{ object.text }}
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();

const props = defineProps({
  socle: Object,
  objectId: Number,
  kind: String,
});

const object = computed(() => {
  if (props.kind === "competency") {
    return props.socle.competencies[props.objectId];
  } else {
    return props.socle.containers[props.objectId];
  }
});
</script>
