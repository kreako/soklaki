<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Évaluations - {{ competency.full_rank }}</div>
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
      <div class="">
        <div v-for="(by, idx) in byStudents" class="mt-32">
          <div class="uppercase text-md tracking-wide text-gray-700 font-bold">
            {{ by.student.firstname }}
            {{ by.student.lastname }}
          </div>
          <div class="flex flex-col items-end text-xs text-gray-700">
            <div
              v-if="!by.evaluation?.from_current_period"
              class="flex items-center space-x-1"
            >
              <IconExclamation class="h-4" />
              <div>
                L'évaluation n'a pas encore été faite sur cette période.
              </div>
            </div>
            <div
              v-if="by.evaluation != null && by.evaluation.status != 'Empty'"
            >
              le {{ by.evaluation?.date }} par
              {{ by.evaluation?.user?.initials }}
            </div>
          </div>
          <EvalCompetency
            :edit="true"
            :comment="by.evaluation?.comment"
            :status="by.evaluation?.status"
            @save="saveEvaluation(idx, $event)"
            @cancel="cancelEvaluation"
          />
          <div class="mt-8">
            <div class="flex items-center space-x-4">
              <div class="form-label">
                {{ by.observations.length }}
                <span v-if="by.observations.length > 1">observations</span>
                <span v-else>observation</span>
              </div>
              <router-link
                :to="`/new-observation-prefill/${by.student.id}/${route.params.id}`"
                class="text-xs hover:text-teal-500"
              >
                En ajoutez-une ?
              </router-link>
            </div>
            <div v-for="o in by.observations" class="mb-1 mt-2">
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
import { userInitials } from "../utils/user";
import Loading from "../components/Loading.vue";
import EvalCompetency from "../components/EvalCompetency.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconChevronUp from "../icons/IconChevronUp.vue";
import IconChevronDown from "../icons/IconChevronDown.vue";
import IconExclamation from "../icons/IconExclamation.vue";
import { useTitle } from "@vueuse/core";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";

useTitle("Évaluation d'une compétence - soklaki.fr");

const store = useStore();
const route = useRoute();

const loading = ref(true);

const byStudents = ref([]);
const competency = ref(null);

const saveEvaluation = async (studentIndex, { comment, status }) => {
  let date = today();
  await store.dispatch("evaluationNew", {
    studentId: byStudents.value[studentIndex].student.id,
    competencyId: route.params.id,
    status: status,
    comment: comment,
    date: date,
  });
  if (byStudents.value[studentIndex].evaluation == null) {
    byStudents.value[studentIndex].evaluation = {};
  }
  byStudents.value[studentIndex].evaluation.status = status;
  byStudents.value[studentIndex].evaluation.comment = comment;
  byStudents.value[studentIndex].evaluation.date = date;
  byStudents.value[studentIndex].evaluation.from_current_period = true;
  byStudents.value[studentIndex].evaluation.user.initials = null; //TODO
};

const cancelEvaluation = (studentId) => {
  // nothing to do :)
};

const previousCompetency = computed(() => {
  if (competency.value.previous == null) {
    return `/evaluations-by-cycle/${route.params.cycle}`;
  } else {
    return `/evaluation/${route.params.cycle}/${competency.value.previous.id}`;
  }
});
const nextCompetency = computed(() => {
  if (competency.value.next == null) {
    return `/evaluation/${route.params.cycle}/comment`;
  } else {
    return `/evaluation/${route.params.cycle}/${competency.value.next.id}`;
  }
});

const getEvaluations = async () => {
  if (route.params.id == null) {
    // Of course
    return;
  }
  loading.value = true;
  const data = await store.dispatch("evaluationMulti", {
    competencyId: route.params.id,
  });
  competency.value = data.competency;
  byStudents.value = data.by_students;
  useTitle(
    `Évaluations ${data.competency.full_rank} - ${route.params.cycle} - soklaki.fr`
  );
  loading.value = false;
};

watch(
  () => route.params.id,
  async () => {
    await getEvaluations();
  }
);

onMounted(async () => {
  await getEvaluations();
});
</script>
