<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Les Évaluations</div>
      <div v-if="stats.c1.student_count > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c1">
          <div class="form-sub-label">Cycle 1</div>
          <EvalSummaryStats :stats="stats.c1" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c2.student_count > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c2">
          <div class="form-sub-label">Cycle 2</div>
          <EvalSummaryStats :stats="stats.c2" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c3.student_count > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c3">
          <div class="form-sub-label">Cycle 3</div>
          <EvalSummaryStats :stats="stats.c3" class="mt-2" />
        </router-link>
      </div>
      <div v-if="stats.c4.student_count > 0" class="mt-8">
        <router-link to="/evaluations-by-cycle/c4">
          <div class="form-sub-label">Cycle 4</div>
          <EvalSummaryStats :stats="stats.c4" class="mt-2" />
        </router-link>
      </div>
    </Loading>
  </div>
</template>
<script setup>
import { onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useTitle } from "@vueuse/core";
import EvalSummaryStats from "../components/EvalSummaryStats.vue";
import Loading from "../components/Loading.vue";

useTitle("Évaluations - soklaki.fr");

const store = useStore();

const loading = ref(true);
const stats = ref(null);

const getStats = async () => {
  loading.value = true;
  const data = await store.dispatch("evaluationStatsSummary");
  stats.value = data;
  loading.value = false;
};

onMounted(async () => {
  await getStats();
});
</script>
