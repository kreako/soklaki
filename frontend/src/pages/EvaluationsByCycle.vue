<template>
  <div class="my-4 px-2">
    <div class="form-label">Les Évaluations du cycle {{ cycle }}</div>
    <div class="my-8 flex flex-row justify-center">
      <div>
        <router-link
          :to="`/evaluation/${route.params.cycle}/${firstCompetency}`"
          class="button-main-action"
        >
          Démarrer une évaluation
        </router-link>
      </div>
    </div>
    <div class="mt-4">
      <div v-for="stat in competencyStats">
        <router-link
          :to="`/evaluation/${route.params.cycle}/${stat.competencyId}`"
        >
          <div class="flex flex-row items-center space-x-2">
            <div class="w-20">
              {{ competencyById(stat.competencyId).full_rank }}
            </div>
            <ProgressBar :current="stat.current" :total="stat.total" />
            <div class="text-gray-700 text-xs">
              {{ stat.current }}/{{ stat.total }}
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <div class="mt-4">
      <router-link :to="`/evaluation/${route.params.cycle}/comment`">
        <div class="flex flex-row items-center space-x-2">
          <div>Commentaire</div>
          <ProgressBar
            :current="commentStats.current"
            :total="commentStats.total"
          />
          <div class="text-gray-700 text-xs">
            {{ commentStats.current }}/{{ commentStats.total }}
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { cycleNb } from "../utils/cycle";
import ProgressBar from "../components/ProgressBar.vue";

const store = useStore();
const route = useRoute();

const cycle = computed(() => cycleNb(route.params.cycle));

const commentStats = computed(() => {
  const stats = store.state.stats[route.params.cycle].commentsCount;
  const total = Object.keys(stats).length;
  const current = Object.values(stats).reduce(
    (acc, cur) => acc + (cur > 0 ? 1 : 0),
    0
  );
  return { total, current };
});

const competencyStats = computed(() => {
  const stats = [];
  for (const [competencyId, statByStudents] of Object.entries(
    store.state.stats[route.params.cycle].stats
  )) {
    const total = Object.keys(statByStudents).length;
    const current = Object.values(statByStudents).reduce(
      (acc, cur) => acc + (cur.evaluations.count > 0 ? 1 : 0),
      0
    );
    stats.push({
      competencyId: competencyId,
      total: total,
      current: current,
    });
  }
  return stats;
});

const firstCompetency = computed(() => {
  if (competencyStats.value.length > 0) {
    return competencyStats.value[0].competencyId;
  } else {
    return null;
  }
});

const competencyById = computed(() => store.getters.competencyById);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("stats", {
    periodId: store.state.currentPeriod,
  });
});
</script>
