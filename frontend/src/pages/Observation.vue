<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
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
          <textarea v-model="observationEditText" class="mt-2 input w-full" rows="5"></textarea>
          <button @click="saveObservationText" class="button-main-action mt-2">Sauvegarder</button>
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
          <button @click="saveObservationDate" class="button-main-action mt-2">Sauvegarder</button>
        </div>
        <div v-else>
          <div class="font-serif space-x-1">
            <span>
              {{ observation.date }}
            </span>
            <!-- TODO link to period page ? -->
            <span v-if="observation.period.name != null" class="text-xs">
              ({{ observation.period.name }})
            </span>
          </div>
        </div>
      </div>
      <!-- students -->
      <div class="mt-16">
        <div class="form-label">Les élèves concernés</div>
        <div
          v-for="studentId in observation.sorted_students"
          class="font-serif flex flex-row space-x-2"
        >
          <div>
            {{ observation.students[studentId].firstname }}
            {{ observation.students[studentId].lastname }}
            ({{ observation.students[studentId].cycle }})
          </div>
          <button @click="removeStudent(studentId)" class="text-gray-300 hover:text-gray-600">
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
            class="mt-4 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            C'est bon, j'ai tout le monde
          </button>
        </div>
        <div v-else>
          <button
            @click="showStudentSelector = true"
            class="mt-1 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            Ajouter des élèves
          </button>
        </div>
      </div>

      <!-- competencies -->
      <div v-if="Object.keys(observation.students).length > 0" class="mt-20">
        <div class="form-label">Les compétences liées</div>
        <div v-for="cycle in ['c1', 'c2', 'c3', 'c4']" class="mt-2">
          <div v-if="observation.cycles[cycle].students.length > 0" class="mt-2">
            <ObservationLinkedCompetencies
              :cycleNb="cycleNb(cycle)"
              :cycle="observation.cycles[cycle]"
              @removeCompetency="removeCompetency($event)"
            />
            <div v-if="showCompetencySelector[cycle]">
              <CompetencySelector
                :socle="socle"
                :cycle="cycle"
                @selected="selectCompetency(cycle, $event)"
              />
              <button
                @click="showCompetencySelector[cycle] = false"
                class="mt-1 rounded-md px-3 border border-teal-700 hover:border-teal-300"
              >
                C'est bon, je les ai toutes
              </button>
            </div>
            <div v-else>
              <button
                @click="showCompetencySelector[cycle] = true"
                class="mt-1 rounded-md px-3 border border-teal-700 hover:border-teal-300"
              >
                Lier des compétences
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Evaluations -->
      <div v-if="haveCompetencies" class="mt-20">
        <div class="form-label">Évaluations</div>
        <div v-for="cycle in ['c1', 'c2', 'c3', 'c4']" class="mt-2">
          <div v-for="competency in observation.cycles[cycle].competencies">
            <div class="form-sub-label mt-2">
              {{ competency.full_rank }}
              {{ competency.text }}
            </div>
            <div v-for="studentId in observation.cycles[cycle].students">
              <div
                v-if="!evaluationInEdit[studentId][competency.id]"
                class="flex flex-row space-x-2"
              >
                <div>
                  {{ observation.students[studentId].firstname }}
                  {{ observation.students[studentId].lastname }}
                </div>
                <div>:</div>
                <div>
                  <div v-if="competency.evaluations[studentId] == null">Non évalué</div>
                  <div v-else>
                    <div v-if="competency.evaluations[studentId].status === 'NotAcquired'">
                      Maîtrise insuffisante
                    </div>
                    <div v-else-if="competency.evaluations[studentId].status === 'InProgress'">
                      Maîtrise fragile
                    </div>
                    <div v-else-if="competency.evaluations[studentId].status === 'Acquired'">
                      Maîtrise satisfaisante
                    </div>
                    <div v-else-if="competency.evaluations[studentId].status === 'TipTop'">
                      Très bonne maîtrise
                    </div>
                    <div v-else>Non évalué</div>
                  </div>
                </div>
                <button @click="editEvaluation(competency.id, studentId)">
                  <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
                </button>
              </div>
              <div v-else class="mb-6 py-2">
                <div>
                  {{ observation.students[studentId].firstname }}
                  {{ observation.students[studentId].firstname }}
                </div>
                <EvalCompetency
                  :edit="true"
                  :comment="competency.evaluations[studentId].comment"
                  :status="competency.evaluations[studentId].status"
                  @save="saveEvaluation($event, competency.id, studentId)"
                  @cancel="cancelEvaluation(competency.id, studentId)"
                />
              </div>
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
          <div className="space-x-1">
            <span>Observée par</span>
            <!-- TODO link to user ?-->
            <span>
              {{ observation.user.firstname }}
              {{ observation.user.lastname }}
            </span>
          </div>
          <div className="space-x-1">
            <span>Complète :</span>
            <span v-if="observation.complete" class="text-green-600">Oui !</span>
            <span v-else class="text-red-600">Non...</span>
          </div>
        </div>
      </div>
      <!-- Allow to "delete" it but behind a disclosure  -->
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
                N'hésitez pas à bien réfléchir, une fois qu'elle est supprimée... Elle est supprimée
                !
              </div>
              <button @click="setActiveFalse" class="button-cancel-action">
                Supprimer cette observation 😱
              </button>
            </div>
          </DisclosurePanel>
        </Disclosure>
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import { cycleNb } from "../utils/cycle";
import { today } from "../utils/date";
import { nonSelectedStudents } from "../utils/observation";
import { evaluationByCompetencyIdStudentId } from "../utils/evaluation";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import StudentSelector from "../components/StudentSelector.vue";
import CompetencySelector from "../components/CompetencySelector.vue";
import DatePicker from "../components/DatePicker.vue";
import EvalCompetency from "../components/EvalCompetency.vue";
import Loading from "../components/Loading.vue";
import ObservationLinkedCompetencies from "../components/ObservationLinkedCompetencies.vue";

