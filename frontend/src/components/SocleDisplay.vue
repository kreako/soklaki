<template>
  <div v-for="container1 in filteredSocle">
    <div class="flex flex-row space-x-2">
      <div class="uppercase tracking-wide text-gray-700">
        {{ socle.containers[container1.id].rank }}.
        {{ socle.containers[container1.id].text }}
      </div>
    </div>
    <div class="pl-2" v-for="container2 in container1.children">
      <!-- Container level 2 -->
      <div class="flex flex-row space-x-2">
        <div class="text-gray-700">
          {{ socle.containers[container2.id].rank }}.
          {{ socle.containers[container2.id].text }}
        </div>
      </div>
      <!-- competencies attached to container level 2 -->
      <div v-for="competency in container2.competencies">
        <div class="pl-2 text-left border border-white hover:border-teal-500">
          {{ socle.competencies[competency.id].rank }}.
          {{ socle.competencies[competency.id].text }}
        </div>
        <div class="pl-2 flex flex-row space-x-2">
          <div
            v-for="subject in competency.subjects"
            class="text-sm text-gray-700"
          >
            #{{ subjectById(subject.subject_id).title }}
          </div>
        </div>
      </div>
    </div>
    <div v-for="competency in container1.competencies">
      <!-- competencies attached to container level 1 -->
      <div class="pl-2 text-left border border-white hover:border-teal-500">
        {{ socle.competencies[competency.id].rank }}.
        {{ socle.competencies[competency.id].text }}
      </div>
      <div class="pl-2 flex flex-row space-x-2">
        <div
          v-for="subject in competency.subjects"
          class="text-sm text-gray-700"
        >
          #{{ subjectById(subject.subject_id).title }}
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { defineProps, computed } from "vue";
import { useStore } from "vuex";
import { filterSocleBySubject } from "../utils/socle";

const store = useStore();

const props = defineProps({
  socle: Object,
  cycle: String,
  subjectFilter: String,
});

const subjectById = computed(() => store.getters.subjectById);

const filteredSocle = computed(() => {
  const socle = props.socle[props.cycle];
  if (props.subjectFilter === "all") {
    return socle;
  } else {
    const subjectId = Number(props.subjectFilter);
    return filterSocleBySubject(socle, subjectId);
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
