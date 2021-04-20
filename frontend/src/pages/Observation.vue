<template>
  <div class="px-2">
    <!-- observation text -->
    <div class="mt-8">
      <div>
        <div class="flex flex-row items-center space-x-3">
          <div class="form-label">Description de l'observation</div>
          <button v-if="observationTextInEdit" @click="saveObservationText">
            <IconCheck class="h-4 text-gray-600 hover:text-teal-500" />
          </button>
          <button v-else @click="editObservationText">
            <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
          </button>
        </div>
      </div>
      <div v-if="observationTextInEdit">
        <textarea
          v-model="observationEditText"
          class="mt-2 input w-full"
          rows="5"
        >
        </textarea>
        <button @click="saveObservationText" class="button-main-action mt-2">
          Sauvegarder
        </button>
      </div>
      <div v-else class="font-serif whitespace-pre">{{ observation.text }}</div>
    </div>
    <!-- observation date -->
    <div class="mt-8">
      <div class="flex flex-row items-center space-x-3">
        <div class="form-label">La date de l'observation</div>
        <button v-if="observationDateInEdit" @click="saveObservationDate">
          <IconCheck class="h-4 text-gray-600 hover:text-teal-500" />
        </button>
        <button v-else @click="editObservationDate">
          <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
        </button>
      </div>
      <div v-if="observationDateInEdit">
        <input
          type="text"
          v-model="observationEditDate"
          @keyup.enter="saveObservationDate"
          class="mt-2 input w-full"
        />
        <button @click="saveObservationDate" class="button-main-action mt-2">
          Sauvegarder
        </button>
      </div>
      <div v-else>
        <div class="font-serif">
          <span>
            {{ observation.date }}
          </span>
          <!-- TODO link to period page ? -->
          <span v-if="period.name != null" class="text-xs">
            ({{ period.name }})
          </span>
        </div>
      </div>
    </div>
    <!-- students -->
    <div class="mt-16">
      <div class="form-label">Les élèves concernés</div>
      <div
        v-for="student in observation.students"
        class="font-serif flex flex-row space-x-2"
      >
        <div>
          {{ studentById(student.student_id).firstname }}
          {{ studentById(student.student_id).lastname }}
          ({{ studentCycle(student.student_id) }})
        </div>
        <button
          @click="removeStudent(student.id)"
          class="text-gray-300 hover:text-gray-600"
        >
          <IconXCircle class="h-4" />
        </button>
      </div>
      <div v-if="showStudentSelector">
        <StudentSelector
          @select="addStudent"
          @cancel="showStudentSelector = false"
          :sortedStudents="sortedStudents"
          :students="students"
        />
      </div>
      <div v-else>
        <button
          @click="showStudentSelector = true"
          class="mt-1 rounded-md px-3 border border-teal-700 hover:border-teal-300"
        >
          Ajouter un élève
        </button>
      </div>
    </div>
    <!-- competencies -->
    <div v-if="Object.keys(studentByCycle).length > 0" class="mt-20">
      <div class="form-label">Les compétences liées</div>
      <div v-for="(cycleStudents, cycle) in studentByCycle" class="mt-2">
        <div>
          <span
            v-if="Object.keys(studentByCycle).length > 1"
            class="form-sub-label"
          >
            cycle {{ cycleNb(cycle) }} - {{ cycleStudents.length }}
            <span v-if="cycleStudents.length > 1"> élèves </span>
            <span v-else> élève </span>
          </span>
        </div>
        <div v-for="competencyId in competenciesByCycle[cycle]">
          <div class="flex flex-row items-center">
            <span>
              {{ competencyById(competencyId).full_rank }}
            </span>
            <span class="ml-1 truncate">
              {{ competencyById(competencyId).text }}
            </span>
            <button
              @click="removeCompetency(competencyId)"
              class="text-gray-300 hover:text-gray-600 mx-2"
            >
              <IconXCircle class="h-4" />
            </button>
          </div>
        </div>
        <div v-if="showCompetencySelector[cycle]">
          <CompetencySelector
            :socle="socle"
            :cycle="cycle"
            @cancel="showCompetencySelector[cycle] = false"
            @selected="selectCompetency(cycle, $event)"
          />
        </div>
        <div v-else>
          <button
            @click="showCompetencySelector[cycle] = true"
            class="mt-1 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            Lier une compétence
          </button>
        </div>
      </div>
    </div>
    <!-- Evaluations -->
    <div v-if="competenciesByStudent.length > 0" class="mt-20">
      <div class="form-label">Évaluation</div>
      <div v-for="c in competenciesByStudent">
        <div class="form-sub-label mt-2">
          {{ competencyById(c.competencyId).full_rank }}
          {{ competencyById(c.competencyId).text }}
        </div>
        <div v-for="e in c.evaluations">
          <div
            v-if="!evaluationInEdit[c.competencyId][e.studentId]"
            class="flex flex-row space-x-2"
          >
            <div>
              {{ studentById(e.studentId).firstname }}
              {{ studentById(e.studentId).lastname }}
            </div>
            <div>:</div>
            <div>
              <div v-if="e.evaluationId == null">Non évalué</div>
              <div v-else>
                <div v-if="evaluationById(e.evaluationId).status === 'Empty'">
                  Non évalué
                </div>
                <div
                  v-else-if="
                    evaluationById(e.evaluationId).status === 'InProgress'
                  "
                >
                  En cours
                </div>
                <div
                  v-else-if="
                    evaluationById(e.evaluationId).status === 'Acquired'
                  "
                >
                  Acquis
                </div>
                <div
                  v-else-if="
                    evaluationById(e.evaluationId).status === 'NotAcquired'
                  "
                >
                  Non acquis
                </div>
              </div>
            </div>
            <button @click="editEvaluation(c.competencyId, e.studentId)">
              <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
            </button>
          </div>
          <div v-else class="mb-6 py-2 px-1 border-teal-300 border">
            <div>
              {{ competencyById(c.competencyId).full_rank }}
              {{ studentById(e.studentId).firstname }}
              {{ studentById(e.studentId).lastname }}
            </div>
            <div>
              <div class="form-sub-label">Commentaire</div>
              <textarea
                v-model="evaluationEditText[c.competencyId][e.studentId]"
                class="mt-2 input w-full"
                rows="5"
              >
              </textarea>
            </div>
            <div class="flex flex-row space-x-2">
              <button
                @click="
                  doEvaluation(c.competencyId, e.studentId, 'NotAcquired')
                "
                class="mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
              >
                Non acquis
              </button>
              <button
                @click="doEvaluation(c.competencyId, e.studentId, 'InProgress')"
                class="mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
              >
                En cours
              </button>
              <button
                @click="doEvaluation(c.competencyId, e.studentId, 'Acquired')"
                class="mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
              >
                Acquis
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { estimateCycle, cycleNb, cycleFullName } from "../utils/cycle";
import { dateJsObj } from "../utils/date";
import { nonSelectedStudents } from "../utils/observation";
import { studentCycleById, groupStudentsByCycle } from "../utils/student";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import StudentSelector from "../components/StudentSelector.vue";
import CompetencySelector from "../components/CompetencySelector.vue";

