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
          class="mt-2 input w-full"
        />
        <button @click="saveObservationDate" class="button-main-action mt-2">
          Sauvegarder
        </button>
      </div>
      <div v-else class="font-serif">{{ observation.date }}</div>
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
          class="ml-2 mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
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
      <div v-for="competencyId in observation.competencies">
        {{ competencyId }}
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
          class="ml-2 mt-2 rounded-md px-3 py-1 shadow-sm border border-teal-700"
        >
          Lier une compétence
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { estimateCycle, cycleNb } from "../utils/cycle";
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

const showStudentSelector = ref(false);
const students = computed(() => store.state.students);
const isStudentObserved = (studentId) => {
  for (const s of observation.value.students) {
    if (s.student_id === studentId) {
      return true;
    }
  }
  return false;
};
const sortedStudents = computed(() =>
  store.state.sortedStudents.filter((id) => !isStudentObserved(id))
);
const studentById = computed(() => store.getters.student);
const studentCycle = computed(() => (studentId) =>
  estimateCycle(
    store.getters.student(studentId).birthdate,
    observation.value.date
  )
);
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

const getObservation = (id) => {
  if (!(id in store.state.observations)) {
    store.dispatch("observation", id);
  }
};
onMounted(() => {
  getObservation(route.params.id);
});
watch(() => route.params.id, getObservation);
</script>
