<template>
  <div class="my-4 px-2">
    <div class="form-label">
      Évaluations - {{ competencyById(competencyId).full_rank }}
    </div>
    <div class="mt-4">
      <div class="uppercase tracking-wide text-gray-700">
        {{ containerById(container1).rank }}.
        {{ containerById(container1).text }}
      </div>
      <div v-if="container2 != null" class="text-gray-700">
        {{ containerById(container2).rank }}.
        {{ containerById(container2).text }}
      </div>
      <div>
        {{ competencyById(competencyId).rank }}.
        {{ competencyById(competencyId).text }}
      </div>
    </div>
    <div class="">
      <div v-for="student in students" class="mt-14">
        <div class="form-label">
          {{ student.firstname }}
          {{ student.lastname }}
        </div>
        <div class="mt-2">
          <EvalCompetency
            :edit="editByStudent[student.id]"
            :comment="evaluationByStudent[student.id].comment"
            :status="evaluationByStudent[student.id].status"
            @save="saveEvaluationByStudent[student.id]"
            @cancel="cancelEvaluationByStudent[student.id]"
          />
        </div>
      </div>
    </div>
    <div class="mt-20 flex flex-row justify-center space-x-4">
      <router-link
        :to="previousCompetency"
        class="border border-gray-300 rounded-md shadow-md hover:text-teal-500 hover:border-teal-500"
      >
        <IconChevronLeft class="h-8" />
      </router-link>
      <router-link
        :to="`/evaluations-by-cycle/${route.params.cycle}`"
        class="border border-gray-300 rounded-md shadow-md hover:text-teal-500 hover:border-teal-500"
      >
        <IconChevronUp class="h-8" />
      </router-link>
      <router-link
        :to="nextCompetency"
        class="border border-gray-300 rounded-md shadow-md hover:text-teal-500 hover:border-teal-500"
      >
        <IconChevronRight class="h-8" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { today } from "../utils/date";
import EvalCompetency from "../components/EvalCompetency.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconChevronUp from "../icons/IconChevronUp.vue";

const store = useStore();
const route = useRoute();

const competencyId = computed(() =>
  route.params.id == null ? null : Number(route.params.id)
);
const competencyById = computed(() => store.getters.competencyById);

const studentById = computed(() => store.getters.studentById);
const students = ref([]);
const fillStudents = () => {
  if (store.state.currentPeriod == null) {
    return;
  }
  const period = store.state.periods[store.state.currentPeriod];
  const full = period.students.map((x) => studentById.value(x.student.id));
  students.value = full.filter(
    (x) => x.current_cycle.current_cycle === route.params.cycle
  );
  goInEdit();
  fillCancelEvaluationByStudent();
  fillSaveEvaluationByStudent();
  fillEvaluationByStudent();
};

const previousCompetency = computed(() => {
  const competencies = Object.keys(store.state.stats[route.params.cycle].stats);
  const current = competencies.findIndex((x) => x == competencyId.value);
  if (current === -1) {
    return "";
  } else if (current === 0) {
    return `/evaluations-by-cycle/${route.params.cycle}`;
  } else {
    const previous = competencies[current - 1];
    return `/evaluation/${route.params.cycle}/${previous}`;
  }
});
const nextCompetency = computed(() => {
  const competencies = Object.keys(store.state.stats[route.params.cycle].stats);
  const current = competencies.findIndex((x) => x == competencyId.value);
  if (current === -1) {
    return "";
  } else if (current === competencies.length - 1) {
    return `/evaluation/${route.params.cycle}/comment`;
  } else {
    const next = competencies[current + 1];
    return `/evaluation/${route.params.cycle}/${next}`;
  }
});

const containerById = computed(() => store.getters.containerById);
const container2 = ref(null);
const container1 = computed(() => {
  if (!(competencyId.value in store.state.socle.competencies)) {
    return null;
  }
  const competency = competencyById.value(competencyId.value);
  const father = containerById.value(competency.container_id);
  if (father.container_id == null) {
    container2.value = null;
    return father.id;
  } else {
    container2.value = father.id;
    return father.container_id;
  }
});

const evaluationByStudent = ref({});
const fillEvaluationByStudent = () => {
  for (const student of students.value) {
    const filtered = Object.values(store.state.evaluations.store).filter(
      (e) =>
        e.student_id === student.id && e.competency_id === competencyId.value
    );
    if (filtered.length > 0) {
      const evaluation = filtered[0];
      evaluationByStudent.value[student.id] = {
        id: evaluation.id,
        comment: evaluation.comment,
        status: evaluation.status,
      };
    } else {
      evaluationByStudent.value[student.id] = {
        id: null,
        comment: null,
        status: "Emtpy",
      };
    }
  }
};

const saveEvaluationByStudent = ref({});
const fillSaveEvaluationByStudent = () => {
  const handlers = {};
  for (const student of students.value) {
    saveEvaluationByStudent.value[student.id] = async ({ comment, status }) => {
      const evaluation = evaluationByStudent.value[student.id];
      if (evaluation.id == null) {
        await store.dispatch("insertEvaluation", {
          studentId: student.id,
          competencyId: competencyId.value,
          periodId: store.state.currentPeriod,
          date: today(),
          status: status,
          comment: comment,
        });
      } else {
        await store.dispatch("updateEvaluation", {
          id: evaluation.id,
          comment: comment,
          date: today(),
          status: status,
          periodId: store.state.currentPeriod,
        });
      }
      fillEvaluationByStudent();
      editByStudent.value[student.id] = false;
    };
  }
};

const cancelEvaluationByStudent = ref({});
const fillCancelEvaluationByStudent = () => {
  for (const student of students.value) {
    cancelEvaluationByStudent.value[student.id] = async ({
      comment,
      status,
    }) => {
      editByStudent.value[student.id] = false;
    };
  }
};

const editByStudent = ref({});
const goInEdit = () => {
  for (const student of students.value) {
    editByStudent.value[student.id] = true;
  }
};
watch(
  () => route.params.id,
  () => {
    goInEdit();
    fillCancelEvaluationByStudent();
    fillSaveEvaluationByStudent();
    fillEvaluationByStudent();
  }
);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("evaluations", {
    periodId: store.state.currentPeriod,
  });
  // For previous/next
  await store.dispatch("stats", {
    periodId: store.state.currentPeriod,
  });
  goInEdit();
  fillStudents();
});
</script>
