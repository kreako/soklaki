<template>
  <div class="my-4 px-2">
    <div class="form-label">Une nouvelle observation</div>
    <div class="form-label">
      {{ student.firstname }}
      {{ student.lastname }}
      - {{ competency.full_rank }}
    </div>
    <div class="mt-10 px-2 w-full">
      <div class="w-full">
        <div class="text-gray-800">Décrivez votre observation</div>
        <textarea v-model="text" class="mt-2 input w-full" rows="8"></textarea>
      </div>
      <div class="mt-8">
        <button @click="save" class="button-main-action">Enregistrer</button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { cycleNb } from "../utils/cycle";
import { fathers } from "../utils/competency";
import Modal from "../components/Modal.vue";
import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";
import HashSubjects from "../components/HashSubjects.vue";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const student = computed(() =>
  store.getters.studentById(route.params.studentId)
);

const competency = computed(() =>
  store.getters.competencyById(route.params.competencyId)
);

const text = ref("");

const template = computed(() => {
  if (route.params.templateId == null) {
    return null;
  } else {
    return store.getters.templateById(route.params.templateId);
  }
});
watch(template, () => {
  if (template.value != null) {
    text.value = template.value.text;
  }
});

const save = async () => {
  let id = await store.dispatch("insertObservation", {
    text: text.value,
  });
  await store.dispatch("insertObservationStudent", {
    observationId: id,
    studentId: Number(route.params.studentId),
  });
  await store.dispatch("insertObservationCompetency", {
    observationId: id,
    competencyId: Number(route.params.competencyId),
  });
  router.push(`/observation/${id}`);
};
</script>
