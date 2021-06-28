<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
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
            <div v-if="observations.length > 0" class="text-sm">
              <Disclosure>
                <DisclosureButton>
                  <div
                    class="text-gray-700 flex flex-row items-center space-x-2"
                  >
                    <div>
                      {{ observations.length }}
                      <span v-if="observations.length > 1"> observations </span>
                      <span v-else> observation </span>
                    </div>
                    <IconChevronDown class="h-4 text-gray-400" />
                  </div>
                </DisclosureButton>
                <DisclosurePanel>
                  <div v-for="o in observations" class="mb-1">
                    <div class="flex flex-row space-x-4 items-center">
                      <div>
                        {{ o.date }}
                      </div>
                      <div
                        class="text-xs rounded-full px-1 border border-gray-600"
                      >
                        {{ userInitials(userById(o.user_id)) }}
                      </div>
                    </div>
                    <div>
                      {{ o.text }}
                    </div>
                  </div>
                </DisclosurePanel>
              </Disclosure>
            </div>
            <EvalCompetency
              :edit="true"
              :comment="evaluation.comment"
              :status="evaluation.status"
              @save="saveEvaluation"
              @cancel="cancelEvaluation"
            />
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
import IconChevronDown from "../icons/IconChevronDown.vue";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { useTitle } from "@vueuse/core";

useTitle("Évaluation - soklaki.fr");

const store = useStore();
const route = useRoute();

const loading = ref(true);

const competencyId = computed(() =>
  route.params.competencyId == null ? null : Number(route.params.competencyId)
);
const competencyById = computed(() => store.getters.competencyById);
const userById = computed(() => store.getters.userById);
const studentById = computed(() => store.getters.studentById);
const studentId = computed(() =>
  route.params.studentId == null ? null : Number(route.params.studentId)
);

const containerById = computed(() => store.getters.containerById);
const competencyFathers = computed(() => fathers(store, competencyId.value));

const evaluation = ref(null);
const observations = ref(null);

const saveEvaluation = async ({ comment, status }) => {
  if (evaluation.value.id == null) {
    const e = await store.dispatch("insertEvaluation", {
      studentId: studentId.value,
      competencyId: competencyId.value,
      periodId: store.state.currentPeriod,
      date: today(),
      status: status,
      comment: comment,
    });
    evaluation.value = e;
  } else {
    await store.dispatch("updateEvaluation", {
      id: evaluation.value.id,
      comment: comment,
      date: today(),
      status: status,
      periodId: store.state.currentPeriod,
    });
    evaluation.value.comment = comment;
    evaluation.value.status = status;
  }
};

const cancelEvaluation = () => {};

const getEvaluation = async () => {
  if (route.params.competencyId == null || route.params.studentId == null) {
    // ok... Still at init... wait for it
    return;
  }
  const data = await store.dispatch("evaluationSingle", {
    competencyId: competencyId.value,
    periodId: store.state.currentPeriod,
    studentId: studentId.value,
  });
  if (data.evaluations.length === 0) {
    // no evaluation
    evaluation.value = {
      id: null,
      comment: null,
      status: "Emtpy",
    };
  } else {
    evaluation.value = data.evaluations[0];
  }
  observations.value = data.observations;
};

watch(
  () => [route.params.competencyId, route.params.studentId],
  async () => {
    loading.value = true;
    await getEvaluation();
    loading.value = false;
  }
);

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await getEvaluation();
  loading.value = false;
});
</script>
