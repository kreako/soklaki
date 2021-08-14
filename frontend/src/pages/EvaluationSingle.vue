<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">
        Évaluation - {{ competency.full_rank }} - {{ student.firstname }}
        {{ student.lastname }}
      </div>
      <div class="mt-4">
        <div class="uppercase tracking-wide text-gray-700 text-xs">
          {{ competency.parent.rank }}.
          {{ competency.parent.text }}
        </div>
        <div
          v-if="competency.parent.parent != null"
          class="text-gray-700 text-xs"
        >
          {{ competency.parent.parent.rank }}.
          {{ competency.parent.parent.text }}
        </div>
        <div>
          {{ competency.rank }}.
          {{ competency.text }}
        </div>
      </div>
      <div class="mt-8">
        <div class="flex flex-col items-end text-xs text-gray-700">
          <div
            v-if="!evaluation.from_current_period"
            class="flex items-center space-x-1"
          >
            <IconExclamation class="h-4" />
            <div>
              Cette évaluation n'a pas encore été mise à jour pour cette
              période.
            </div>
          </div>
          <div>le {{ evaluation.date }} par {{ evaluation.user.initials }}</div>
        </div>
        <EvalCompetency
          :edit="true"
          :comment="evaluation.comment"
          :status="evaluation.status"
          @save="saveEvaluation"
          @cancel="cancelEvaluation"
        />
        <div class="mt-12">
          <div class="flex flex-row justify-center space-x-2">
            <router-link
              v-if="competency.previous != null"
              :to="`/evaluation-single/${route.params.cycle}/${competency.previous.id}/${route.params.studentId}`"
              class="
                border border-gray-300
                rounded-md
                shadow-md
                hover:text-teal-500 hover:border-teal-500
              "
            >
              <IconChevronLeft class="h-8 text-gray-700" />
            </router-link>
            <router-link
              v-if="competency.next != null"
              :to="`/evaluation-single/${route.params.cycle}/${competency.next.id}/${route.params.studentId}`"
              class="
                border border-gray-300
                rounded-md
                shadow-md
                hover:text-teal-500 hover:border-teal-500
              "
            >
              <IconChevronRight class="h-8 text-gray-700" />
            </router-link>
          </div>
        </div>
        <div class="mt-12">
          <div class="flex items-center space-x-4">
            <div class="form-label">
              {{ observations.length }}
              <span v-if="observations.length > 1">observations</span>
              <span v-else>observation</span>
            </div>
            <router-link
              :to="`/new-observation-prefill/${route.params.studentId}/${route.params.competencyId}`"
              class="text-xs hover:text-teal-500"
            >
              En ajoutez-une ?
            </router-link>
          </div>
          <div v-for="o in observations" class="mb-1 mt-2">
            <div class="flex flex-row space-x-4 items-center">
              <div>
                {{ o.date }}
              </div>
              <div class="text-xs rounded-full px-1 border border-gray-600">
                {{ o.user.initials }}
              </div>
            </div>
            <div class="whitespace-pre ml-1">
              {{ o.text }}
            </div>
          </div>
        </div>
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
import { userInitials } from "../utils/user";
import EvalCompetency from "../components/EvalCompetency.vue";
import Loading from "../components/Loading.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconExclamation from "../icons/IconExclamation.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";
import { useTitle } from "@vueuse/core";

useTitle("Évaluation - soklaki.fr");

const store = useStore();
const route = useRoute();

const loading = ref(true);

const evaluation = ref(null);
const observations = ref(null);
const student = ref(null);
const competency = ref(null);

const saveEvaluation = async ({ comment, status }) => {
  let date = today();
  await store.dispatch("evaluationNew", {
    studentId: route.params.studentId,
    competencyId: route.params.competencyId,
    status: status,
    comment: comment,
    date: date,
  });
  evaluation.value.status = status;
  evaluation.value.comment = comment;
  evaluation.value.date = date;
  evaluation.value.from_current_period = true;
};

const cancelEvaluation = () => {};

const getEvaluation = async () => {
  if (route.params.competencyId == null || route.params.studentId == null) {
    // ok... Still at init... wait for it
    return;
  }
  loading.value = true;
  const data = await store.dispatch("evaluationSingle", {
    competencyId: route.params.competencyId,
    studentId: route.params.studentId,
  });
  observations.value = data.observations;
  evaluation.value = data.evaluation;
  competency.value = data.competency;
  student.value = data.student;
  useTitle(
    `Évaluation ${data.competency.full_rank} - ${data.student.firstname} ${data.student.lastname} - soklaki.fr`
  );
  loading.value = false;
};

watch(
  () => [route.params.competencyId, route.params.studentId],
  async () => {
    await getEvaluation();
  }
);

onMounted(async () => {
  await getEvaluation();
});
</script>
