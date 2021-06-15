<template>
  <div>
    <div>
      {{ competencyById(competency.id).full_rank }}
      {{ competencyById(competency.id).text }}
    </div>
    <div
      class="text-sm uppercase text-gray-700 tracking-wider font-semibold mt-4"
    >
      Tags
    </div>
    <hr class="bg-gray-700" />
    <div>
      <div v-for="s in competency.subjects">
        #{{ subjectById(s.subject_id).title }}
      </div>
    </div>
    <div
      class="text-sm uppercase text-gray-700 tracking-wider font-semibold mt-4"
    >
      Exemples
    </div>
    <hr class="bg-gray-700" />
    <div>
      <div v-for="t in competency.templates">
        {{ templateById(t.id).text }}
      </div>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { computed, ref, defineProps, defineEmit } from "vue";
import MillerColumn from "../components/MillerColumn.vue";

const props = defineProps({
  competency: Object,
});

const store = useStore();

const competencyById = computed(() => store.getters.competencyById);
const subjectById = computed(() => store.getters.subjectById);
const templateById = computed(() => store.getters.templateById);
</script>
