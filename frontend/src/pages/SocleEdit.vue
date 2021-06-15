<template>
  <div class="my-4 px-2">
    <div>
      <IconHome class="h-4" />
      <div v-if="selectedCycle">
        {{ cycle.text }}
      </div>
      <div v-if="selectedL1">
        {{ containerById(containerL1.id).full_rank }}
        {{ containerById(containerL1.id).text }}
      </div>
      <div v-if="selectedL2">
        {{ containerById(containerL2.id).full_rank }}
        {{ containerById(containerL2.id).text }}
      </div>
      <div v-if="selectedCompetency">
        {{ competencyById(selectedCompetency).full_rank }}
        {{ competencyById(selectedCompetency).text }}
      </div>
    </div>
    <div>
      <MillerColumn :list="cycles" title="Cycles" @selected="selectCycle">
        <template v-slot:label="slot"> {{ slot.item.text }} </template>
        <template v-slot:child>
          <MillerColumn
            v-if="selectedCycle"
            :list="socle[selectedCycle]"
            title="Domaines"
            @selected="selectL1"
          >
            <template v-slot:label="slot">
              {{ containerById(slot.item.id).full_rank }}
              {{ containerById(slot.item.id).text }}
            </template>
            <template v-slot:child>
              <div v-if="selectedL1">
                <div v-if="containerL1.children.length > 0">
                  <MillerColumn
                    :list="containerL1.children"
                    title="Sous domaines"
                    @selected="selectL2"
                  >
                    <template v-slot:label="slot">
                      {{ containerById(slot.item.id).full_rank }}
                      {{ containerById(slot.item.id).text }}
                    </template>
                    <template v-slot:child>
                      {{ selectedL2 }}
                      <MillerColumn
                        v-if="selectedL2"
                        :list="containerL2.competencies"
                        title="Compétences"
                        @selected="selectCompetency"
                      >
                        <template v-slot:label="slot">
                          {{ competencyById(slot.item.id).full_rank }}
                          {{ competencyById(slot.item.id).text }}
                        </template>
                        <template v-slot:child>
                          <div v-if="selectedCompetency">
                            <div>Tags</div>
                            <div>
                              <div v-for="s in competency.subjects">
                                #{{ subjectById(s.subject_id).title }}
                              </div>
                            </div>
                            <div>Exemples</div>
                            <div>
                              <div v-for="t in competency.templates">
                                {{ templateById(t.id).text }}
                              </div>
                            </div>
                          </div>
                        </template>
                      </MillerColumn>
                    </template>
                  </MillerColumn>
                </div>
                <div v-else>
                  <MillerColumn
                    :list="containerL1.competencies"
                    title="Compétences"
                    @selected="selectCompetency"
                  >
                    <template v-slot:label="slot">
                      {{ competencyById(slot.item.id).full_rank }}
                      {{ competencyById(slot.item.id).text }}
                    </template>
                    <template v-slot:child>
                      <div v-if="selectedCompetency">
                        <div>Tags</div>
                        <div>
                          <div v-for="s in competency.subjects">
                            #{{ subjectById(s.subject_id).title }}
                          </div>
                        </div>
                        <div>Exemples</div>
                        <div>
                          <div v-for="t in competency.templates">
                            {{ templateById(t.id).text }}
                          </div>
                        </div>
                      </div>
                    </template>
                  </MillerColumn>
                </div>
              </div>
            </template>
          </MillerColumn>
        </template>
      </MillerColumn>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import IconHome from "../icons/IconHome.vue";
import MillerColumn from "../components/MillerColumn.vue";

useTitle("Socle modification - soklaki.fr");

const store = useStore();
const route = useRoute();

const socle = computed(() => store.state.socle);

const containerById = computed(() => store.getters.containerById);
const competencyById = computed(() => store.getters.competencyById);
const subjectById = computed(() => store.getters.subjectById);
const templateById = computed(() => store.getters.templateById);

const cycles = [
  { id: "c1", text: "Cycle 1" },
  { id: "c2", text: "Cycle 2" },
  { id: "c3", text: "Cycle 3" },
  { id: "c4", text: "Cycle 4" },
];

const selectedCycle = ref(null);
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

const selectedL1 = ref(null);
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
    (x) => x.id === selectedL1.value
  );
});

const selectedL2 = ref(null);
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
    .find((x) => x.id === selectedL1.value)
    .children.find((x) => x.id === selectedL2.value);
});

const selectedCompetency = ref(null);
const selectCompetency = async (id) => {
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
