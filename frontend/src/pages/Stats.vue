<template>
  <div class="my-4 px-2">
    <div class="form-label">
      Plein de statistiques sur le cycle {{ cycleNb(route.params.cycle) }}
    </div>
    <div class="mt-12">
      <div v-for="slice in students">
        <div class="flex flex-row mt-20">
          <div class="w-16"></div>
          <div
            v-for="studentId in slice"
            class="text-xs w-8 self-end writing-mode-vertical-lr"
          >
            {{ studentById(studentId).firstname }}
            {{ studentById(studentId).lastname }}
          </div>
        </div>
        <div class="mt-2">
          <div
            v-for="(statByStudents, competencyId) in stats.stats"
            class="flex flex-row items-center leading-tight"
          >
            <div class="w-16 text-gray-700 text-right pr-2 hover:text-teal-500">
              <button @click="selectCompetency(competencyId)">
                {{ competencyById(competencyId).full_rank }}
              </button>
            </div>
            <div v-for="studentId in slice" class="flex flex-row space-x-1 w-8">
              <button
                @click="selectObservation(competencyId, studentId)"
                :class="
                  statByStudents[studentId].observations > 0
                    ? 'bg-green-500'
                    : 'bg-red-500'
                "
                class="w-2 h-2"
              ></button>
              <router-link
                :to="`/evaluation-single/${route.params.cycle}/${competencyId}/${studentId}`"
                :class="{
                  'bg-red-500':
                    statByStudents[studentId].evaluations.status === 'Empty',
                  'bg-blue-500':
                    statByStudents[studentId].evaluations.status ===
                    'NotAcquired',
                  'bg-teal-500':
                    statByStudents[studentId].evaluations.status ===
                    'InProgress',
                  'bg-green-500':
                    statByStudents[studentId].evaluations.status ===
                      'Acquired' ||
                    statByStudents[studentId].evaluations.status === 'TipTop',
                }"
                class="w-2 h-2"
              ></router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Modal
      :title="competencyModalTitle"
      :show="showCompetencyModal"
      @close="closeCompetencyModal"
    >
      <div>
        <div class="uppercase tracking-wide text-gray-700">
          {{ competencyFathers[0].rank }}.
          {{ competencyFathers[0].text }}
        </div>
        <div v-if="competencyFathers[1].rank != null" class="text-gray-700">
          {{ competencyFathers[1].rank }}.
          {{ competencyFathers[1].text }}
        </div>
        <div>
          {{ competencyById(selectedCompetency).rank }}.
          {{ competencyById(selectedCompetency).text }}
        </div>
        <div class="mt-2 pl-2">
          <HashSubjects
            :subjects="competencyById(selectedCompetency).subjects"
          />
        </div>
        <div class="mt-2 pl-2">
          <CompetencyTemplates
            :templates="competencyById(selectedCompetency).templates"
          />
        </div>
      </div>
    </Modal>
    <Modal
      :title="observationModalTitle"
      :show="showObservationModal"
      @close="closeObservationModal"
    >
      <div>
        <div class="uppercase tracking-wide text-gray-700 text-xs">
          {{ competencyFathers[0].rank }}.
          {{ competencyFathers[0].text }}
        </div>
        <div
          v-if="competencyFathers[1].rank != null"
          class="text-gray-700 text-xs"
        >
          {{ competencyFathers[1].rank }}.
          {{ competencyFathers[1].text }}
        </div>
        <div class="text-sm">
          {{ competencyById(selectedCompetency).rank }}.
          {{ competencyById(selectedCompetency).text }}
        </div>
        <div class="pl-2">
          <HashSubjects
            :subjects="competencyById(selectedCompetency).subjects"
          />
        </div>
        <div
          v-if="competencyById(selectedCompetency).templates.length > 0"
          class="mt-8 pl-2"
        >
          <div class="font-bold">
            Créer une nouvelle observation à partir d'un modèle
          </div>
          <ul class="mt-2">
            <li
              v-for="template in competencyById(selectedCompetency).templates"
              class="mt-1 hover:text-teal-500"
            >
              <router-link
                :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${template.id}`"
              >
                {{ templateById(template.id).text }}
              </router-link>
            </li>
            <li class="mt-3 hover:text-teal-500">
              <router-link
                :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${-1}`"
              >
                Sans modèle
              </router-link>
            </li>
          </ul>
        </div>
        <div v-else class="mt-8 pl-2">
          <div class="hover:text-teal-500">
            <router-link
              :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${-1}`"
            >
              Créer une nouvelle observation
            </router-link>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until, useTitle } from "@vueuse/core";
import { cycleNb } from "../utils/cycle";
import { fathers } from "../utils/competency";
import Modal from "../components/Modal.vue";
import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";
import HashSubjects from "../components/HashSubjects.vue";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

const store = useStore();
const route = useRoute();

useTitle(`Statistiques avancées ${route.params.cycle}  - soklaki.fr`);

const studentById = computed(() => store.getters.studentById);
const competencyById = computed(() => store.getters.competencyById);

const stats = computed(() => store.state.stats[route.params.cycle]);

const breakpoints = useBreakpoints(breakpointsTailwind);
const mobile = breakpoints.smaller("md");

const selectedCompetency = ref(null);
const selectedStudent = ref(null);

const showObservationModal = ref(false);
const selectObservation = (competencyId, studentId) => {
  selectedCompetency.value = competencyId;
  selectedStudent.value = studentId;
  showObservationModal.value = true;
};
const closeObservationModal = () => {
  showObservationModal.value = false;
};
const observationModalTitle = computed(() => {
  if (selectedCompetency.value == null) {
    return null;
  }
  const competency = competencyById.value(selectedCompetency.value);
  const student = studentById.value(selectedStudent.value);
  return `Observation de ${competency.full_rank} pour ${student.firstname} ${student.lastname}`;
});
const templateById = computed(() => store.getters.templateById);

const showCompetencyModal = ref(false);
const selectCompetency = (id) => {
  selectedCompetency.value = id;
  showCompetencyModal.value = true;
};
const closeCompetencyModal = () => {
  showCompetencyModal.value = false;
};
const competencyModalTitle = computed(() => {
  if (selectedCompetency.value == null) {
    return null;
  }
  const competency = competencyById.value(selectedCompetency.value);
  return `Compétence - ${competency.full_rank}`;
});
const competencyFathers = computed(() =>
  fathers(store, selectedCompetency.value)
);

const students = computed(() => {
  if (store.state.stats[route.params.cycle].studentsCount === null) {
    return [];
  }
  const full = store.state.periods[store.state.currentPeriod].students.map(
    (x) => x.student.id
  );
  const filtered = full.filter(
    (x) =>
      store.state.students[x].current_cycle.current_cycle === route.params.cycle
  );
  let sliceSize = 20;
  if (mobile.value) {
    sliceSize = 7;
  }
  const students = [];
  let index = 0;
  while (true) {
    const slice = filtered.slice(index, index + sliceSize);
    if (slice.length === 0) {
      return students;
    }
    students.push(slice);
    index = index + sliceSize;
  }
});

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("stats", { periodId: store.state.currentPeriod });
});
</script>

<style>
.writing-mode-vertical-lr {
  writing-mode: vertical-lr;
}
</style>
