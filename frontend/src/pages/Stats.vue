<template>
  <div class="my-4 px-2">
    mobile : {{ mobile }}
    <div class="form-label">Plein de statistiques !</div>
    <div class="mt-4 form-sub-label">Cycle 1</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c1" @selectedCompetency="selectCompetency" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 2</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c2" @selectedCompetency="selectCompetency" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 3</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c3" @selectedCompetency="selectCompetency" />
    </div>
    <div class="mt-20 form-sub-label">Cycle 4</div>
    <div class="mt-2">
      <StatsDetails :stats="stats.c4" @selectedCompetency="selectCompetency" />
    </div>
  </div>
  <TransitionRoot appear :show="showCompetencyModal" as="template">
    <Dialog
      as="div"
      static
      :open="showCompetencyModal"
      @close="showCompetencyModal = false"
    >
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="min-h-screen md:px-4 text-center">
          <!--
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0"
            enter-to="opacity-0"
            leave="duration-200 ease-in"
            leave-from="opacity-0"
            leave-to="opacity-0"
          >-->
          <DialogOverlay class="fixed inset-0 bg-black opacity-50" />
          <!--</TransitionChild>-->

          <span class="inline-block h-screen align-middle" aria-hidden="true">
            &#8203;
          </span>

          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <div
              class="inline-block w-full max-w-md p-6 md:my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
            >
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-gray-900"
              >
                La compétence {{ competencyById(selectedCompetency).full_rank }}
              </DialogTitle>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  {{ competencyById(selectedCompetency).text }}
                </p>
              </div>

              <div class="mt-4">
                <button
                  type="button"
                  class="inline-flex justify-center px-4 py-2 text-sm font-medium text-blue-900 bg-blue-100 border border-transparent rounded-md hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                  @click="showCompetencyModal = false"
                >
                  OK
                </button>
              </div>
            </div>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { until } from "@vueuse/core";
import StatsDetails from "../components/StatsDetails.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
  DialogTitle,
} from "@headlessui/vue";
import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";

const store = useStore();

const stats = computed(() => store.state.stats);

const breakpoints = useBreakpoints(breakpointsTailwind);
const mobile = breakpoints.smaller("md");

const competencyById = computed(() => store.getters.competencyById);

const selectedCompetency = ref(null);
const showCompetencyModal = ref(false);
const selectCompetency = (id) => {
  selectedCompetency.value = id;
  showCompetencyModal.value = true;
};

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("stats", { periodId: store.state.currentPeriod });
});
</script>
