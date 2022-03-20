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
            @trash="trashContainer(socle[selectedCycle], $event)"
            @moveUp="moveUpContainer(socle[selectedCycle], $event)"
            @moveDown="moveDownContainer(socle[selectedCycle], $event)"
            @add="goToNewContainer(null, socle[selectedCycle])"
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
                @trash="trashContainer(containerL1.children, $event)"
                @moveUp="moveUpContainer(containerL1.children, $event)"
                @moveDown="moveDownContainer(containerL1.children, $event)"
                @add="goToNewContainer(selectedL1, containerL1.children)"
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
                @trash="trashCompetency(containerL2.competencies, $event)"
                @moveUp="moveUpCompetency(containerL2.competencies, $event)"
                @moveDown="moveDownCompetency(containerL2.competencies, $event)"
                @add="goToNewCompetency(selectedL2, containerL2.competencies)"
                @move="goToMoveCompetency($event, containerL2.competencies)"
                :movable="true"
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
                @trash="trashCompetency(containerL1.competencies, $event)"
                @moveUp="moveUpCompetency(containerL1.competencies, $event)"
                @moveDown="moveDownCompetency(containerL1.competencies, $event)"
                @add="goToNewCompetency(selectedL1, containerL1.competencies)"
                @move="goToMoveCompetency($event, containerL1.competencies)"
                :movable="true"
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
        <input
          @keyup.enter="confirmContainerEdit"
          type="text"
          v-model="containerText"
          class="input w-full"
        />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Modification du titre"
      :show="showEditCompetencyModal"
      @confirm="confirmCompetencyEdit"
      @cancel="cancelCompetencyEdit"
    >
      <div>
        <input
          @keyup.enter="confirmCompetencyEdit"
          type="text"
          v-model="competencyText"
          class="input w-full"
        />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Suppression d'un domaine/sous domaine"
      :show="showTrashContainerModal"
      @confirm="confirmContainerTrash"
      @cancel="cancelContainerTrash"
    >
      <div>Êtes-vous sur de vouloir supprimer ce domaine/sous domaine ?</div>
      <div class="mt-2 font-mono">
        {{ containerById(containerTrash.id).full_rank }}
        {{ containerById(containerTrash.id).text }}
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Suppression d'une compétence"
      :show="showTrashCompetencyModal"
      @confirm="confirmCompetencyTrash"
      @cancel="cancelCompetencyTrash"
    >
      <div>Êtes-vous sur de vouloir supprimer cette compétence ?</div>
      <div class="mt-2 font-mono">
        {{ competencyById(competencyTrash.id).full_rank }}
        {{ competencyById(competencyTrash.id).text }}
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Nouveau domaine/sous domaine"
      :show="showNewContainerModal"
      @confirm="confirmContainerNew"
      @cancel="cancelContainerNew"
    >
      <div>
        <input
          @keyup.enter="confirmContainerNew"
          type="text"
          v-model="containerText"
          class="input w-full"
        />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Nouvelle compétence"
      :show="showNewCompetencyModal"
      @confirm="confirmCompetencyNew"
      @cancel="cancelCompetencyNew"
    >
      <div>
        <input
          @keyup.enter="confirmCompetencyNew"
          type="text"
          v-model="competencyText"
          class="input w-full"
        />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Déplacer cette compétence dans un autre domaine/sous domaine"
      :show="showMoveCompetencyModal"
      @confirm="confirmCompetencyMove"
      @cancel="cancelCompetencyMove"
    >
      <div>
        <ContainerSelector
          @selected="selectedMoveContainer"
          :cycle="selectedCycle"
        />
      </div>
    </ModalConfirmCancel>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle, until } from "@vueuse/core";
import { computed, ref, onMounted, watchEffect, watch } from "vue";
import Loading from "../components/Loading.vue";
import ContainerSelector from "../components/ContainerSelector.vue";
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

