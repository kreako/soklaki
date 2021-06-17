<template>
  <div>
    <div>
      {{ competencyById(competency.id).full_rank }}
      {{ competencyById(competency.id).text }}
    </div>
    <div class="flex flex-row items-center space-x-2 mt-8">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">
        Tags
      </div>
      <button
        @click="editSubjects = true"
        class="hover:text-teal-500 text-gray-700"
      >
        <IconPencil class="h-3" />
      </button>
    </div>
    <hr class="bg-gray-700" />
    <div>
      <div v-for="s in competency.subjects">
        <div class="flex flex-row items-center space-x-2">
          <div>#{{ subjectById(s.subject_id).title }}</div>
          <button
            v-if="editSubjects"
            @click="removeSubject(s.subject_id, competency.id)"
            class="text-gray-300 hover:text-gray-600"
          >
            <IconXCircle class="h-4" />
          </button>
        </div>
      </div>
      <div v-if="editSubjects">
        <SubjectSelector @select="addSubject" :subjects="nonSelectedSubjects" />
        <button
          @click="editSubjects = false"
          class="
            mt-2
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          C'est bon, je les ai tous
        </button>
      </div>
    </div>
    <div
      class="text-sm uppercase text-gray-700 tracking-wider font-semibold mt-8"
    >
      Exemples
    </div>
    <hr class="bg-gray-700" />
    <div>
      <div v-for="t in competency.templates" class="mb-2">
        {{ templateById(t.id).text }}
      </div>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { computed, ref, defineProps, defineEmit } from "vue";
import MillerColumn from "../components/MillerColumn.vue";
import SubjectSelector from "../components/SubjectSelector.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconXCircle from "../icons/IconXCircle.vue";

const props = defineProps({
  competency: Object,
});

const store = useStore();

const competencyById = computed(() => store.getters.competencyById);
const subjectById = computed(() => store.getters.subjectById);
const templateById = computed(() => store.getters.templateById);

const nonSelectedSubjects = computed(() => {
  const selected = props.competency.subjects.map((x) => x.subject_id);
  const nonSelected = store.getters.subjects.filter(
    (x) => !selected.includes(x.id)
  );
  return nonSelected;
});

const editSubjects = ref(false);
const addSubject = async (id, subjectId) => {
  await store.dispatch("insertSocleCompetencySubject", {
    competencyId: props.competency.id,
    subjectId: id,
  });
};
const removeSubject = async (subjectId, competencyId) => {
  await store.dispatch("deleteSocleCompetencySubject", {
    subjectId,
    competencyId,
  });
};
</script>
