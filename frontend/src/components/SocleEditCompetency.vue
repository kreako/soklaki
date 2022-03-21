<template>
  <div>
    <div class="flex flex-row items-center space-x-2">
      <div>
        {{ competencyById(competency.id).full_rank }}
        {{ competencyById(competency.id).text }}
      </div>
      <button @click="goInEditCompetency" class="hover:text-teal-500 text-gray-700">
        <IconPencil class="h-3" />
      </button>
    </div>
    <div class="flex flex-row items-center space-x-2 mt-8">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">Tags</div>
      <button @click="editSubjects = true" class="hover:text-teal-500 text-gray-700">
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
        <div class="flex flex-col md:flex-row md:items-center md:space-x-2 mt-2">
          <button
            @click="newSubject"
            class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            <div class="flex flex-row items-center space-x-2">
              <div>Nouveau tag</div>
              <IconPlus class="h-3 text-gray-700" />
            </div>
          </button>
          <button
            @click="deleteSubject"
            class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            <div class="flex flex-row items-center space-x-2">
              <div>Supprimer un tag</div>
              <IconX class="h-3 text-gray-700" />
            </div>
          </button>
          <button
            @click="editSubjects = false"
            class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
          >
            C'est bon, je les ai tous
          </button>
        </div>
      </div>
    </div>
    <div class="flex flex-row items-center space-x-2 mt-8">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">Exemples</div>
      <button @click="goInEditTemplates()" class="hover:text-teal-500 text-gray-700">
        <IconPencil class="h-3" />
      </button>
    </div>
    <hr class="bg-gray-700" />
    <div v-if="editTemplates">
      <div v-for="t in editedTemplates" class="mb-2">
        <textarea
          :value="t.text"
          @input="setTemplateText(t.id, $event.target.value)"
          class="mt-2 input w-full"
          rows="5"
        ></textarea>
      </div>
      <div v-for="(t, index) in addedTemplates" class="mb-2">
        <textarea
          :value="t"
          @input="setAddedTemplateText(index, $event.target.value)"
          class="mt-2 input w-full"
          rows="5"
        ></textarea>
      </div>
      <div class="flex flex-col md:flex-row md:items-center md:space-x-2 mt-2">
        <button
          @click="addTemplate"
          class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
        >
          Ajouter un exemple
        </button>
        <button
          @click="saveTemplatesEdit"
          class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
        >
          Sauvegarder
        </button>
        <button
          @click="editTemplates = false"
          class="mt-2 rounded-md px-3 border border-teal-700 hover:border-teal-300"
        >
          Tout annuler
        </button>
      </div>
    </div>
    <div v-else>
      <div v-for="t in competency.templates" class="flex flex-row items-center space-x-2 mb-2">
        <div>
          {{ templateById(t.id).text }}
        </div>
        <button @click="deleteTemplate(t.id)" class="text-gray-300 hover:text-gray-600">
          <IconTrash class="h-4" />
        </button>
      </div>
    </div>
    <div class="flex flex-row items-center space-x-4 mt-8">
      <button
        @click="goToPrevCompetency()"
        class="border border-gray-300 rounded-md shadow-md hover:text-teal-500 hover:border-teal-500"
      >
        <IconChevronLeft class="h-8" />
      </button>
      <button
        @click="goToNextCompetency()"
        class="border border-gray-300 rounded-md shadow-md hover:text-teal-500 hover:border-teal-500"
      >
        <IconChevronRight class="h-8" />
      </button>
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
            <button v-else class="group flex flex-row" @click="toggleDeleteSubject(subject.id)">
              <IconX class="w-4 text-gray-300 group-hover:text-teal-500 mr-2" />
              <div class="group-hover:text-teal-500">{{ subject.title }}</div>
            </button>
          </div>
        </div>
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Suppression d'un exemple"
      :show="showDeleteTemplateModal"
      @confirm="confirmDeleteTemplate"
      @cancel="cancelDeleteTemplate"
    >
      <div>
        <div>Êtes-vous sûr de vouloir supprimer cet exemple ?</div>
        <div class="mt-2 font-mono">
          {{ templateById(selectedForDeletionTemplate).text }}
        </div>
      </div>
    </ModalConfirmCancel>
    <ModalConfirmCancel
      title="Modification du titre de la compétence"
      :show="showCompetencyModal"
      @confirm="confirmCompetency"
      @cancel="cancelCompetency"
    >
      <div>
        <input type="text" v-model="competencyTitle" class="input w-full" />
      </div>
    </ModalConfirmCancel>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { computed, ref, defineProps, defineEmit } from "vue";
