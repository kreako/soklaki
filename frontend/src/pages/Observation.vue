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
        <DatePicker
          :value="observationEditDate"
          @selected="observationDateSelected"
          class="mt-2"
        />
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
          @click="removeStudent(student.student_id)"
          class="text-gray-300 hover:text-gray-600"
        >
          <IconXCircle class="h-4" />
        </button>
      </div>
      <div v-if="showStudentSelector">
        <StudentSelector
          @select="addStudent"
          :sortedStudents="sortedStudents"
          :students="students"
          class="mt-4"
        />
        <button
          @click="showStudentSelector = false"
          class="
            mt-4
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          C'est bon, j'ai tout le monde
        </button>
      </div>
      <div v-else>
        <button
          @click="showStudentSelector = true"
          class="
            mt-1
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          Ajouter des élèves
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
            @selected="selectCompetency(cycle, $event)"
          />
          <button
            @click="showCompetencySelector[cycle] = false"
            class="
              mt-1
              rounded-md
              px-3
              border border-teal-700
              hover:border-teal-300
            "
          >
            C'est bon, je les ai toutes
          </button>
        </div>
        <div v-else>
          <button
            @click="showCompetencySelector[cycle] = true"
            class="
              mt-1
              rounded-md
              px-3
              border border-teal-700
              hover:border-teal-300
            "
          >
            Lier des compétences
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
            v-if="!evaluationInEdit[c.competencyId][e.student_id]"
            class="flex flex-row space-x-2"
          >
            <div>
              {{ studentById(e.student_id).firstname }}
              {{ studentById(e.student_id).lastname }}
            </div>
            <div>:</div>
            <div>
              <div v-if="e.id == null">Non évalué</div>
              <div v-else>
                <div v-if="e.status === 'NotAcquired'">
                  Maîtrise insuffisante
                </div>
                <div v-else-if="e.status === 'InProgress'">
                  Maîtrise fragile
                </div>
                <div v-else-if="e.status === 'Acquired'">
                  Maîtrise satisfaisante
                </div>
                <div v-else-if="e.status === 'TipTop'">Très bonne maîtrise</div>
                <div v-else>Non évalué</div>
              </div>
            </div>
            <button @click="editEvaluation(c.competencyId, e.student_id)">
              <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
            </button>
          </div>
          <div v-else class="mb-6 py-2">
            <div>
              {{ studentById(e.student_id).firstname }}
              {{ studentById(e.student_id).lastname }}
            </div>
            <EvalCompetency
              :edit="true"
              :comment="e.comment"
              :status="e.status"
              @save="saveEvaluation($event, c.competencyId, e.student_id)"
              @cancel="cancelEvaluation(c.competencyId, e.student_id)"
            />
          </div>
        </div>
      </div>
    </div>
    <!-- Details -->
    <div class="mt-20">
      <div>
        <div class="flex flex-row items-center space-x-3">
          <div class="form-label">Détails</div>
        </div>
      </div>
      <div class="text-sm">
        <div>
          <span>Observée par </span>
          <!-- TODO link to user ?-->
          <span>
            {{ userById(observation.user_id).firstname }}
            {{ userById(observation.user_id).lastname }}
          </span>
        </div>
        <div>
          <span>Complète : </span>
          <span v-if="observation.complete.complete" class="text-green-600">
            Oui !
          </span>
          <span v-else class="text-red-600">Non...</span>
        </div>
      </div>
    </div>
    <!-- Details -->
    <div class="mt-20">
      <Disclosure>
        <DisclosureButton class="">
          <div class="flex flex-row items-center space-x-3">
            <div class="form-label">Zone dangereuse</div>
          </div>
        </DisclosureButton>
        <DisclosurePanel>
          <div>
            <div>
              N'hésitez pas à bien réfléchir, une fois qu'elle est supprimée...
              Elle est supprimée !
            </div>
            <button @click="setActiveFalse" class="button-cancel-action">
              Supprimer cette observation 😱
            </button>
          </div>
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import { cycleNb, cycleFullName } from "../utils/cycle";
import { dateToNiceString, today } from "../utils/date";
import { nonSelectedStudents } from "../utils/observation";
import { groupStudentsByCycle, studentsIdToCycle } from "../utils/student";
import { groupCompetenciesByCycle } from "../utils/competency";
import { evaluationByCompetencyIdStudentId } from "../utils/evaluation";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";
import IconX from "../icons/IconX.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import StudentSelector from "../components/StudentSelector.vue";
import CompetencySelector from "../components/CompetencySelector.vue";
import DatePicker from "../components/DatePicker.vue";
import EvalCompetency from "../components/EvalCompetency.vue";

useTitle("Observation - soklaki.fr");

const store = useStore();
const router = useRouter();
const route = useRoute();

const observation = computed(() => {
  if (
    store.state.observation == null ||
    store.state.observation.id != route.params.id
  ) {
    return store.getters.observationById(null);
  }

  return store.state.observation;
});

const observationTextInEdit = ref(false);
const observationEditText = ref("");
const editObservationText = () => {
  observationEditText.value = observation.value.text;
  observationTextInEdit.value = true;
};
const saveObservationText = async () => {
  await store.dispatch("updateObservationText", {
    id: route.params.id,
    text: observationEditText.value,
  });
  observationTextInEdit.value = false;
};

