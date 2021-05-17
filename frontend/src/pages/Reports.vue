<template>
  <div class="my-4 px-2">
    <div class="form-label">Les rapports</div>
    <div v-for="periodId in sortedPeriods" class="mt-12">
      <div class="form-sub-label">
        {{ periodById(periodId).name }}
      </div>
      <router-link :to="`/reports-by-period/${periodId}`">
        <div class="flex flex-row mt-2 space-x-4 hover:text-teal-500">
          <div>{{ periodById(periodId).students.length }} Élèves</div>
          <div>
            {{ reportsNbPerPeriods[periodId] }}
            <span v-if="reportsNbPerPeriods[periodId] > 1">Rapports</span>
            <span v-else>Rapport</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import { useTitle } from "@vueuse/core";

useTitle("Rapports - soklaki.fr");

const store = useStore();

const sortedPeriods = computed(() => store.state.sortedPeriods);
const periodById = computed(() => store.getters.periodById);
const studentById = computed(() => store.getters.studentById);

/// return {period_id: count}
const reportsNbPerPeriods = computed(() => {
  const reports = {};
  for (const periodId of store.state.sortedPeriods) {
    if (periodId in store.state.reports.sorted) {
      reports[periodId] = store.state.reports.sorted.length;
    } else {
      reports[periodId] = 0;
    }
  }
  return reports;
});

onMounted(async () => {
  await store.dispatch("reports");
});
</script>
