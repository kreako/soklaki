<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Quelques statistiques...</div>
      <div v-if="stats.incompleteObservationsCount > 0" class="flex flex-row">
        <div class="flex-grow"></div>
        <div class="flex-grow-0">
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
      </div>
      <div v-else class="mt-4">
        <router-link to="/observations">
          Pas d'observations incomplètes ! 👍
        </router-link>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
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
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-12">
        <div v-for="week in last4Weeks">
          <Disclosure>
            <DisclosureButton>
              <div class="flex flex-row items-center space-x-4 mt-4 md:mt-0">
                <div
                  class="
                    text-xs text-gray-700
                    uppercase
                    tracking-wide
                    font-bold
                  "
                >
                  Semaine du {{ week.weekStart }}
                </div>
                <IconQuestionMark class="h-3 text-gray-400" />
              </div>
            </DisclosureButton>
            <DisclosurePanel>
              <MascotteTip class="my-2">
                <template v-slot:title
                  >Le top des utilisateur.ice.s 🏅</template
                >
                <template v-slot:default>
                  <div>
                    Avec le rang (plus d'observations/évaluations classe plus
                    haut)
                  </div>
                  <div>Le prénom, le nom</div>
                  <div>
                    Une petite barre qui représente le nombre d'observations
                    qu'il.elle a rapporté par rapport au nombre total
                    d'observations faites dans la semaine
                  </div>
                  <div>La même chose pour les évaluations !</div>
                </template>
              </MascotteTip>
            </DisclosurePanel>
          </Disclosure>
          <div class="mt-2">
            <table class="w-full">
              <tbody>
                <tr
                  v-for="(count, idx) in week.counts"
                  :class="
                    idx == 0 ? 'text-base' : idx > 2 ? 'text-xs' : 'text-sm'
                  "
                >
                  <td>{{ idx + 1 }}.</td>
                  <td>
                    {{ userById(count.user).firstname }}&nbsp;{{
                      userById(count.user).lastname
                    }}
                  </td>
                  <td class="w-1/2 px-2">
                    <div class="flex flex-row items-center">
                      <ProgressBar
                        :current="count.observations"
                        :total="week.observations"
                        :label="count.observations.toString()"
                      />
                    </div>
                  </td>
                  <td class="w-1/2">
                    <ProgressBar
                      :current="count.evaluations"
                      :total="week.evaluations"
                      :label="count.evaluations.toString()"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
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

const stats = computed(() => store.state.statsSummary);

const addTotal = (week) => {
  week.observations = 0;
  week.evaluations = 0;
  for (const count of week.counts) {
    week.observations += count.observations;
    week.evaluations += count.evaluations;
  }
  return week;
};

const last4Weeks = computed(() => {
  const weeks = [];

  // First search for the monday of this week - getDay() = 1
  let monday = new Date();
  while (monday.getDay() !== 1) {
    monday.setDate(monday.getDate() - 1);
  }
  monday = dateToString(monday);

  let count = 0;
  for (const week of store.state.statsSummary.weeks) {
    if (count > 3) {
      return weeks;
    }
    if (count > 0) {
      weeks.push(addTotal(week));
      count += 1;
    } else {
      if (week.weekStart == monday) {
        weeks.push(addTotal(week));
        count = 1;
      }
    }
  }
  return weeks;
});

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("statsSummary", { periodId: store.state.currentPeriod });
  loading.value = false;
});
</script>
