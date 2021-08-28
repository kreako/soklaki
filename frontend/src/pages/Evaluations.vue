<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Les Évaluations</div>
      <div v-if="stats.c1.studentsCount > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c1">
          <div class="form-sub-label">Cycle 1</div>
          <EvalSummaryStats :stats="stats.c1" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c2.studentsCount > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c2">
          <div class="form-sub-label">Cycle 2</div>
          <EvalSummaryStats :stats="stats.c2" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c3.studentsCount > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c3">
          <div class="form-sub-label">Cycle 3</div>
          <EvalSummaryStats :stats="stats.c3" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c4.studentsCount > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c4">
          <div class="form-sub-label">Cycle 4</div>
          <EvalSummaryStats :stats="stats.c4" class="mt-2" />
        </router-link>
      </div>
    </Loading>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import { useTitle } from "@vueuse/core";
import EvalSummaryStats from "../components/EvalSummaryStats.vue";
import Loading from "../components/Loading.vue";

useTitle("Évaluations - soklaki.fr");

const store = useStore();

const stats = computed(() => store.state.statsSummary);
const loading = ref(true);

onMounted(async () => {
  loading.value = true;
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("statsSummary", { periodId: store.state.currentPeriod });
  loading.value = false;
});
</script>
