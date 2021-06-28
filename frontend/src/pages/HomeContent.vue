<template>
  <div class="my-4 px-2">
    <div class="form-label">Quelques statistiques...</div>
    <div v-if="stats.incompleteObservationsCount > 0" class="mt-4">
      <router-link
        :to="{
          path: '/observations',
          query: { limit: 50, offset: 0, filter: 'incomplete' },
        }"
      >
        <span class="text-xl">
          {{ stats.incompleteObservationsCount }}
        </span>
        <span v-if="stats.incompleteObservationsCount > 1">
          observations incomplètes
        </span>
        <span v-else> observation incomplète </span>
      </router-link>
    </div>
    <div v-else class="mt-4">
      <router-link to="/observations">
        Pas d'observations incomplètes ! 👍
      </router-link>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
      <router-link to="/stats/c1">
        <div class="mt-12 md:mt-0 flex flex-row items-center space-x-4">
          <div class="text-xs text-gray-700 uppercase tracking-wide font-bold">
            Cycle 1
          </div>
          <div class="text-xs text-gray-500">(+ de détails)</div>
        </div>
        <div class="mt-2">
          <StatsSummary :stats="stats.c1" />
        </div>
      </router-link>
      <router-link to="/stats/c2">
        <div class="mt-12 md:mt-0 flex flex-row items-center space-x-4">
          <div class="text-xs text-gray-700 uppercase tracking-wide font-bold">
            Cycle 2
          </div>
          <div class="text-xs text-gray-500">(+ de détails)</div>
        </div>
        <div class="mt-2">
          <StatsSummary :stats="stats.c2" />
        </div>
      </router-link>
      <router-link to="/stats/c3">
        <div class="mt-12 md:mt-0 flex flex-row items-center space-x-4">
          <div class="text-xs text-gray-700 uppercase tracking-wide font-bold">
            Cycle 3
          </div>
          <div class="text-xs text-gray-500">(+ de détails)</div>
        </div>
        <div class="mt-2">
          <StatsSummary :stats="stats.c3" />
        </div>
      </router-link>
      <router-link to="/stats/c4">
        <div class="mt-12 md:mt-0 flex flex-row items-center space-x-4">
          <div class="text-xs text-gray-700 uppercase tracking-wide font-bold">
            Cycle 4
          </div>
          <div class="text-xs text-gray-500">(+ de détails)</div>
        </div>
        <div class="mt-2">
          <StatsSummary :stats="stats.c4" />
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until, useTitle } from "@vueuse/core";
import StatsSummary from "../components/StatsSummary.vue";

useTitle("Accueil - soklaki.fr");

const store = useStore();

const stats = computed(() => store.state.statsSummary);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("statsSummary", { periodId: store.state.currentPeriod });
});
</script>
