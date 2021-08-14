<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">
        Une nouvelle observation - {{ competency.full_rank }} -
        {{ student.firstname }}
        {{ student.lastname }}
      </div>
      <div class="mt-4">
        <div class="uppercase tracking-wide text-gray-700 text-xs">
          {{ competency.parent.rank }}.
          {{ competency.parent.text }}
        </div>
        <div
          v-if="competency.parent.parent != null"
          class="text-gray-700 text-xs"
        >
          {{ competency.parent.parent.rank }}.
          {{ competency.parent.parent.text }}
        </div>
        <div>
          {{ competency.rank }}.
          {{ competency.text }}
        </div>
      </div>
      <div class="mt-10 px-2 w-full">
        <div class="w-full">
          <div class="text-gray-800">Décrivez votre observation</div>
          <textarea
            v-model="text"
            class="mt-2 input w-full"
            rows="8"
          ></textarea>
        </div>
        <div class="mt-8">
          <button @click="save" class="button-main-action">Enregistrer</button>
        </div>
      </div>
    </Loading>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { cycleNb } from "../utils/cycle";
import Loading from "../components/Loading.vue";
import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";
import { useTitle } from "@vueuse/core";

useTitle("Nouvelle observation - soklaki.fr");

const store = useStore();
const route = useRoute();
const router = useRouter();

const loading = ref(true);

const student = ref(null);
const competency = ref(null);

const text = ref("");

const save = async () => {
  let data = await store.dispatch("observationNewPrefill", {
    text: text.value,
    studentId: route.params.studentId,
    competencyId: route.params.competencyId,
  });
  router.push(`/observation/${data.id}`);
};

const loadPrefill = async () => {
  if (route.params.competencyId == null || route.params.studentId == null) {
    // ok... Still at init... wait for it
    return;
  }
  loading.value = true;
  const data = await store.dispatch("observationPrefill", {
    competencyId: route.params.competencyId,
    studentId: route.params.studentId,
  });
  competency.value = data.competency;
  student.value = data.student;
  useTitle(
    `Nouvelle observation ${data.competency.full_rank} - ${data.student.firstname} ${data.student.lastname} - soklaki.fr`
  );
  loading.value = false;
};

watch(
  () => [route.params.competencyId, route.params.studentId],
  async () => {
    await loadPrefill();
  }
);

onMounted(async () => {
  await loadPrefill();
});
</script>
