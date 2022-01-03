<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Les Évaluations du cycle {{ cycle }}</div>
      <div class="my-8 flex flex-row justify-center">
        <div>
          <router-link
            :to="`/evaluation/${route.params.cycle}/${stats.first_competency}`"
            class="button-main-action"
          >
            Démarrer une évaluation
          </router-link>
        </div>
      </div>
      <div class="mt-4">
        <div v-for="by_competency in stats.competencies">
          <router-link
            :to="`/evaluation/${route.params.cycle}/${by_competency.competency.id}`"
          >
            <div class="flex flex-row items-center space-x-2">
              <div class="w-20">
                {{ by_competency.competency.full_rank }}
              </div>
              <ProgressBar
                :current="by_competency.count"
                :total="stats.total"
              />
              <div class="text-gray-700 text-xs">
                {{ by_competency.count }}/{{ stats.total }}
              </div>
            </div>
          </router-link>
        </div>
      </div>
      <div class="mt-4">
        <router-link :to="`/evaluation/${route.params.cycle}/comment`">
          <div class="flex flex-row items-center space-x-2">
            <div>Commentaire</div>
            <ProgressBar :current="stats.comment_count" :total="stats.total" />
            <div class="text-gray-700 text-xs">
              {{ stats.comment_count }}/{{ stats.total }}
            </div>
          </div>
        </router-link>
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { cycleNb } from "../utils/cycle";
import ProgressBar from "../components/ProgressBar.vue";
import { useTitle } from "@vueuse/core";
import Loading from "../components/Loading.vue";

const store = useStore();
const route = useRoute();

useTitle(`Évaluations ${route.params.cycle} - soklaki.fr`);

const loading = ref(true);
const stats = ref(null);

const cycle = computed(() => cycleNb(route.params.cycle));

const getStats = async () => {
  if (route.params.cycle == null) {
    // Of course
    return;
  }
  loading.value = true;
  const data = await store.dispatch("evaluationStatsByCycle", {
    cycle: route.params.cycle,
  });
  stats.value = data;
  loading.value = false;
};

watch(
  () => route.params.cycle,
  async () => {
    await getStats();
  }
);

onMounted(async () => {
  await getStats();
});
</script>
