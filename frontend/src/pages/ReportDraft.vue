<template>
  <div class="my-4 px-2">
    <div class="form-label">
      Rapport {{ student.firstname }} {{ student.lastname }} - {{ period.name }}
    </div>
    <div class="mt-12">
      <div>
        <div class="form-sub-label">École</div>
        <div>{{ groupName }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Date du rapport</div>
        <div>{{ today() }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Nom</div>
        <div>{{ student.lastname }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Prénom</div>
        <div>{{ student.firstname }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Cycle</div>
        <div>Cycle {{ cycleNb(route.params.cycle) }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Date d'anniversaire</div>
        <div>{{ student.birthdate }}</div>
      </div>
      <div class="mt-3">
        <div class="form-sub-label">Date d'entrée à l'école</div>
        <div>{{ student.school_entry }}</div>
      </div>
      <div v-if="student.school_exit != null" class="mt-3">
        <div class="form-sub-label">Date de sortie de l'école</div>
        <div>{{ student.school_exit }}</div>
      </div>
    </div>
    <div class="mt-12">
      <div v-for="container1 in socle">
        <div class="uppercase tracking-wide text-gray-700 text-sm">
          {{ containerById(container1.id).rank }}.
          {{ containerById(container1.id).text }}
        </div>
        <div v-for="container2 in container1.children" class="pl-2">
          <div class="text-gray-700 text-sm">
            {{ containerById(container2.id).rank }}.
            {{ containerById(container2.id).text }}
          </div>
          <div v-for="competency in container2.competencies" class="pl-2">
            <div class="text-gray-700">
              {{ competencyById(competency.id).rank }}.
              {{ competencyById(competency.id).text }}
            </div>
            <div class="pl-2 my-4">
              <ReportPerCompetency
                :evaluation="evaluationPerCompetency[competency.id]"
                :observations="observationsPerCompetency[competency.id]"
              />
            </div>
          </div>
        </div>
        <div v-for="competency in container1.competencies" class="pl-2">
          <div class="text-gray-700">
            {{ competencyById(competency.id).rank }}.
            {{ competencyById(competency.id).text }}
          </div>
          <div class="pl-2 my-4">
            <ReportPerCompetency
              :evaluation="evaluationPerCompetency[competency.id]"
              :observations="observationsPerCompetency[competency.id]"
            />
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="mt-20 form-sub-label uppercase tracking-wide">
        Les observations
      </div>
      <div v-for="observation in observations" class="mt-4">
        <div class="text-sm">
          {{ observation.date }}
        </div>
        <div
          v-for="competency in observation.competencies"
          class="pl-2 text-sm text-gray-700"
        >
          {{ competencyById(competency.competency_id).full_rank }}.
          {{ competencyById(competency.competency_id).text }}
        </div>
        <div class="font-serif">
          {{ observation.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { cycleNb } from "../utils/cycle";
import { today } from "../utils/date";
import ReportPerCompetency from "../components/ReportPerCompetency.vue";

const store = useStore();
const route = useRoute();

const containerById = computed(() => store.getters.containerById);
const competencyById = computed(() => store.getters.competencyById);

const groupName = computed(() => store.state.group.name);

const period = computed(() => store.getters.periodById(route.params.periodId));
const student = computed(() =>
  store.getters.studentById(route.params.studentId)
);

const socle = computed(() => store.state.socle[route.params.cycle]);

const observations = computed(() => store.state.report.observations);

const observationsPerCompetency = computed(() => {
  const count = {};
  for (const observation of store.state.report.observations) {
    for (const c of observation.competencies) {
      const id = c.competency_id;
      if (!(id in count)) {
        count[id] = 0;
      }
      count[id] += 1;
    }
  }
  return count;
});

const evaluationPerCompetency = computed(() => {
  const evaluations = {};
  for (const evaluation of store.state.report.evaluations) {
    const id = evaluation.competency_id;
    if (!(id in evaluations)) {
      evaluations[id] = evaluation;
    }
  }
  return evaluations;
});

watch(route, async () => {
  if (route.path != "/report-draft") {
    return;
  }
  await store.dispatch("report", {
    periodId: Number(route.params.periodId),
    studentId: Number(route.params.studentId),
  });
});

onMounted(async () => {
  await store.dispatch("report", {
    periodId: Number(route.params.periodId),
    studentId: Number(route.params.studentId),
  });
});
</script>