const observationDateInEdit = ref(false);
const observationEditDate = ref("");
const observationDateSelected = (value) => {
  observationEditDate.value = value;
};
const editObservationDate = () => {
  observationEditDate.value = observation.value.date;
  observationDateInEdit.value = true;
};
const saveObservationDate = async () => {
  await store.dispatch("updateObservationDate", {
    id: route.params.id,
    date: observationEditDate.value,
  });
  observationDateInEdit.value = false;
};
const period = computed(() => {
  const id =
    observation.value.period == null
      ? null
      : observation.value.period.eval_period_id;
  return store.getters.periodById(id);
});

const showStudentSelector = ref(false);
const students = computed(() => store.state.students);
const sortedStudents = computed(() =>
  nonSelectedStudents(store, observation.value)
);
const studentById = computed(() => store.getters.studentById);
const studentsCycle = computed(() =>
  studentsIdToCycle(observation.value.students)
);
const studentCycle = computed(
  () => (studentId) => studentsCycle.value[studentId]
);
const addStudent = async (id) => {
  await store.dispatch("insertObservationStudent", {
    observationId: route.params.id,
    studentId: id,
  });
};
const removeStudent = async (id) => {
  await store.dispatch("deleteObservationStudent", {
    observationId: route.params.id,
    studentId: id,
  });
};

const studentByCycle = computed(() =>
  groupStudentsByCycle(observation.value.students)
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
      return;
    }
  }
  await store.dispatch("insertObservationCompetency", {
    observationId: route.params.id,
    competencyId: competencyId,
  });
};
const removeCompetency = async (competencyId) => {
  await store.dispatch("deleteObservationCompetency", {
    observationId: route.params.id,
    competencyId: competencyId,
  });
};
const competenciesByCycle = computed(() =>
  groupCompetenciesByCycle(
    store,
    observation.value.competencies.map((x) => x.competency_id)
  )
);

const saveEvaluation = async ({ comment, status }, competencyId, studentId) => {
  if (
    competencyId in evaluationByCompetencyStudent.value &&
    studentId in evaluationByCompetencyStudent.value[competencyId]
  ) {
    const evaluation =
      evaluationByCompetencyStudent.value[competencyId][studentId];
    await store.dispatch("updateEvaluation", {
      id: evaluation.id,
      comment: comment,
      date: today(),
      status: status,
      periodId: store.state.currentPeriod,
    });
  } else {
    await store.dispatch("insertEvaluation", {
      studentId: studentId,
      competencyId: competencyId,
      periodId: store.state.currentPeriod,
      date: today(),
      status: status,
      comment: comment,
    });
  }
  await getObservation(observation.value.id);
  evaluationInEdit.value[competencyId][studentId] = false;
};
const cancelEvaluation = (competencyId, studentId) => {
  evaluationInEdit.value[competencyId][studentId] = false;
};

// competencyId -> studentId -> boolean
// filled by competenciesByStudent above
const evaluationInEdit = ref({});

const evaluationByCompetencyStudent = computed(() => {
  return evaluationByCompetencyIdStudentId(observation.value.last_evaluations);
});
const competenciesByStudent = computed(() => {
  if (observation.value.competencies == null) {
    // Maybe init is not done yet...
    return [];
  }
  // Now build an array of competencies with :
  // [ { competencyId, evaluations: [{evaluation}] } ]
  const competencies = [];
  for (const c of observation.value.competencies) {
    const competencyId = c.competency_id;
    if (!(competencyId in store.state.socle.competencies)) {
      // store is not yet full
      return [];
    }
    const competency = store.getters.competencyById(competencyId);
    // Fill edit helper
    if (!(competencyId in evaluationInEdit.value)) {
      evaluationInEdit.value[competencyId] = {};
    }
    const evaluations = [];
    for (const s of observation.value.students) {
      const studentId = s.student_id;
      if (competency.cycle !== studentCycle.value(studentId)) {
        // Ignore student it doesn't match the cycle
        continue;
      }
      if (competencyId in evaluationByCompetencyStudent.value) {
        if (studentId in evaluationByCompetencyStudent.value[competencyId]) {
          // Winner
          const evaluation =
            evaluationByCompetencyStudent.value[competencyId][studentId];
          evaluations.push(evaluation);
          if (!(studentId in evaluationInEdit.value[competencyId])) {
            evaluationInEdit.value[competencyId][studentId] = false;
          }
          continue;
        }
      }
      // no evaluation found, push a null one
      evaluations.push({ id: null, student_id: studentId });
      if (!(studentId in evaluationInEdit.value[competencyId])) {
        evaluationInEdit.value[competencyId][studentId] = false;
      }
    }
    if (evaluations.length > 0) {
      // If not this is a competency without student
      // Can happen if the last student of the cycle is removed and not the competency
      competencies.push({
        competencyId: competencyId,
        evaluations: evaluations,
      });
    }
  }
  return competencies;
});
const competencyById = computed(() => store.getters.competencyById);
const editEvaluation = (competencyId, studentId) => {
  evaluationInEdit.value[competencyId][studentId] = true;
};

const userById = computed(() => store.getters.userById);

const setActiveFalse = async () => {
  await store.dispatch("updateObservationActive", {
    id: route.params.id,
    active: false,
  });
  router.push("/observations");
};

const getObservation = async (id) => {
  id = Number(id);
  if (!id) {
    // id is not a number :(
    return;
  }
  await store.dispatch("observation", id);
};
onMounted(async () => {
  await getObservation(route.params.id);
});
watch(() => route.params.id, getObservation);
</script>