useTitle("Observation - soklaki.fr");

const store = useStore();
const router = useRouter();
const route = useRoute();

const loading = ref(true);
const observation = ref(null);
// studentId -> competencyId -> boolean
// filled by getObservation above
const evaluationInEdit = ref({});

const setObservation = (o) => {
  // observation
  observation.value = o;
  // evaluationInEdit
  for (const student of Object.values(observation.value.students)) {
    if (!(student.id in evaluationInEdit.value)) {
      evaluationInEdit.value[student.id] = {};
    }
    for (const competency of observation.value.cycles[student.cycle].competencies) {
      if (!(competency.id in evaluationInEdit.value[student.id])) {
        evaluationInEdit.value[student.id][competency.id] = false;
      }
    }
  }
};

const getObservation = async (id) => {
  const observation = await store.dispatch("observationSingle", { id });
  setObservation(observation);
};

onMounted(async () => {
  loading.value = true;
  await getObservation(route.params.id);
  loading.value = false;
});

watch(() => route.params.id, getObservation);

const haveCompetencies = computed(
  () =>
    observation.value.cycles.c1.competencies.length > 0 ||
    observation.value.cycles.c2.competencies.length > 0 ||
    observation.value.cycles.c3.competencies.length > 0 ||
    observation.value.cycles.c4.competencies.length > 0
);

// Text edit

const observationTextInEdit = ref(false);
const observationEditText = ref("");
const editObservationText = () => {
  observationEditText.value = observation.value.text;
  observationTextInEdit.value = true;
};
const saveObservationText = async () => {
  const observation = await store.dispatch("updateObservationSingleText", {
    id: route.params.id,
    text: observationEditText.value,
  });
  setObservation(observation);
  observationTextInEdit.value = false;
};

// Date edit

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
  const observation = await store.dispatch("updateObservationSingleDate", {
    id: route.params.id,
    date: observationEditDate.value,
  });
  setObservation(observation);
  observationDateInEdit.value = false;
};

// student list

const showStudentSelector = ref(false);
const students = computed(() => store.state.students);
const sortedStudents = computed(() => nonSelectedStudents(store, observation.value));
const addStudent = async (id) => {
  const observation = await store.dispatch("insertObservationStudent", {
    observationId: route.params.id,
    studentId: id,
  });
  setObservation(observation);
};
const removeStudent = async (id) => {
  const observation = await store.dispatch("deleteObservationStudent", {
    observationId: route.params.id,
    studentId: id,
  });
  setObservation(observation);
};

// competency selector

const showCompetencySelector = ref({
  c1: false,
  c2: false,
  c3: false,
  c4: false,
});
const socle = computed(() => store.state.socle);
const selectCompetency = async (cycle, competencyId) => {
  // Check if this is not already in there
  const idx = observation.value.cycles[cycle].competencies.findIndex((x) => x.id == competencyId);
  if (idx != -1) {
    // Yes, just ignore
    return;
  }
  const o = await store.dispatch("insertObservationCompetency", {
    observationId: route.params.id,
    competencyId: competencyId,
  });
  setObservation(o);
};
const removeCompetency = async (competencyId) => {
  const observation = await store.dispatch("deleteObservationCompetency", {
    observationId: route.params.id,
    competencyId: competencyId,
  });
  setObservation(observation);
};

// evaluation

const saveEvaluation = async ({ comment, level }, competencyId, studentId) => {
  const date = today();
  await store.dispatch("evaluationNew", {
    competencyId: competencyId,
    studentId: studentId,
    level,
    comment,
    date,
  });
  await getObservation(route.params.id);

  evaluationInEdit.value[studentId][competencyId] = false;
};
const cancelEvaluation = (competencyId, studentId) => {
  evaluationInEdit.value[studentId][competencyId] = false;
};

const editEvaluation = (competencyId, studentId) => {
  evaluationInEdit.value[studentId][competencyId] = true;
};

// "delete"

const setActiveFalse = async () => {
  await store.dispatch("setObservationActive", {
    id: route.params.id,
    active: false,
  });
  router.push("/observations");
};
</script>
