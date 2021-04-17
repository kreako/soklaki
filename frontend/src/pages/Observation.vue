<template>
  <div class="mt-4 px-2">
    <!-- observation text -->
    <div>
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
          <span class="text-xs"> ({{ period.name }}) </span>
        </div>
      </div>
    </div>
    <!-- students -->
    <div class="mt-8">
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
          class="mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
        >
          Ajouter un élève
        </button>
      </div>
    </div>
    <!-- competencies -->
    <div v-for="(cycleStudents, cycle) in studentByCycle" class="mt-8">
      <div>
        <span class="form-label">Les compétences liées </span>
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
            {{ socle.competencies[competencyId].full_rank }}
          </span>
          <span class="ml-1 truncate">
            {{ socle.competencies[competencyId].text }}
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
          class="mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
        >
          Lier une compétence
        </button>
      </div>
    </div>
    <!-- les évaluations -->
    <div v-for="student in observation.students" class="mt-8">
      <div>
        <span class="form-label"> Évaluation </span>
        <span v-if="observation.students.length > 1" class="form-sub-label">
          {{ studentById(student.student_id).firstname }}
          {{ studentById(student.student_id).lastname }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { estimateCycle, cycleNb } from "../utils/cycle";
import { dateJsObj } from "../utils/date";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import StudentSelector from "../components/StudentSelector.vue";
import CompetencySelector from "../components/CompetencySelector.vue";

const store = useStore();
const router = useRouter();
const route = useRoute();

const observation = computed(() => {
  return (
    store.state.observations[route.params.id] || {
      id: null,
      createdAt: null,
      updatedAt: null,
      userId: null,
      date: null,
      text: null,
      students: [],
      competencies: [],
      period: null,
    }
  );
});

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
  if (observation.value.period != null) {
    if (observation.value.period.id in store.state.periods) {
      return store.state.periods[observation.value.period.id];
    }
  }
  // default
  return {
    name: "?",
  };
});

const showStudentSelector = ref(false);
const students = computed(() => store.state.students);
const isStudentObserved = (studentId) => {
  // Used to filter out from selector the student that I already selected
  for (const s of observation.value.students) {
    if (s.student_id === studentId) {
      return true;
    }
  }
  return false;
};
const sortedStudents = computed(() => {
  if (observation.value.period != null) {
    // There is an associated period
    const periodId = observation.value.period.id;
    if (!(periodId in store.state.periods)) {
      // But the store is not ready
      return [];
    }
    const period = store.state.periods[periodId];
    return period.students
      .map((x) => x.student.id)
      .filter((id) => !isStudentObserved(id));
  } else {
    // return the full set of students (even those not in school anymore)
    return store.state.sortedStudents.filter((id) => !isStudentObserved(id));
  }
});
const studentById = computed(() => store.getters.student);
const studentCycle = computed(() => (studentId) => {
  const student = store.getters.student(studentId);
  if (student.birthdate == null) {
    // Best effort
    return null;
  }
  return estimateCycle(student.birthdate, observation.value.date);
});
const addStudent = async (id) => {
  await store.dispatch("insertObservationStudent", {
    observationId: observation.value.id,
    studentId: id,
  });
  showStudentSelector.value = false;
};
const removeStudent = async (id) => {
  await store.dispatch("deleteObservationStudent", {
    observationId: observation.value.id,
    id: id,
  });
};

const studentByCycle = computed(() => {
  const cycles = {};
  for (const s of observation.value.students) {
    const id = s.student_id;
    const student = store.state.students[id];
    if (student == null) {
      // May happens when store is not full at app startup
      continue;
    }
    const cycle = estimateCycle(student.birthdate, observation.value.date);
    if (!(cycle in cycles)) {
      cycles[cycle] = [];
    }
    cycles[cycle].push(id);
  }
  return cycles;
});

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

const getObservation = (id) => {
  id = Number(id);
  if (!id) {
    // id is not a number :(
    return;
  }
  if (!(id in store.state.observations)) {
    store.dispatch("observation", id);
  }
};
onMounted(() => {
  getObservation(route.params.id);
});
watch(() => route.params.id, getObservation);
</script>
