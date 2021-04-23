<template>
  <div class="my-4 px-2">
    <div class="form-label">Plein de statistiques !</div>
    <div class="mt-4 form-sub-label">Cycle 1</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c1" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 2</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c2" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 3</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c3" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 4</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c4" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import StatsDetails from "../components/StatsDetails.vue";

const store = useStore();

const stats = computed(() => store.state.stats);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("stats", { periodId: store.state.currentPeriod });
});
</script>
