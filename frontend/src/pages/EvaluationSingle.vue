<template>
  <div class="my-4 px-2">
    <div class="form-label">
      Évaluation - {{ competencyById(competencyId).full_rank }}
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
      <div class="mt-14">
        <div class="form-label">
          {{ studentById(studentId).firstname }}
          {{ studentById(studentId).lastname }}
        </div>
        <div class="mt-2">
          <EvalCompetency
            :edit="edit"
            :comment="evaluation.comment"
            :status="evaluation.status"
            @save="saveEvaluation"
            @cancel="cancelEvaluation"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { today } from "../utils/date";
import { fathers } from "../utils/competency";
import EvalCompetency from "../components/EvalCompetency.vue";

const store = useStore();
const route = useRoute();

const competencyId = computed(() =>
  route.params.competencyId == null ? null : Number(route.params.competencyId)
);
const competencyById = computed(() => store.getters.competencyById);

const studentById = computed(() => store.getters.studentById);
const studentId = computed(() =>
  route.params.studentId == null ? null : Number(route.params.studentId)
);

const containerById = computed(() => store.getters.containerById);
const competencyFathers = computed(() => fathers(store, competencyId.value));

const edit = ref(true);

const evaluation = computed(() => store.state.evaluations.evaluation);

const saveEvaluation = async ({ comment, status }) => {
  if (evaluation.value.id == null) {
    await store.dispatch("insertEvaluation", {
      studentId: studentId.value,
      competencyId: competencyId.value,
      periodId: store.state.currentPeriod,
      date: today(),
      status: status,
      comment: comment,
    });
  } else {
    await store.dispatch("updateEvaluation", {
      id: evaluation.value.id,
      comment: comment,
      date: today(),
      status: status,
      periodId: store.state.currentPeriod,
    });
  }
  await store.dispatch("evaluationSingle", {
    competencyId: competencyId.value,
    periodId: store.state.currentPeriod,
    studentId: studentId.value,
  });
  edit.value = false;
};

const cancelEvaluation = () => {
  edit.value = false;
};

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("evaluationSingle", {
    competencyId: competencyId.value,
    periodId: store.state.currentPeriod,
    studentId: studentId.value,
  });
});
</script>
