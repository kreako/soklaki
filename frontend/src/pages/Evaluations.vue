<template>
  <div class="my-4 px-2">
    <div class="form-label">Les Évaluations</div>
    <div class="mt-8">
      <router-link to="/evaluations-by-cycle/c1">
        <div class="form-sub-label">Cycle 1</div>
        <EvalSummaryStats :stats="stats.c1" class="mt-2" />
      </router-link>
    </div>
    <div class="mt-8">
      <router-link to="/evaluations-by-cycle/c2">
        <div class="form-sub-label">Cycle 2</div>
        <EvalSummaryStats :stats="stats.c2" class="mt-2" />
      </router-link>
    </div>
    <div class="mt-8">
      <router-link to="/evaluations-by-cycle/c3">
        <div class="form-sub-label">Cycle 3</div>
        <EvalSummaryStats :stats="stats.c3" class="mt-2" />
      </router-link>
    </div>
    <div class="mt-8">
      <router-link to="/evaluations-by-cycle/c4">
        <div class="form-sub-label">Cycle 4</div>
        <EvalSummaryStats :stats="stats.c4" class="mt-2" />
      </router-link>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import EvalSummaryStats from "../components/EvalSummaryStats.vue";

const store = useStore();

const stats = computed(() => store.state.statsSummary);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("statsSummary", { periodId: store.state.currentPeriod });
});
</script>
