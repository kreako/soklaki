<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div>
        <div
          class="cursor-pointer hover:text-teal-500"
          @click="selectCycle(null)"
        >
          <IconHome class="h-4" />
        </div>
        <div v-if="selectedCycle" class="pl-2">
          <div
            class="cursor-pointer hover:text-teal-500"
            @click="selectL1(null)"
          >
            {{ cycle.text }}
          </div>
          <div v-if="selectedL1" class="pl-2">
            <div
              class="cursor-pointer hover:text-teal-500"
              @click="selectL2(null)"
            >
              {{ containerById(containerL1.id).full_rank }}
              {{ containerById(containerL1.id).text }}
            </div>
            <div v-if="selectedL2" class="pl-2">
              <div
                class="cursor-pointer hover:text-teal-500"
                @click="selectCompetency(null)"
              >
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
            :editable="false"
            v-slot="{ item }"
          >
            {{ item.text }}
          </MillerColumn>
          <MillerColumn
            v-if="selectedCycle"
            :list="socle[selectedCycle]"
            title="Domaines"
            addLabel="Ajouter un domaine"
            @selected="selectL1"
            @edit="goToEditContainer"
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
                addLabel="Ajouter un sous domaine"
                @selected="selectL2"
                @edit="goToEditContainer"
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
                addLabel="Ajouter une compétence"
                @selected="selectCompetency"
                @edit="goToEditCompetency"
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
                addLabel="Ajouter une compétence"
                @selected="selectCompetency"
                @edit="goToEditCompetency"
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
    </Loading>
    <ModalConfirmCancel
      title="Modification du titre"
      :show="showEditContainerModal"
      @confirm="confirmContainerEdit"
      @cancel="cancelContainerEdit"
    >
      <div>
        <input type="text" v-model="containerText" class="input w-full" />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Modification du titre"
      :show="showEditCompetencyModal"
      @confirm="confirmCompetencyEdit"
      @cancel="cancelCompetencyEdit"
    >
      <div>
        <input type="text" v-model="competencyText" class="input w-full" />
      </div>
    </ModalConfirmCancel>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle, until } from "@vueuse/core";
import { computed, ref, onMounted, watchEffect } from "vue";
import Loading from "../components/Loading.vue";
import IconHome from "../icons/IconHome.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import MillerColumn from "../components/MillerColumn.vue";
import SocleEditCompetency from "../components/SocleEditCompetency.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";

useTitle("Socle modification - soklaki.fr");

const store = useStore();
const route = useRoute();
const router = useRouter();

const socle = computed(() => store.state.socle);

const containerById = computed(() => store.getters.containerById);
const competencyById = computed(() => store.getters.competencyById);

const loading = ref(true);

const cycles = [
  { id: "c1", text: "Cycle 1" },
  { id: "c2", text: "Cycle 2" },
  { id: "c3", text: "Cycle 3" },
  { id: "c4", text: "Cycle 4" },
];

const selectedCycle = ref(route.query.cycle);
const selectCycle = async (id) => {
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

const selectedL1 = ref(route.query.l1);
const selectL1 = async (id) => {
  selectedL1.value = id;
  selectedL2.value = null;
  selectedCompetency.value = null;
};

const containerL1 = computed(() => {
  if (selectedCycle.value == null) {
    return store.getters.containerById(null);
  }
  return store.state.socle[selectedCycle.value].find(
    (x) => x.id == selectedL1.value
  );
});

const selectedL2 = ref(route.query.l2);
const selectL2 = async (id) => {
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
    .find((x) => x.id == selectedL1.value)
    .children.find((x) => x.id == selectedL2.value);
});

const selectedCompetency = ref(route.query.competency);
const selectCompetency = async (id) => {
  selectedCompetency.value = id;
};

const competency = computed(() => {
  if (selectedCycle.value == null) {
    return store.getters.competencyById(null);
  }
  if (selectedL1.value == null) {
    return store.getters.competencyById(null);
  }
  if (selectedL2.value == null) {
    return store.state.socle[selectedCycle.value]
      .find((x) => x.id == selectedL1.value)
      .competencies.find((x) => x.id == selectedCompetency.value);
  } else {
    return store.state.socle[selectedCycle.value]
      .find((x) => x.id == selectedL1.value)
      .children.find((x) => x.id == selectedL2.value)
      .competencies.find((x) => x.id == selectedCompetency.value);
  }
});

const showEditContainerModal = ref(false);
const containerText = ref("");
const containerId = ref(null);
const goToEditContainer = (id) => {
  showEditContainerModal.value = true;
  containerText.value = store.getters.containerById(id).text;
  containerId.value = id;
};
const confirmContainerEdit = async () => {
  await store.dispatch("updateSocleContainerText", {
    id: containerId.value,
    text: containerText.value,
  });
  showEditContainerModal.value = false;
};
const cancelContainerEdit = () => {
  showEditContainerModal.value = false;
};

const showEditCompetencyModal = ref(false);
const competencyText = ref("");
const competencyId = ref(null);
const goToEditCompetency = (id) => {
  showEditCompetencyModal.value = true;
  competencyText.value = store.getters.competencyById(id).text;
  competencyId.value = id;
};
const confirmCompetencyEdit = async () => {
  await store.dispatch("updateSocleCompetencyText", {
    id: competencyId.value,
    text: competencyText.value,
  });
  showEditCompetencyModal.value = false;
};
const cancelCompetencyEdit = () => {
  showEditCompetencyModal.value = false;
};

watchEffect(() => {
  router.replace({
    query: {
      cycle: selectedCycle.value,
      l1: selectedL1.value,
      l2: selectedL2.value,
      competency: selectedCompetency.value,
    },
  });
});

onMounted(async () => {
  await until(() => store.state.socle.c1.length > 0).toBeTruthy();
  loading.value = false;
});
</script>
