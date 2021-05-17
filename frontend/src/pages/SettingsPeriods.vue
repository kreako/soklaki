<template>
  <div class="my-4 px-2">
    <div class="flex flex-row space-x-4 items-center">
      <div class="form-label">Les périodes d'évaluation</div>
      <router-link
        to="/settings/new-period"
        class="text-gray-700 text-xs hover:text-teal-500"
      >
        Ajouter une période
      </router-link>
    </div>
    <div class="mt-12">
      <div v-for="periodId in periods">
        <div class="flex flex-row space-x-4 items-center mt-4">
          <div class="flex-grow hover:text-teal-500">
            <router-link :to="`/settings/period/${periodId}`">
              {{ periodById(periodId).name }}
            </router-link>
          </div>
          <div class="text-sm text-gray-700 tabular-nums">
            {{ periodById(periodId).start }}
          </div>
          <div class="text-sm text-gray-700 tabular-nums">
            {{ periodById(periodId).end }}
          </div>
        </div>
      </div>
    </div>
    <div class="mt-8">
      <div class="flex flex-row items-center space-x-2 button-minor-action">
        <router-link to="/settings/new-period">
          <IconPlus class="h-4" />
        </router-link>
        <router-link to="/settings/new-period">
          Ajouter une période
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import IconPlus from "../icons/IconPlus.vue";
import { useTitle } from "@vueuse/core";

useTitle("Périodes - soklaki.fr");

const store = useStore();

const periods = computed(() => store.state.sortedPeriods);

const periodById = computed(() => store.getters.periodById);
</script>