const store = useStore();
const router = useRouter();
const route = useRoute();

const observation = computed(() =>
  store.getters.observationById(route.params.id)
);

const observationTextInEdit = ref(false);
const observationEditText = ref("");
const editObservationText = () => {
  observationEditText.value = observation.value.text;
  observationTextInEdit.value = true;
};
const saveObservationText = async () => {
  // TODO store dispatch
  await store.dispatch("updateObservationText", {
    id: observation.value.id,
    text: observationEditText.value,
  });
  observationTextInEdit.value = false;
};

const observationDateInEdit = ref(false);
const observationEditDate = ref("");
const editObservationDate = () => {
  observationEditDate.value = observation.value.date;
  observationDateInEdit.value = true;
};
const saveObservationDate = async () => {
  // TODO store dispatch
  await store.dispatch("updateObservationDate", {
    id: observation.value.id,
    date: observationEditDate.value,
  });
  observationDateInEdit.value = false;
};
const period = computed(() => {
  const periodId =
    observation.value.period == null ? null : observation.value.period.id;
  return store.getters.periodById(periodId);
});

const showStudentSelector = ref(false);
const students = computed(() => store.state.students);
const sortedStudents = computed(() =>
  nonSelectedStudents(store, observation.value)
);
const studentById = computed(() => store.getters.studentById);
const studentCycle = computed(() => (studentId) =>
  studentCycleById(store, observation.value.date, studentId)
);
const addStudent = async (id) => {
  await store.dispatch("insertObservationStudent", {
    observationId: observation.value.id,
    studentId: id,
  });
  showStudentSelector.value = false;
  await updateEvaluations();
};
const removeStudent = async (id) => {
  await store.dispatch("deleteObservationStudent", {
    observationId: observation.value.id,
    id: id,
  });
};

const studentByCycle = computed(() =>
  groupStudentsByCycle(
    store,
    observation.value.date,
    observation.value.students.map((x) => x.student_id)
  )
);

