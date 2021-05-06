<template>
  <div class="my-4 px-2">
    <div class="form-label">Quelques statistiques...</div>
    <div class="mt-4">
      <router-link
        :to="{
          path: '/observations',
          query: { limit: 50, offset: 0, filter: 'incomplete' },
        }"
      >
        <span class="text-xl">
          {{ stats.incompleteObservationsCount }}
        </span>
        <span> observations incomplètes </span>
      </router-link>
    </div>
    <router-link to="/stats/c1">
      <div class="mt-12 flex flex-row items-center space-x-4">
        <div class="form-sub-label">Cycle 1</div>
        <div class="text-xs text-gray-500">(+ de détails)</div>
      </div>
      <div class="mt-2">
        <StatsSummary :stats="stats.c1" />
      </div>
    </router-link>
    <router-link to="/stats/c2">
      <div class="mt-12 flex flex-row items-center space-x-4">
        <div class="form-sub-label">Cycle 2</div>
        <div class="text-xs text-gray-500">(+ de détails)</div>
      </div>
      <div class="mt-2">
        <StatsSummary :stats="stats.c2" />
      </div>
    </router-link>
    <router-link to="/stats/c3">
      <div class="mt-12 flex flex-row items-center space-x-4">
        <div class="form-sub-label">Cycle 3</div>
        <div class="text-xs text-gray-500">(+ de détails)</div>
      </div>
      <div class="mt-2">
        <StatsSummary :stats="stats.c3" />
      </div>
    </router-link>
    <router-link to="/stats/c4">
      <div class="mt-12 flex flex-row items-center space-x-4">
        <div class="form-sub-label">Cycle 4</div>
        <div class="text-xs text-gray-500">(+ de détails)</div>
      </div>
      <div class="mt-2">
        <StatsSummary :stats="stats.c4" />
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import StatsSummary from "../components/StatsSummary.vue";

const store = useStore();

const stats = computed(() => store.state.statsSummary);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("statsSummary", { periodId: store.state.currentPeriod });
});
</script>
