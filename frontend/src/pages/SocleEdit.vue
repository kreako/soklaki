<template>
  <div class="my-4 px-2">
    <div>
      <div class="cursor-pointer" @click="selectCycle(null)">
        <IconHome class="h-4" />
      </div>
      <div v-if="selectedCycle" class="pl-2">
        <div class="cursor-pointer" @click="selectL1(null)">
          {{ cycle.text }}
        </div>
        <div v-if="selectedL1" class="pl-2">
          <div class="cursor-pointer" @click="selectL2(null)">
            {{ containerById(containerL1.id).full_rank }}
            {{ containerById(containerL1.id).text }}
          </div>
          <div v-if="selectedL2" class="pl-2">
            <div class="cursor-pointer" @click="selectCompetency(null)">
              {{ containerById(containerL2.id).full_rank }}
              {{ containerById(containerL2.id).text }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-row items-stretch mt-8">
      <div class="flex-grow">
        <MillerColumn
          :list="cycles"
          title="Cycles"
          @selected="selectCycle"
          :hide="selectedCycle != null"
          v-slot="{ item }"
        >
          {{ item.text }}
        </MillerColumn>
        <MillerColumn
          v-if="selectedCycle"
          :list="socle[selectedCycle]"
          title="Domaines"
          @selected="selectL1"
          :hide="selectedL1 != null"
          v-slot="{ item }"
        >
          {{ containerById(item.id).full_rank }}
          {{ containerById(item.id).text }}
        </MillerColumn>
        <div v-if="selectedL1">
          <div v-if="containerL1.children.length > 0">
            <MillerColumn
              :list="containerL1.children"
              title="Sous domaines"
              @selected="selectL2"
              :hide="selectedL2 != null"
              v-slot="{ item }"
            >
              {{ containerById(item.id).full_rank }}
              {{ containerById(item.id).text }}
            </MillerColumn>
            <MillerColumn
              v-if="selectedL2"
              :list="containerL2.competencies"
              title="Compétences"
              @selected="selectCompetency"
              :hide="selectedCompetency != null"
              v-slot="{ item }"
            >
              {{ competencyById(item.id).full_rank }}
              {{ competencyById(item.id).text }}
            </MillerColumn>
            <div v-if="selectedCompetency">
              <SocleEditCompetency :competency="competency" />
            </div>
          </div>
          <div v-else>
            <MillerColumn
              :list="containerL1.competencies"
              title="Compétences"
              @selected="selectCompetency"
              :hide="selectedCompetency != null"
              v-slot="{ item }"
            >
              {{ competencyById(item.id).full_rank }}
              {{ competencyById(item.id).text }}
            </MillerColumn>
            <div v-if="selectedCompetency">
              <SocleEditCompetency :competency="competency" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import IconHome from "../icons/IconHome.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import MillerColumn from "../components/MillerColumn.vue";
import SocleEditCompetency from "../components/SocleEditCompetency.vue";

useTitle("Socle modification - soklaki.fr");

const store = useStore();
const route = useRoute();

const socle = computed(() => store.state.socle);

const containerById = computed(() => store.getters.containerById);
const competencyById = computed(() => store.getters.competencyById);

const cycles = [
  { id: "c1", text: "Cycle 1" },
  { id: "c2", text: "Cycle 2" },
  { id: "c3", text: "Cycle 3" },
  { id: "c4", text: "Cycle 4" },
];

const depthNavigation = ref(0);

const goBackToL1 = () => {
  selectedL2.value = null;
  selectedCompetency.value = null;
};

const selectedCycle = ref(null);
const selectCycle = async (id) => {
  depthNavigation.value = 0;
  selectedCycle.value = id;
  selectedL1.value = null;
  selectedL2.value = null;
  selectedCompetency.value = null;
};

const cycle = computed(() => {
  if (selectedCycle.value == null) {
    return { id: null, text: null };
  }
  return cycles.find((x) => x.id === selectedCycle.value);
});

const selectedL1 = ref(null);
const selectL1 = async (id) => {
  depthNavigation.value = 1;
  selectedL1.value = id;
  selectedL2.value = null;
  selectedCompetency.value = null;
};

const containerL1 = computed(() => {
  if (selectedCycle.value == null) {
    return store.getters.containerById(null);
  }
  return store.state.socle[selectedCycle.value].find(
    (x) => x.id === selectedL1.value
  );
});

const selectedL2 = ref(null);
const selectL2 = async (id) => {
  depthNavigation.value = 2;
  selectedL2.value = id;
  selectedCompetency.value = null;
};

const containerL2 = computed(() => {
  if (selectedCycle.value == null) {
    return store.getters.containerById(null);
  }
  if (selectedL1.value == null) {
    return store.getters.containerById(null);
  }
  return store.state.socle[selectedCycle.value]
    .find((x) => x.id === selectedL1.value)
    .children.find((x) => x.id === selectedL2.value);
});

const selectedCompetency = ref(null);
const selectCompetency = async (id) => {
  depthNavigation.value = 3;
  selectedCompetency.value = id;
};

const competency = computed(() => {
  if (selectedCycle.value == null) {
    return store.getters.containerById(null);
  }
  if (selectedL1.value == null) {
    return store.getters.containerById(null);
  }
  if (selectedL2.value == null) {
    return store.state.socle[selectedCycle.value]
      .find((x) => x.id === selectedL1.value)
      .competencies.find((x) => x.id === selectedCompetency.value);
  } else {
    return store.state.socle[selectedCycle.value]
      .find((x) => x.id === selectedL1.value)
      .children.find((x) => x.id === selectedL2.value)
      .competencies.find((x) => x.id === selectedCompetency.value);
  }
});

// TODO store actions
// insertSocleContainer
// insertSocleCompetency
// insertSocleSubject
// insertSocleCompetencySubject
// updateSocleContainerActive
// updateSocleCompetencyActive
// updateSocleSubjectActive
// updateSocleCompetencySubjectActive
// updateSocleContainerContainerId
// updateSocleCompetencyContainerId
// updateSocleContainerRank
// updateSocleCompetencyRank
// updateSocleContainerText
// updateSocleCompetencyText
// updateSocleSubjectText
</script>