const showCompetencySelector = ref({
  c1: false,
  c2: false,
  c3: false,
  c4: false,
});
const socle = computed(() => store.state.socle);
const selectCompetency = async (cycle, competencyId) => {
  // Check if this is not already in there
  for (const competency of observation.value.competencies) {
    if (competency.competency_id === competencyId) {
      // Yes, just ignore
      showCompetencySelector.value[cycle] = false;
      return;
    }
  }
  await store.dispatch("insertObservationCompetency", {
    observationId: observation.value.id,
    competencyId: competencyId,
  });
  showCompetencySelector.value[cycle] = false;
  await updateEvaluations();
};
const removeCompetency = async (competencyId) => {
  await store.dispatch("deleteObservationCompetency", {
    observationId: observation.value.id,
    competencyId: competencyId,
  });
};
const competenciesByCycle = computed(() => {
  const competencies = {
    c1: [],
    c2: [],
    c3: [],
    c4: [],
  };
  for (const c of observation.value.competencies) {
    const competencyId = c.competency_id;
    const competency = store.state.socle.competencies[competencyId];
    if (competency == null) {
      // Could happen when the store is not yet full
      continue;
    }
    competencies[competency.cycle].push(competencyId);
  }
  return competencies;
});

// This function will dispatch evaluationsByStudentCompetency action
// Allowing computed property competenciesByStudent to use the evaluation id
// Because vue don't allow async computed
// TODO This function will over dispatch because it doesn't check competency.cycle === student.cycle
// Not so important for now (number of competencies/students is probably small)
// observation is dispatched first but to updateEvaluations I need store.state.socle.competencies
// Maybe with nextTick or refactor updateEvaluations/competenciesByStudent with vue-async-computed
const updateEvaluations = async () => {
  for (const c of observation.value.competencies) {
    const competencyId = c.competency_id;
    for (const s of observation.value.students) {
      const studentId = s.student_id;
      await store.dispatch("evaluationByStudentCompetency", {
        studentId: studentId,
        competencyId: competencyId,
      });
    }
  }
};
const competenciesByStudent = computed(() => {
  // Now build an array of competencies with :
  // [ { competencyId, evaluations: [{studentId, evaluationId}] } ]
  const competencies = [];
  for (const c of observation.value.competencies) {
    const competencyId = c.competency_id;
    if (!(competencyId in store.state.socle.competencies)) {
      // store is not yet full
      return [];
    }
    const competency = store.state.socle.competencies[competencyId];
    const evaluations = [];
    for (const s of observation.value.students) {
      const studentId = s.student_id;
      if (competency.cycle !== studentCycle.value(studentId)) {
        // Ignore student it doesn't match the cycle
        continue;
      }
      if (studentId in store.state.evaluations.byStudentCompetency) {
        if (
          competencyId in store.state.evaluations.byStudentCompetency[studentId]
        ) {
          // Winner
          const evaluationId =
            store.state.evaluations.byStudentCompetency[studentId][
              competencyId
            ];
          evaluations.push({
            studentId: studentId,
            evaluationId: evaluationId,
          });
          // Make sure that evaluationInEdit is filled
          if (!(competencyId in evaluationInEdit.value)) {
            evaluationInEdit.value[competencyId] = {};
          }
          if (!(studentId in evaluationInEdit.value)) {
            evaluationInEdit.value[competencyId][studentId] = false;
          }
          // And evaluationEditText too
          if (!(competencyId in evaluationEditText.value)) {
            evaluationEditText.value[competencyId] = {};
          }
          if (!(studentId in evaluationEditText.value)) {
            if (evaluationId == null) {
              evaluationEditText.value[competencyId][studentId] = "";
            } else {
              evaluationEditText.value[competencyId][studentId] =
                store.state.evaluations.evaluations[evaluationId].comment;
            }
          }
        }
      }
    }
    competencies.push({ competencyId: competencyId, evaluations: evaluations });
  }
  return competencies;
});
const competencyById = computed(() => store.getters.competencyById);
// competencyId -> studentId -> boolean
// filled by competenciesByStudent computed
const evaluationInEdit = ref({});
// competencyId -> studentId -> text
// filled by competenciesByStudent computed too
const evaluationEditText = ref({});
const editEvaluation = (competencyId, studentId) => {
  evaluationInEdit.value[competencyId][studentId] = true;
};
const doEvaluation = async (competencyId, studentId, status) => {
  const comment = evaluationEditText.value[competencyId][studentId];
  const periodId =
    observation.value.period == null ? null : observation.value.period.id;
  await store.dispatch("insertEvaluation", {
    competencyId: competencyId,
    studentId: studentId,
    status: status,
    comment: comment,
    date: observation.value.date,
    periodId: periodId,
  });
  evaluationInEdit.value[competencyId][studentId] = false;
};
const evaluationById = computed(() => store.getters.evaluationById);

const getObservation = async (id) => {
  id = Number(id);
  if (!id) {
    // id is not a number :(
    return;
  }
  await store.dispatch("observation", id);
  await updateEvaluations();
};
onMounted(async () => {
  await getObservation(route.params.id);
});
watch(() => route.params.id, getObservation);
</script>
