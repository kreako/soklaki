<template>
  <div v-for="container1 in filteredSocle">
    <div class="flex flex-row space-x-2">
      <RankText
        kind="container1"
        :socle="socle"
        :objectId="container1.id"
        @edit="editContainer(container1.id)"
      />
    </div>
    <div class="pl-2" v-for="container2 in container1.children">
      <!-- Container level 2 -->
      <div class="flex flex-row space-x-2">
        <RankText
          kind="container2"
          :socle="socle"
          :objectId="container2.id"
          @edit="editContainer(container2.id)"
        />
      </div>
      <!-- competencies attached to container level 2 -->
      <div v-for="competency in container2.competencies" class="pl-2">
        <Disclosure>
          <DisclosureButton class="">
            <RankText
              kind="competency"
              :socle="socle"
              :objectId="competency.id"
              @edit="editCompetency(competency.id)"
            />
          </DisclosureButton>
          <DisclosurePanel class="pl-2">
            <HashSubjects
              :subjects="competency.subjects"
              @edit="editSubjects(competency.id)"
            />
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
            @edit="editCompetency(competency.id)"
          />
        </DisclosureButton>
        <DisclosurePanel class="pl-2">
          <HashSubjects
            :subjects="competency.subjects"
            @edit="editSubjects(competency.id)"
          />
          <CompetencyTemplates :templates="competency.templates" />
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
  <Modal
    :title="competencyModalTitle"
    :show="showEditCompetency"
    @close="closeCompetencyModal"
  >
    <div>TODO Content</div>
  </Modal>
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

const editContainer = (containerId) => {
  console.log("editContainer", containerId);
};

// Competency edition
const showEditCompetency = ref(false);
const competencyId = ref(null);
const competencyById = computed(() => store.getters.competencyById);
const competency = computed(() => competencyById.value(competencyId.value));
const competencyModalTitle = computed(() => {
  if (competencyId.value == null) {
    return "";
  }
  const fullRank = competency.value.full_rank;
  const text = competency.value.text;
  return `Modification de ${fullRank} ${text}`;
});
const editCompetency = (id) => {
  competencyId.value = id;
  showEditCompetency.value = true;
};
const closeCompetencyModal = () => {
  showEditCompetency.value = false;
};

const editSubjects = (competencyId) => {
  console.log("editSubjects", competencyId);
};

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
