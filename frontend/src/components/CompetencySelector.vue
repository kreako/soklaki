<template>
  <div>
    <div class="flex flex-row">
      <!-- header : title, + filters -->
      <div class="text-gray-800 flex-grow">
        Compétences (cycle&nbsp;{{ cycleAsNb }})
      </div>
      <div class="text-gray-800 flex flex-row items-center space-x-1">
        <select
          v-model="selectedSubject"
          class="appearance-none block bg-transparent py-1 text-gray-500 font-medium text-sm focus:outline-none focus:text-gray-900 transition-colors duration-200"
        >
          <option :value="-1">Par matières</option>
          <option v-for="subject in socle.subjects" :value="subject.id">
            {{ subject.title }}
          </option>
        </select>
      </div>
    </div>
    <div class="mt-2 text-sm space-x-1 space-y-1"></div>
    <input
      v-model="socleFilter"
      class="input w-full mt-2"
      type="text"
      placeholder="Filtre..."
    />
    <div class="mt-2">
      <div v-if="filtered">
        <div v-for="domain in filteredSocle">
          <div class="flex flex-row space-x-2">
            <div class="uppercase text-xs tracking-wide text-gray-700">
              {{ socle.domains[domain.id].rank }}.
              {{ socle.domains[domain.id].title }}
            </div>
            <button v-if="domain.id === selectedDomain" @click="deselectDomain">
              <IconBackSpace class="w-4 text-gray-500" />
            </button>
          </div>
          <div class="pl-2" v-for="component in domain.components">
            <div class="flex flex-row space-x-2">
              <div class="text-xs text-gray-700">
                {{ socle.components[component.id].rank }}.
                {{ socle.components[component.id].title }}
              </div>
              <button
                v-if="component.id === selectedComponent"
                @click="deselectComponent"
              >
                <IconBackSpace class="w-4 text-gray-500" />
              </button>
            </div>
            <div v-for="competency in component.competencies">
              <button
                @click="selectCompetency(competency.id)"
                class="pl-2 text-left border border-white hover:border-teal-500"
              >
                {{ socle.competencies[competency.id].rank }}.
                {{ socle.competencies[competency.id].text }}
              </button>
            </div>
          </div>
        </div>
        <div v-if="filteredSocle.length === 0">
          <!-- Nothing to display ? Give me a smiley -->
          <MascotteTip>
            <template v-slot:title>Rien à afficher ! 🙀</template>
            <template v-slot:default>
              Oups, les filtres sont peut-être trop sévères, je ne trouve rien à
              afficher. Est-ce que vous voulez les
              <a
                @click="resetAllFilters"
                class="text-blue-600 underline cursor-pointer"
                >remettre à zéro ?</a
              >
            </template>
          </MascotteTip>
        </div>
      </div>
      <div v-else>
        <div v-if="selectedDomain == null">
          <div v-for="domain in socle[cycle]">
            <button
              @click="selectDomain(domain.id)"
              class="uppercase tracking-wide text-gray-700 text-left border border-white hover:border-teal-500"
            >
              {{ socle.domains[domain.id].rank }}.
              {{ socle.domains[domain.id].title }}
            </button>
          </div>
        </div>
        <div v-else>
          <!-- Here I need to select a component -->
          <div class="flex flex-row space-x-2">
            <div class="uppercase text-xs tracking-wide text-gray-700">
              {{ socle.domains[selectedDomain].rank }}.
              {{ socle.domains[selectedDomain].title }}
            </div>
            <button @click="deselectDomain">
              <IconBackSpace class="w-4 text-gray-500" />
            </button>
          </div>
          <div
            v-for="component in componentsFromDomain(selectedDomain)"
            class="pl-2"
          >
            <button
              @click="selectComponent(component.id)"
              class="text-gray-700 text-left border border-white hover:border-teal-500"
            >
              {{ socle.components[component.id].rank }}.
              {{ socle.components[component.id].title }}
            </button>
          </div>
        </div>
      </div>
      <!--
            -->
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref, computed } from "vue";
import { cycleNb } from "../utils/cycle";
import IconChevronDown from "../icons/IconChevronDown.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconBackSpace from "../icons/IconBackSpace.vue";
import MascotteTip from "../components/MascotteTip.vue";

