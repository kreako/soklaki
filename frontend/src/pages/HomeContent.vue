<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="col-span-2">
          <MascotteTip class="my-2">
            <template v-slot:title>Bienvenue sur soklaki ! 🥳</template>
            <template v-slot:default>
              <div class="text-sm">
                Un menu à gauche avec toutes les actions disponibles. 👈 Des
                statistiques pour se motiver ici. 👇👉
              </div>
              <div class="mt-1">
                Et si quelque chose ne se passait pas comme prévu,
                <router-link class="font-bold underline" to="/help">
                  contactez moi
                </router-link>
                !
              </div>
            </template>
          </MascotteTip>
        </div>
        <StatBoxPercent
          label="Progression générale"
          :value="stats.progress"
          :enable="true"
        />
        <router-link
          :to="{
            path: '/observations',
            query: { limit: 50, offset: 0, filter: 'incomplete' },
          }"
        >
          <StatBox
            label="Observations en cours"
            :value="stats.incomplete_observations_count"
          />
        </router-link>
        <router-link to="/stats/c1">
          <StatBoxPercent
            label="Cycle 1"
            :value="stats.c1.progress"
            :enable="stats.c1.students_count > 0"
          />
        </router-link>
        <router-link to="/stats/c2">
          <StatBoxPercent
            label="Cycle 2"
            :value="stats.c2.progress"
            :enable="stats.c2.students_count > 0"
          />
        </router-link>
        <router-link to="/stats/c3">
          <StatBoxPercent
            label="Cycle 3"
            :value="stats.c3.progress"
            :enable="stats.c3.students_count > 0"
          />
        </router-link>
        <router-link to="/stats/c4">
          <StatBoxPercent
            label="Cycle 4"
            :value="stats.c4.progress"
            :enable="stats.c4.students_count > 0"
          />
        </router-link>

        <button
          @click="showWeek.splice(index, 1, !showWeek[index])"
          v-for="(week, index) in stats.weeks"
        >
          <StatBoxWeek :week="week" />
        </button>
        <div
          v-for="(week, index) in stats.weeks"
          class="col-span-2 md:col-span-4"
        >
          <div
            v-if="showWeek[index]"
            class="p-4 border-t border-b border-gray-800 rounded-xl"
          >
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
                  {{ idx + 1 }}. {{ count.user.firstname }}&nbsp;{{
                    count.user.lastname
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
                    <div class="flex-grow text-sm text-gray-700">
                      Évaluations
                    </div>
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
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until, useTitle } from "@vueuse/core";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { dateToString } from "../utils/date";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import StatBox from "../components/StatBox.vue";
import StatBoxPercent from "../components/StatBoxPercent.vue";
import StatBoxWeek from "../components/StatBoxWeek.vue";
import ProgressBar from "../components/ProgressBar.vue";
import Loading from "../components/Loading.vue";
import MascotteTip from "../components/MascotteTip.vue";

useTitle("Accueil - soklaki.fr");

const store = useStore();

const loading = ref(true);

const showWeek = ref([false, false, false, false]);

const stats = ref({});

onMounted(async () => {
  stats.value = await store.dispatch("homeContent");
  loading.value = false;
});
</script>