const showNewContainerModal = ref(false);
const newContainerRank = ref(null);
const newContainerParentId = ref(null);
const goToNewContainer = (containerParentId, list) => {
  newContainerRank.value =
    store.getters.containerById(list[list.length - 1].id).rank + 1;
  newContainerParentId.value = containerParentId;
  showNewContainerModal.value = true;
};
const confirmContainerNew = async () => {
  await store.dispatch("insertSocleContainer", {
    containerId: newContainerParentId.value,
    cycle: selectedCycle.value,
    rank: newContainerRank.value,
    text: containerText.value,
  });
  showNewContainerModal.value = false;
};
const cancelContainerNew = () => {
  showNewContainerModal.value = false;
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

const showNewCompetencyModal = ref(false);
const newCompetencyRank = ref(null);
const newCompetencyParentId = ref(null);
const goToNewCompetency = (competencyParentId, list) => {
  newCompetencyRank.value =
    store.getters.competencyById(list[list.length - 1].id).rank + 1;
  newCompetencyParentId.value = competencyParentId;
  showNewCompetencyModal.value = true;
};
const confirmCompetencyNew = async () => {
  await store.dispatch("insertSocleCompetency", {
    containerId: newCompetencyParentId.value,
    cycle: selectedCycle.value,
    rank: newCompetencyRank.value,
    text: competencyText.value,
  });
  showNewCompetencyModal.value = false;
};
const cancelCompetencyNew = () => {
  showNewCompetencyModal.value = false;
};

const showTrashContainerModal = ref(false);
const containerTrash = ref(null);
const containerTrashAfter = ref([]);
const trashContainer = (list, id) => {
  const idx = list.findIndex((x) => x.id == id);
  containerTrashAfter.value = [];
  for (let i = idx + 1; i < list.length; i++) {
    containerTrashAfter.value.push(list[i].id);
  }
  containerTrash.value = id;
  showTrashContainerModal.value = true;
};
const confirmContainerTrash = async () => {
  for (const id of containerTrashAfter.value) {
    const container = store.getters.containerById(id);
    await store.dispatch("updateSocleContainerRank", {
      id: id,
      rank: container.rank - 1,
    });
  }
  await store.dispatch("updateSocleContainerActive", {
    id: containerTrash.value,
    active: false,
  });
  showTrashContainerModal.value = false;
};
const cancelContainerTrash = () => {
  showTrashContainerModal.value = false;
};

const showTrashCompetencyModal = ref(false);
const competencyTrash = ref(null);
const competencyTrashAfter = ref([]);
const trashCompetency = (list, id) => {
  const idx = list.findIndex((x) => x.id == id);
  competencyTrashAfter.value = [];
  for (let i = idx + 1; i < list.length; i++) {
    competencyTrashAfter.value.push(list[i].id);
  }
  competencyTrash.value = id;
  showTrashCompetencyModal.value = true;
};
const confirmCompetencyTrash = async () => {
  for (const id of competencyTrashAfter.value) {
    const competency = store.getters.competencyById(id);
    await store.dispatch("updateSocleCompetencyRank", {
      id: id,
      rank: competency.rank - 1,
    });
  }
  await store.dispatch("updateSocleCompetencyActive", {
    id: competencyTrash.value,
    active: false,
  });
  showTrashCompetencyModal.value = false;
};
const cancelCompetencyTrash = () => {
  showTrashCompetencyModal.value = false;
};

const moveUpContainer = async (list, id) => {
  const container = store.getters.containerById(id);
  if (container.rank == 1) {
    // Already on top
    return;
  }
  // Update the container
  await store.dispatch("updateSocleContainerRank", {
    id: id,
    rank: container.rank - 1,
  });
  // Find the container before
  const idx = list.findIndex((x) => x.id == id) - 1;
  const before = store.getters.containerById(list[idx].id);
  await store.dispatch("updateSocleContainerRank", {
    id: before.id,
    rank: before.rank + 1,
  });
  // Now reload the socle
  await store.dispatch("socle");
};

const moveDownContainer = async (list, id) => {
  // Find the container after
  const idx = list.findIndex((x) => x.id == id) + 1;
  if (list.length <= idx) {
    // last of the list, do nothing
    return;
  }
  const after = store.getters.containerById(list[idx].id);
  const container = store.getters.containerById(id);
  // Update the container
  await store.dispatch("updateSocleContainerRank", {
    id: id,
    rank: container.rank + 1,
  });
  await store.dispatch("updateSocleContainerRank", {
    id: after.id,
    rank: after.rank - 1,
  });
  // Now reload the socle
  await store.dispatch("socle");
};

const moveUpCompetency = async (list, id) => {
  const competency = store.getters.competencyById(id);
  if (competency.rank == 1) {
    // Already on top
    return;
  }
  // Update the container
  await store.dispatch("updateSocleCompetencyRank", {
    id: id,
    rank: competency.rank - 1,
  });
  // Find the competency before
  const idx = list.findIndex((x) => x.id == id) - 1;
  const before = store.getters.competencyById(list[idx].id);
  await store.dispatch("updateSocleCompetencyRank", {
    id: before.id,
    rank: before.rank + 1,
  });
  // Now reload the socle
  await store.dispatch("socle");
};

const moveDownCompetency = async (list, id) => {
  // Find the competency after
  const idx = list.findIndex((x) => x.id == id) + 1;
  if (list.length <= idx) {
    // last of the list, do nothing
    return;
  }
  const after = store.getters.competencyById(list[idx].id);
  const competency = store.getters.competencyById(id);
  // Update the competency
  await store.dispatch("updateSocleCompetencyRank", {
    id: id,
    rank: competency.rank + 1,
  });
  await store.dispatch("updateSocleCompetencyRank", {
    id: after.id,
    rank: after.rank - 1,
  });
  // Now reload the socle
  await store.dispatch("socle");
};

// Modal toggle
const showMoveCompetencyModal = ref(false);
// id of the competency to move
const selectMoveCompetency = ref(null);
// list of competency after the one to move that need a rank update
// after a successful move
const selectMoveCompetencyAfterList = ref([]);
// Container id where to move the competency, as selected by ContainerSelector
const selectMoveContainer = ref(null);
const goToMoveCompetency = (id, list) => {
  selectMoveContainer.value = null;
  selectMoveCompetencyAfterList.value = [];
  const idx = list.findIndex((x) => x.id == id);
  for (let i = idx + 1; i < list.length; i++) {
    selectMoveCompetencyAfterList.value.push(list[i].id);
  }
  selectMoveCompetency.value = id;
  showMoveCompetencyModal.value = true;
};
const selectedMoveContainer = (id) => {
  selectMoveContainer.value = id;
};
const confirmCompetencyMove = async () => {
  if (selectMoveContainer.value == null) {
    // No container selected, do nothing
    return;
  }
  const c = store.getters.competencyById(selectMoveCompetency.value);
  if (selectMoveContainer.value == c.container_id) {
    // Move into the container where I already belong ? Too easy
    showMoveCompetencyModal.value = false;
    return;
  }
  for (const id of selectMoveCompetencyAfterList.value) {
    const competency = store.getters.competencyById(id);
    await store.dispatch("updateSocleCompetencyRank", {
      id: id,
      rank: competency.rank - 1,
    });
  }
  await store.dispatch("updateSocleCompetencyContainerId", {
    id: selectMoveCompetency.value,
    containerId: selectMoveContainer.value,
  });
  showMoveCompetencyModal.value = false;
};
const cancelCompetencyMove = () => {
  showMoveCompetencyModal.value = false;
};

watchEffect(() => {
  router.push({
    query: {
      cycle: selectedCycle.value,
      l1: selectedL1.value,
      l2: selectedL2.value,
      competency: selectedCompetency.value,
    },
  });
});

watch(route, () => {
  if (route.path !== "/socle/edit") {
    // Not my page
    return;
  }
  if (route.query.cycle != selectedCycle.value) {
    selectedCycle.value = route.query.cycle;
  }
  if (route.query.l1 != selectedL1.value) {
    selectedL1.value = route.query.l1;
  }
  if (route.query.l2 != selectedL2.value) {
    selectedL2.value = route.query.l2;
  }
  if (route.query.competency != selectedCompetency.value) {
    selectedCompetency.value = route.query.competency;
  }
});

onMounted(async () => {
  await until(() => store.state.socle.c1.length > 0).toBeTruthy();
  await store.dispatch("competenciesSorted");
  loading.value = false;
});
</script>