const props = defineProps({
  socle: Object,
  cycle: String,
});

const cycleAsNb = computed(() => cycleNb(props.cycle));

const selectedSubject = ref(-1);
const isInSubjects = (competency, subjectId) => {
  for (let i = 0; i < competency.subjects.length; i++) {
    if (competency.subjects[i].subject.id === subjectId) {
      return true;
    }
  }
  return false;
};

const selectedDomain = ref(null);
const selectDomain = (id) => {
  selectedDomain.value = id;
};
const deselectDomain = () => {
  selectedDomain.value = null;
  selectedComponent.value = null;
};
const componentsFromDomain = (domainId) => {
  for (const domain of props.socle[props.cycle]) {
    if (domain.id === domainId) {
      return domain.components;
    }
  }
  // TODO error ?
  return [];
};

const selectedComponent = ref(null);
const selectComponent = (id) => {
  selectedComponent.value = id;
};
const deselectComponent = () => {
  selectedComponent.value = null;
};

const emit = defineEmit(["selected"]);

const selectCompetency = (competencyId) => {
  emit("selected", competencyId);
};

const socleFilter = ref("");

const searchObjectIdInArray = (array, o) => {
  for (const e of array) {
    if (e.id === o.id) {
      return e;
    }
  }
  array.push(o);
  return array[array.length - 1];
};

const cheatcodeRe = /(\d)[\. ](\d)[\. ](\d{1,2})/;

const filteredSocle = computed(() => {
  const cheatSocleAccess = socleFilter.value.match(cheatcodeRe);
  if (cheatSocleAccess != null) {
    // OMG an advanced user typing the direct access to the competency
    const domainRank = cheatSocleAccess[1];
    const componentRank = cheatSocleAccess[2];
    const competencyRank = cheatSocleAccess[3];
    // Let's find it
    for (const domain of props.socle[props.cycle]) {
      if (props.socle.domains[domain.id].rank != domainRank) {
        continue;
      }
      for (const component of domain.components) {
        if (props.socle.components[component.id].rank != componentRank) {
          continue;
        }
        for (const competency of component.competencies) {
          if (props.socle.competencies[competency.id].rank == competencyRank) {
            return [
              {
                id: domain.id,
                components: [
                  {
                    id: component.id,
                    competencies: [competency],
                  },
                ],
              },
            ];
          }
        }
      }
    }
  }
  // Let's build a socle tree with competencies matching the filter
  // of this non advanced user, expecting text filter
  let r = new RegExp(socleFilter.value, "i");
  const socle = [];
  for (const domain of props.socle[props.cycle]) {
    if (selectedDomain.value != null && domain.id !== selectedDomain.value) {
      // Ignore non selected domain
      continue;
    }
    for (const component of domain.components) {
      if (
        selectedComponent.value != null &&
        component.id !== selectedComponent.value
      ) {
        // Ignore non selected component
        continue;
      }
      for (const competency of component.competencies) {
        if (selectedSubject.value !== -1) {
          if (!isInSubjects(competency, selectedSubject.value)) {
            // Do not select competencies not in selected subject
            continue;
          }
        }
        if (r.test(props.socle.competencies[competency.id].text)) {
          // This is a match so add this competency with the corresponding domain/component
          const d = searchObjectIdInArray(socle, {
            id: domain.id,
            components: [],
          });
          const c = searchObjectIdInArray(d.components, {
            id: component.id,
            competencies: [],
          });
          c.competencies.push(competency);
        }
      }
    }
  }
  return socle;
});

const filtered = computed(
  () =>
    selectedSubject.value !== -1 ||
    socleFilter.value !== "" ||
    (selectedDomain.value != null && selectedComponent.value != null)
);

const resetAllFilters = () => {
  selectedSubject.value = -1;
  socleFilter.value = "";
  selectedDomain.value = null;
  selectedComponent.value = null;
};
</script>
