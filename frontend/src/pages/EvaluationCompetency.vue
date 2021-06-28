<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">
        Évaluations - {{ competencyById(competencyId).full_rank }}
      </div>
      <div class="mt-4">
        <div class="uppercase tracking-wide text-gray-700">
          {{ competencyFathers[0].rank }}.
          {{ competencyFathers[0].text }}
        </div>
        <div v-if="competencyFathers[1].rank != null" class="text-gray-700">
          {{ competencyFathers[1].rank }}.
          {{ competencyFathers[1].text }}
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
              :edit="true"
              :comment="evaluationByStudent[student.id].comment"
              :status="evaluationByStudent[student.id].status"
              @save="saveEvaluation(student.id, $event)"
              @cancel="cancelEvaluation(student.id)"
            />
          </div>
        </div>
      </div>
      <div class="mt-20 flex flex-row justify-center space-x-4">
        <router-link
          :to="previousCompetency"
          class="
            border border-gray-300
            rounded-md
            shadow-md
            hover:text-teal-500 hover:border-teal-500
          "
        >
          <IconChevronLeft class="h-8" />
        </router-link>
        <router-link
          :to="`/evaluations-by-cycle/${route.params.cycle}`"
          class="
            border border-gray-300
            rounded-md
            shadow-md
            hover:text-teal-500 hover:border-teal-500
          "
        >
          <IconChevronUp class="h-8" />
        </router-link>
        <router-link
          :to="nextCompetency"
          class="
            border border-gray-300
            rounded-md
            shadow-md
            hover:text-teal-500 hover:border-teal-500
          "
        >
          <IconChevronRight class="h-8" />
        </router-link>
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { today } from "../utils/date";
import { fathers } from "../utils/competency";
import Loading from "../components/Loading.vue";
import EvalCompetency from "../components/EvalCompetency.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconChevronUp from "../icons/IconChevronUp.vue";
import { useTitle } from "@vueuse/core";

useTitle("Évaluation d'une compétence - soklaki.fr");

const store = useStore();
const route = useRoute();

const loading = ref(true);

const competencyId = computed(() =>
  route.params.id == null ? null : Number(route.params.id)
);
const competencyById = computed(() => store.getters.competencyById);

const studentById = computed(() => store.getters.studentById);

const containerById = computed(() => store.getters.containerById);
const competencyFathers = computed(() => fathers(store, competencyId.value));

const evaluations = ref([]);
const observations = ref([]);
const competencies = ref([]);

const students = computed(() => {
  const period = store.state.periods[store.state.currentPeriod];
  const full = period.students.map((x) =>
    store.getters.studentById(x.student.id)
  );
  return full.filter(
    (x) => x.current_cycle.current_cycle === route.params.cycle
  );
});

const searchEvaluation = (studentId) => {
  // evaluations are sorted by date desc, so the first one is the one I'm looking for
  return evaluations.value.find((e) => {
    if (e.student_id === studentId && e.competency_id == route.params.id) {
      return true;
    }
    return false;
  });
};

const evaluationByStudent = computed(() => {
  const e = {};
  for (const student of students.value) {
    // Search for an existing evaluation
    const evaluation = searchEvaluation(student.id);
    if (evaluation == null) {
      // No evaluation yet
      e[student.id] = {
        id: null,
        comment: null,
        status: "Emtpy",
      };
    } else {
      e[student.id] = {
        id: evaluation.id,
        comment: evaluation.comment,
        status: evaluation.status,
      };
    }
  }
  return e;
});

const saveEvaluation = async (studentId, { comment, status }) => {
  const evaluation = searchEvaluation(studentId);
  if (evaluation == null) {
    const e = await store.dispatch("insertEvaluation", {
      studentId: studentId,
      competencyId: Number(route.params.id),
      periodId: store.state.currentPeriod,
      date: today(),
      status: status,
      comment: comment,
    });
    evaluations.value.push(e);
  } else {
    await store.dispatch("updateEvaluation", {
      id: evaluation.id,
      comment: comment,
      date: today(),
      status: status,
      periodId: store.state.currentPeriod,
    });
    evaluation.comment = comment;
    evaluation.status = status;
  }
};

const cancelEvaluation = (studentId) => {
  // nothing to do :)
};

const previousCompetency = computed(() => {
  const current = competencies.value.findIndex((x) => x == route.params.id);
  if (current === -1) {
    // Oups ?
    return "";
  } else if (current === 0) {
    return `/evaluations-by-cycle/${route.params.cycle}`;
  } else {
    const previous = competencies.value[current - 1];
    return `/evaluation/${route.params.cycle}/${previous}`;
  }
});
const nextCompetency = computed(() => {
  const current = competencies.value.findIndex((x) => x == route.params.id);
  if (current === -1) {
    // Oups ?
    return "";
  } else if (current === competencies.value.length - 1) {
    return `/evaluation/${route.params.cycle}/comment`;
  } else {
    const next = competencies.value[current + 1];
    return `/evaluation/${route.params.cycle}/${next}`;
  }
});

const getEvaluations = async () => {
  if (route.params.id == null) {
    // Of course
    return;
  }
  const data = await store.dispatch("evaluationsByCompetency", {
    competencyId: Number(route.params.id),
    cycle: route.params.cycle,
  });
  evaluations.value = data.evaluations;
  observations.value = data.observations;
  competencies.value = data.competencies.map((x) => x.id);
};

watch(
  () => route.params.id,
  async () => {
    loading.value = true;
    await getEvaluations();
    loading.value = false;
  }
);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await getEvaluations();
  loading.value = false;
});
</script>
