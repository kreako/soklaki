<template>
  <div class="my-4 px-2">
    <div>
      <IconHome class="h-4" />
    </div>
    <div>
      <MillerColumn />
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
