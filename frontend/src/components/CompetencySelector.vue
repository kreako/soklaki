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
        <!-- At least one filter is selected so display the full thing -->
        <div v-for="container1 in filteredSocle">
          <div class="flex flex-row space-x-2">
            <div class="uppercase text-xs tracking-wide text-gray-700">
              {{ socle.containers[container1.id].rank }}.
              {{ socle.containers[container1.id].text }}
            </div>
            <button
              v-if="container1.id === selectedContainer1"
              @click="deselectContainer1"
            >
              <IconBackSpace class="w-4 text-gray-500" />
            </button>
          </div>
          <div class="pl-2" v-for="container2 in container1.children">
            <!-- Container level 2 -->
            <div class="flex flex-row space-x-2">
              <div class="text-xs text-gray-700">
                {{ socle.containers[container2.id].rank }}.
                {{ socle.containers[container2.id].text }}
              </div>
              <button
                v-if="container2.id === selectedContainer2"
                @click="deselectContainer2"
              >
                <IconBackSpace class="w-4 text-gray-500" />
              </button>
            </div>
            <!-- competencies attached to container level 2 -->
            <div v-for="competency in container2.competencies">
              <button
                @click="selectCompetency(competency.id)"
                class="pl-2 text-left border border-white hover:border-teal-500"
              >
                {{ socle.competencies[competency.id].rank }}.
                {{ socle.competencies[competency.id].text }}
              </button>
            </div>
          </div>
          <div v-for="competency in container1.competencies">
            <!-- competencies attached to container level 1 -->
            <button
              @click="selectCompetency(competency.id)"
              class="pl-2 text-left border border-white hover:border-teal-500"
            >
              {{ socle.competencies[competency.id].rank }}.
              {{ socle.competencies[competency.id].text }}
            </button>
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
        <!-- Nothing is filtered -->
        <div v-if="selectedContainer1 == null">
          <!-- no container level 1 selected : so display level 1 container -->
          <div v-for="container1 in socle[cycle]">
            <button
              @click="selectContainer1(container1.id)"
              class="uppercase tracking-wide text-gray-700 text-left border border-white hover:border-teal-500"
            >
              {{ socle.containers[container1.id].rank }}.
              {{ socle.containers[container1.id].text }}
            </button>
          </div>
        </div>
        <div v-else>
          <!-- container level 1 is selected so Here I need to select a container2
            Note that I don't display competencies because if container 1 is selected
            And no container level 2 exists, it is considered as filtered -->
          <div class="flex flex-row space-x-2">
            <div class="uppercase text-xs tracking-wide text-gray-700">
              {{ socle.containers[selectedContainer1].rank }}.
              {{ socle.containers[selectedContainer1].text }}
            </div>
            <button @click="deselectContainer1">
              <IconBackSpace class="w-4 text-gray-500" />
            </button>
          </div>
          <div
            v-for="container2 in containers2FromContainer1(selectedContainer1)"
            class="pl-2"
          >
            <button
              @click="selectContainer2(container2.id)"
              class="text-gray-700 text-left border border-white hover:border-teal-500"
            >
              {{ socle.containers[container2.id].rank }}.
              {{ socle.containers[container2.id].text }}
            </button>
          </div>
        </div>
      </div>
      <div class="mt-4 text-right pr-2">
        <button @click="$emit('cancel')" class="button-minor-action text-sm">
          Annuler
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref, computed } from "vue";
import { cycleNb } from "../utils/cycle";
import {
  filterSocleBySubject,
  filterSocleBy2Ranks,
  filterSocleBy3Ranks,
  filterSocleByRegex,
  filterSocleByContainerId,
  filterSocleByContainerIds,
} from "../utils/socle";
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

const selectedContainer1 = ref(null);
const selectContainer1 = (id) => {
  selectedContainer1.value = id;
};
const deselectContainer1 = () => {
  selectedContainer1.value = null;
  selectedContainer2.value = null;
};
const containers2FromContainer1 = (container1Id) => {
  for (const container1 of props.socle[props.cycle]) {
    if (container1.id === container1Id) {
      return container1.children;
    }
  }
  // TODO error ?
  return [];
};

const selectedContainer2 = ref(null);
const selectContainer2 = (id) => {
  selectedContainer2.value = id;
};
const deselectContainer2 = () => {
  selectedContainer2.value = null;
};

const emit = defineEmit(["selected", "cancel"]);

const selectCompetency = (competencyId) => {
  emit("selected", competencyId);
};

const socleFilter = ref("");

const cheatcodeRe = /(\d{1,2})[\. ](\d{1,2})[\. ]?(\d{1,2})?/;

const filteredSocle = computed(() => {
  const socle = props.socle[props.cycle];
  const cheatSocleAccess = socleFilter.value.match(cheatcodeRe);
  if (cheatSocleAccess != null) {
    // OMG an advanced user typing the direct access to the competency
    if (cheatSocleAccess[3] == null) {
      const container1Rank = cheatSocleAccess[1];
      const competencyRank = cheatSocleAccess[2];
      const f = filterSocleBy2Ranks(
        props,
        socle,
        container1Rank,
        competencyRank
      );
      if (f.length > 0) {
        return f;
      }
    } else {
      const container1Rank = cheatSocleAccess[1];
      const container2Rank = cheatSocleAccess[2];
      const competencyRank = cheatSocleAccess[3];
      const f = filterSocleBy3Ranks(
        props,
        socle,
        container1Rank,
        container2Rank,
        competencyRank
      );
      if (f.length > 0) {
        return f;
      }
    }
  }
  // Let's build a socle tree with competencies matching the filter
  // of this non advanced user, expecting subject or text filter
  let f = socle;
  if (selectedContainer1.value != null) {
    if (selectedContainer2.value != null) {
      f = filterSocleByContainerIds(
        f,
        selectedContainer1.value,
        selectedContainer2.value
      );
    } else {
      f = filterSocleByContainerId(f, selectedContainer1.value);
    }
  }
  if (selectedSubject.value !== -1) {
    f = filterSocleBySubject(f, selectedSubject.value);
  }
  let r = new RegExp(socleFilter.value, "i");
  return filterSocleByRegex(props, f, r);
});

const filtered = computed(() => {
  if (selectedSubject.value !== -1) {
    // A subject have been chosen
    return true;
  }
  if (socleFilter.value !== "") {
    // something has been entered in filter box
    return true;
  }
  if (selectedContainer1.value != null) {
    // level 1 has been selected
    if (selectedContainer2.value != null) {
      // level 2 selected too
      return true;
    }
    for (const container1 of props.socle[props.cycle]) {
      if (container1.id === selectedContainer1.value) {
        if (container1.children.length === 0) {
          // level 1 has no children so considered filtered
          return true;
        } else {
          // has container children
          return false;
        }
      }
    }
  }
  // everything else is not filtered
  return false;
});

const resetAllFilters = () => {
  selectedSubject.value = -1;
  socleFilter.value = "";
  selectedContainer1.value = null;
  selectedContainer2.value = null;
};
</script>
