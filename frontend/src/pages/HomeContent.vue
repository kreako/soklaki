<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Quelques statistiques...</div>
      <div v-if="stats.incomplete_observations_count > 0" class="flex flex-row">
        <div class="flex-grow"></div>
        <div class="flex-grow-0">
          <router-link
            :to="{
              path: '/observations',
              query: { limit: 50, offset: 0, filter: 'incomplete' },
            }"
          >
            <span class="text-xl">
              {{ stats.incomplete_observations_count }}
            </span>
            <span v-if="stats.incomplete_observations_count > 1">
              observations incomplètes
            </span>
            <span v-else> observation incomplète </span>
          </router-link>
        </div>
      </div>
      <div v-else class="mt-4">
        <router-link to="/observations">
          Pas d'observations incomplètes ! 👍
        </router-link>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 md:gap-y-20 md:gap-x-32 mt-8">
        <router-link to="/stats/c1">
          <div class="mt-12 md:mt-0 flex flex-row items-center space-x-4">
            <div
              class="text-xs text-gray-700 uppercase tracking-wide font-bold"
            >
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
            <div
              class="text-xs text-gray-700 uppercase tracking-wide font-bold"
            >
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
            <div
              class="text-xs text-gray-700 uppercase tracking-wide font-bold"
            >
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
            <div
              class="text-xs text-gray-700 uppercase tracking-wide font-bold"
            >
              Cycle 4
            </div>
            <div class="text-xs text-gray-500">(+ de détails)</div>
          </div>
          <div class="mt-2">
            <StatsSummary :stats="stats.c4" />
          </div>
        </router-link>
      </div>
      <div
        class="grid grid-cols-1 md:grid-cols-2 md:gap-y-20 md:gap-x-32 mt-20"
      >
        <div v-for="week in stats.weeks">
          <div
            class="
              mt-12
              md:mt-0
              text-xs text-gray-700
              uppercase
              tracking-wide
              font-bold
            "
          >
            Semaine du {{ week.week_start }}
          </div>
          <div class="mt-2">
            <div
              v-if="week.counts.length > 0"
              v-for="(count, idx) in week.counts"
              class="mt-2"
            >
              <div>
                {{ idx + 1 }}. {{ userById(count.user).firstname }}&nbsp;{{
                  userById(count.user).lastname
                }}
              </div>

              <div>
                <div class="flex flex-row items-end">
                  <div class="flex-grow text-sm text-gray-700">
                    Observations
                  </div>
                  <div class="text-gray-700 text-xs">
                    {{ count.observations }} / {{ week.observations }}
                  </div>
                </div>
                <ProgressBar
                  :current="count.observations"
                  :total="week.observations"
                />
              </div>
              <div>
                <div class="flex flex-row items-end">
                  <div class="flex-grow text-sm text-gray-700">Évaluations</div>
                  <div class="text-gray-700 text-xs">
                    {{ count.evaluations }} / {{ week.evaluations }}
                  </div>
                </div>
                <ProgressBar
                  :current="count.evaluations"
                  :total="week.evaluations"
                />
              </div>
            </div>
            <div v-else>
              <MascotteTip class="my-2">
                <template v-slot:title>Oh ! 😱</template>
                <template v-slot:default>
                  Personne n'a encore rien fait cette semaine !
                </template>
              </MascotteTip>
            </div>
          </div>
        </div>
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until, useTitle } from "@vueuse/core";
import { dateToString } from "../utils/date";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import StatsSummary from "../components/StatsSummary.vue";
import ProgressBar from "../components/ProgressBar.vue";
import Loading from "../components/Loading.vue";
import MascotteTip from "../components/MascotteTip.vue";

useTitle("Accueil - soklaki.fr");

const store = useStore();

const userById = computed(() => store.getters.userById);

const loading = ref(true);

const stats = ref({});

onMounted(async () => {
  stats.value = await store.dispatch("homeContent");
  loading.value = false;
});
</script>
