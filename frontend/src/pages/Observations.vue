<template>
  <div class="mt-4 px-2">
    <div>Observations</div>
    <div>
      <div v-for="observationId in sortedObservations">
        {{ observations[observationId].date }}
        {{ observations[observationId].text }}
      </div>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { computed, ref, onMounted, watch } from "vue";

const store = useStore();

const observations = computed(() => store.state.observations);
const sortedObservations = computed(
  () => store.state.sortedCreatedAtObservations
);
onMounted(() => {
  store.dispatch("observations", { limit: 4, offset: 0 });
});
</script>
