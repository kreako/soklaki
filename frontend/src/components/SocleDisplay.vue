<template>
  <div v-for="container1 in filteredSocle">
    <div class="flex flex-row space-x-2">
      <RankText kind="container1" :socle="socle" :objectId="container1.id" />
    </div>
    <div class="pl-2" v-for="container2 in container1.children">
      <!-- Container level 2 -->
      <div class="flex flex-row space-x-2">
        <RankText kind="container2" :socle="socle" :objectId="container2.id" />
      </div>
      <!-- competencies attached to container level 2 -->
      <div v-for="competency in container2.competencies" class="pl-2">
        <Disclosure>
          <DisclosureButton class="">
            <RankText
              kind="competency"
              :socle="socle"
              :objectId="competency.id"
            />
          </DisclosureButton>
          <DisclosurePanel class="pl-2">
            <HashSubjects :subjects="competency.subjects" />
            <CompetencyTemplates :templates="competency.templates" />
          </DisclosurePanel>
        </Disclosure>
      </div>
    </div>
    <div v-for="competency in container1.competencies" class="pl-2">
      <!-- competencies attached to container level 1 -->
      <Disclosure>
        <DisclosureButton class="">
          <RankText
            kind="competency"
            :socle="socle"
            :objectId="competency.id"
          />
        </DisclosureButton>
        <DisclosurePanel class="pl-2">
          <HashSubjects :subjects="competency.subjects" />
          <CompetencyTemplates :templates="competency.templates" />
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
</template>
<script setup>
import { defineProps, computed, ref } from "vue";
import { useStore } from "vuex";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { filterSocleBySubject } from "../utils/socle";
import RankText from "./RankText.vue";
import HashSubjects from "./HashSubjects.vue";
import CompetencyTemplates from "./CompetencyTemplates.vue";
import Modal from "./Modal.vue";

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
</script>
