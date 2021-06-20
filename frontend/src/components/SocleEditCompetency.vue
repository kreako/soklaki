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
      <div v-if="editSubjects" class="mt-2">
        <SubjectSelector @select="addSubject" :subjects="nonSelectedSubjects" />
        <div
          class="flex flex-col md:flex-row md:items-center md:space-x-2 mt-2"
        >
          <button
            @click="newSubject"
            class="
              mt-2
              rounded-md
              px-3
              border border-teal-700
              hover:border-teal-300
            "
          >
            <div class="flex flex-row items-center space-x-2">
              <div>Nouveau tag</div>
              <IconPlus class="h-3 text-gray-700" />
            </div>
          </button>
          <button
            @click="deleteSubject"
            class="
              mt-2
              rounded-md
              px-3
              border border-teal-700
              hover:border-teal-300
            "
          >
            <div class="flex flex-row items-center space-x-2">
              <div>Supprimer un tag</div>
              <IconX class="h-3 text-gray-700" />
            </div>
          </button>
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
    </div>
    <div class="flex flex-row items-center space-x-2 mt-8">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">
        Exemples
      </div>
      <button
        @click="editTemplates = true"
        class="hover:text-teal-500 text-gray-700"
      >
        <IconPencil class="h-3" />
      </button>
    </div>
    <hr class="bg-gray-700" />
    <div v-if="editTemplates">
      <div v-for="t in competency.templates" class="mb-2">
        <textarea
          :value="templateById(t.id).text"
          @input="setTemplateText(t.id, $event.target.value)"
          class="mt-2 input w-full"
          rows="5"
        >
        </textarea>
      </div>
      <div class="flex flex-col md:flex-row md:items-center md:space-x-2 mt-2">
        <button
          @click="saveTemplatesEdit"
          class="
            mt-2
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          Sauvegarder
        </button>
        <button
          @click="editTemplates = false"
          class="
            mt-2
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          Tout annuler
        </button>
      </div>
    </div>
    <div v-else>
      <div v-for="t in competency.templates" class="mb-2">
        {{ templateById(t.id).text }}
      </div>
    </div>
    <ModalConfirmCancel
      title="Nouveau tag"
      :show="showNewSubjectModal"
      @confirm="confirmNewSubject"
      @cancel="cancelNewSubject"
    >
      <div>
        <div>Création d'un nouveau tag</div>
        <input
          type="text"
          v-model="tagValue"
          @keyup.enter="confirmNewSubject"
          class="input w-full input"
        />
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Suppression d'un tag"
      :show="showDeleteSubjectModal"
      @confirm="confirmDeleteSubject"
      @cancel="cancelDeleteSubject"
    >
      <div>
        <div>Suppression d'un tag</div>
        <div>
          <div
            v-for="subject in subjects"
            :key="subject.id"
            class="px-2 flex flex-row items-center gap-2"
          >
            <button
              v-if="selectedDeleteSubject === subject.id"
              class="flex flex-row"
              @click="toggleDeleteSubject(subject.id)"
            >
              <IconX class="w-4 text-teal-500 mr-2" />
              <div class="text-teal-500">{{ subject.title }}</div>
            </button>
            <button
              v-else
              class="group flex flex-row"
              @click="toggleDeleteSubject(subject.id)"
            >
              <IconX class="w-4 text-gray-300 group-hover:text-teal-500 mr-2" />
              <div class="group-hover:text-teal-500">{{ subject.title }}</div>
            </button>
          </div>
        </div>
      </div>
    </ModalConfirmCancel>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { computed, ref, defineProps, defineEmit } from "vue";
import MillerColumn from "../components/MillerColumn.vue";
import SubjectSelector from "../components/SubjectSelector.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import IconPlus from "../icons/IconPlus.vue";
import IconX from "../icons/IconX.vue";
import IconLogout from "../icons/IconLogout.vue";

const props = defineProps({
  competency: Object,
});

const store = useStore();

const competencyById = computed(() => store.getters.competencyById);
const subjectById = computed(() => store.getters.subjectById);
const templateById = computed(() => store.getters.templateById);

const subjects = computed(() => store.getters.subjects);

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

const showNewSubjectModal = ref(false);
const tagValue = ref("");
const newSubject = () => {
  tagValue.value = "";
  showNewSubjectModal.value = true;
};
const confirmNewSubject = async () => {
  await store.dispatch("insertSocleSubject", { title: tagValue.value });
  showNewSubjectModal.value = false;
};
const cancelNewSubject = () => {
  showNewSubjectModal.value = false;
};

const showDeleteSubjectModal = ref(false);
const deleteSubject = () => {
  showDeleteSubjectModal.value = true;
};
const confirmDeleteSubject = async () => {
  await store.dispatch("updateSocleSubjectActive", {
    id: selectedDeleteSubject.value,
    active: false,
  });
  showDeleteSubjectModal.value = false;
};
const cancelDeleteSubject = () => {
  showDeleteSubjectModal.value = false;
};
const selectedDeleteSubject = ref(null);
const toggleDeleteSubject = (subjectId) => {
  if (subjectId === selectedDeleteSubject.value) {
    selectedDeleteSubject.value = null;
  } else {
    selectedDeleteSubject.value = subjectId;
  }
};

const editTemplates = ref(false);
const templatesText = ref({});
const setTemplateText = (id, text) => {
  templatesText.value[id] = text;
};
const saveTemplatesEdit = async () => {
  for (const [id, text] of Object.entries(templatesText.value)) {
    await store.dispatch("updateSocleCompetencyTemplateText", { id, text });
  }
  editTemplates.value = false;
};
</script>