import SubjectSelector from "../components/SubjectSelector.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconXCircle from "../icons/IconXCircle.vue";
import IconTrash from "../icons/IconTrash.vue";
import IconPlus from "../icons/IconPlus.vue";
import IconX from "../icons/IconX.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";

const props = defineProps({
  competency: Object,
});

const emit = defineEmit(["goToNextCompetency", "goToPrevCompetency"]);

const goToNextCompetency = () => {
  emit("goToNextCompetency");
};

const goToPrevCompetency = () => {
  emit("goToPrevCompetency");
};

const store = useStore();

const competencyById = computed(() => store.getters.competencyById);
const subjectById = computed(() => store.getters.subjectById);
const templateById = computed(() => store.getters.templateById);

const subjects = computed(() => store.getters.subjects);

const nonSelectedSubjects = computed(() => {
  const selected = props.competency.subjects.map((x) => x.subject_id);
  const nonSelected = store.getters.subjects.filter((x) => !selected.includes(x.id));
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
const editedTemplates = ref([]);
const goInEditTemplates = () => {
  editedTemplates.value = [];
  for (const t of props.competency.templates) {
    editedTemplates.value.push({
      id: t.id,
      text: store.getters.templateById(t.id).text,
    });
  }
  editTemplates.value = true;
};
const setTemplateText = (id, text) => {
  for (const t of editedTemplates.value) {
    if (t.id === id) {
      t.text = text;
    }
  }
};
const saveTemplatesEdit = async () => {
  for (const t of editedTemplates.value) {
    await store.dispatch("updateSocleCompetencyTemplateText", {
      id: t.id,
      text: t.text.trim(),
    });
  }
  for (const text of addedTemplates.value) {
    const t = text.trim();
    if (t !== "") {
      await store.dispatch("insertSocleCompetencyTemplate", {
        competencyId: props.competency.id,
        text: t,
      });
    }
  }
  editTemplates.value = false;
};

const showDeleteTemplateModal = ref(false);
const selectedForDeletionTemplate = ref(null);
const deleteTemplate = (id) => {
  selectedForDeletionTemplate.value = id;
  showDeleteTemplateModal.value = true;
};
const confirmDeleteTemplate = async () => {
  await store.dispatch("updateSocleCompetencyTemplateActive", {
    id: selectedForDeletionTemplate.value,
    active: false,
  });
  showDeleteTemplateModal.value = false;
};
const cancelDeleteTemplate = () => {
  showDeleteTemplateModal.value = false;
  selectedForDeletionTemplate.value = null;
};

const addedTemplates = ref([]);
const addTemplate = () => {
  addedTemplates.value.push("");
};
const setAddedTemplateText = (index, text) => {
  addedTemplates.value[index] = text;
};

const showCompetencyModal = ref(false);
const competencyTitle = ref("");
const goInEditCompetency = () => {
  competencyTitle.value = store.getters.competencyById(props.competency.id).text;
  showCompetencyModal.value = true;
};
const confirmCompetency = async () => {
  await store.dispatch("updateSocleCompetencyText", {
    id: props.competency.id,
    text: competencyTitle.value,
  });
  showCompetencyModal.value = false;
};
const cancelCompetency = async () => {
  showCompetencyModal.value = false;
};
</script>
