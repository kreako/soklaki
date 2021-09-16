<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Les informations</div>
      <div class="mt-8 grid grid-cols-1 md:grid-cols-2">
        <InputTextWithLabel
          label="Prénom"
          :value="student.firstname"
          @save="saveFirstname"
        />
        <InputTextWithLabel
          label="Nom"
          :value="student.lastname"
          @save="saveLastname"
        />
        <InputDateWithLabel
          label="Date d'anniversaire"
          :value="student.birthdate"
          @save="saveBirthdate"
        />
        <div></div>
        <InputDateWithLabel
          label="Date d'entrée à l'école"
          :value="student.school_entry"
          @save="saveSchoolEntry"
        />
        <div>
          <div v-if="student.school_exit != null || addSchoolExit == true">
            <InputDateWithLabel
              label="Date de sortie de l'école"
              :value="student.school_exit"
              :edit="addSchoolExit"
              :nullable="true"
              @save="saveSchoolExit"
              @cancel="addSchoolExit = false"
            />
          </div>
          <div v-else>
            <div class="form-sub-label">L'élève est toujours à l'école</div>
            <button
              @click="addSchoolExit = true"
              class="button-minor-action text-xs"
            >
              Ajouter une date de sortie
            </button>
          </div>
        </div>
      </div>
      <Disclosure>
        <DisclosureButton class="mt-16">
          <div class="flex flex-row items-center space-x-2">
            <div class="form-label">Les statistiques</div>
            <IconQuestionMark class="w-6 h-6 text-gray-500" />
          </div>
        </DisclosureButton>
        <DisclosurePanel class="py-2">
          <MascotteTip class="my-2">
            <template v-slot:title>
              Les statistiques pour {{ student.firstname }}
              {{ student.lastname }} ! 🧐
            </template>
            <template v-slot:default>
              <div class="mt-4">
                4 gros blocs sombres qui indique :
                <ul class="list-disc list-inside">
                  <li>
                    Le pourcentage total de ce qu'il reste à faire pour
                    compléter les observations/évaluations
                  </li>
                  <li>
                    Y a t'il un commentaire général enregistré pour cette
                    période ?
                  </li>
                  <li>
                    Le pourcentage total de ce qu'il reste à faire pour
                    compléter toutes les observations (au moins 1 par
                    compétence)
                  </li>
                  <li>
                    Le pourcentage total de ce qu'il reste à faire pour
                    compléter toutes les évaluations (1 par compétence)
                  </li>
                </ul>
              </div>
              <div class="mt-8">
                Puis une grille avec :
                <ul class="list-disc list-inside">
                  <li>Le numéro de la compétence</li>
                  <li class="mt-2">
                    Le nombre d'observations enregistrées pour cet élève et
                    cette compétence (sur la gauche), avec :
                    <ul class="ml-2">
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-gray-500"></div>
                          <div>Aucune observation enregistrée</div>
                        </div>
                      </li>
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-green-500"></div>
                          <div>Au moins un observation enregistrée ! \o/</div>
                        </div>
                      </li>
                    </ul>
                  </li>
                  <li class="mt-2">
                    L'évaluation associée à cet élève pour cette compétence (sur
                    la droite), avec :
                    <ul class="ml-2">
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-gray-500"></div>
                          <div>Aucune évaluation enregistrée</div>
                        </div>
                      </li>
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-red-500"></div>
                          <div>Une évaluation "Maitrise insuffisante"</div>
                        </div>
                      </li>
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-yellow-500"></div>
                          <div>Une évaluation "Maitrise fragile"</div>
                        </div>
                      </li>
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-green-500"></div>
                          <div>Une évaluation "Maitrise satisfaisante"</div>
                        </div>
                      </li>
                      <li>
                        <div class="flex items-center space-x-2">
                          <div class="w-5 h-5 rounded-md bg-pink-500"></div>
                          <div>Une évaluation "Très bonne maitrise"</div>
                        </div>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
              <div class="mt-4">
                <div>
                  Chaque petit carré
                  <div
                    class="
                      inline-block
                      align-middle
                      w-5
                      h-5
                      rounded-md
                      border border-gray-500
                    "
                  ></div>
                  est cliquable et vous emmène là où vous pourrez observer ou
                  évaluer !
                </div>
                <div>
                  D'ailleurs, les numéros de chaque compétence sont cliquables
                  également !
                </div>
              </div>
              <div class="mt-4">
                Et maintenant, votre mission, si vous l'acceptez, mettre de la
                couleur sur cette page et sur celle de tous les autres élèves !
                🎨
              </div>
            </template>
          </MascotteTip>
        </DisclosurePanel>
      </Disclosure>
      <div class="mt-8 grid grid-cols-2 md:grid-cols-4">
        <StatBoxPercent label="Total" :value="summary.progress" />
        <StatBoxPercent
          label="Commentaire"
          :value="summary.comment ? 100 : 0"
        />
        <StatBoxPercent label="Observations" :value="summary.observations" />
        <StatBoxPercent label="Évaluations" :value="summary.evaluations" />
      </div>
      <div class="mt-8 grid grid-cols-2 md:grid-cols-4">
        <div v-for="stat in stats" class="flex items-center space-x-2">
          <div class="w-16">
            <button @click="selectCompetency(stat.competency.id)">
              {{ stat.competency.full_rank }}
            </button>
          </div>
          <StatObservationBox
            :link="`/new-observation-prefill/${route.params.id}/${stat.competency.id}`"
            :observations="stat.eval.observations"
          />
          <StatEvaluationBox
            :link="`/evaluation-single/${cycle}/${stat.competency.id}/${route.params.id}`"
            :status="stat.eval.evaluation"
          />
        </div>
      </div>
      <!-- Allow to "delete" it but behind a disclosure  -->
      <div class="mt-20">
        <Disclosure>
          <DisclosureButton class="">
            <div class="flex flex-row items-center space-x-3">
              <div class="form-label">Zone dangereuse</div>
            </div>
          </DisclosureButton>
          <DisclosurePanel>
            <div>
              <div>
                N'hésitez pas à bien réfléchir, une fois qu'il.elle est
                supprimé.e... Elle est supprimé.e !
              </div>
              <button @click="setActiveFalse" class="button-cancel-action">
                Supprimer cet élève 😱
              </button>
            </div>
          </DisclosurePanel>
        </Disclosure>
      </div>
      <div class="mt-16">
        <router-link
          to="/students"
          class="text-gray-700 text-xs hover:text-teal-500"
        >
          Retourner à la liste des élèves↵
        </router-link>
      </div>
    </Loading>
    <Modal
      :title="competencyModalTitle"
      :show="showCompetencyModal"
      @close="closeCompetencyModal"
    >
      <div>
        <div class="uppercase tracking-wide text-gray-700">
          {{ competencyFathers[0].rank }}.
          {{ competencyFathers[0].text }}
        </div>
        <div v-if="competencyFathers[1].rank != null" class="text-gray-700">
          {{ competencyFathers[1].rank }}.
          {{ competencyFathers[1].text }}
        </div>
        <div>
          {{ competencyById(selectedCompetency).rank }}.
          {{ competencyById(selectedCompetency).text }}
        </div>
        <div class="mt-2 pl-2">
          <HashSubjects
            :subjects="competencyById(selectedCompetency).subjects"
          />
        </div>
        <div class="mt-2 pl-2">
          <CompetencyTemplates
            :templates="competencyById(selectedCompetency).templates"
          />
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { useTitle } from "@vueuse/core";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { fathers } from "../utils/competency";
import IconCheck from "../icons/IconCheck.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import Modal from "../components/Modal.vue";
import Loading from "../components/Loading.vue";
import MascotteTip from "../components/MascotteTip.vue";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";
import InputDateWithLabel from "../components/InputDateWithLabel.vue";
import StatEvaluationBox from "../components/StatEvaluationBox.vue";
import StatObservationBox from "../components/StatObservationBox.vue";
import StatBoxPercent from "../components/StatBoxPercent.vue";
import HashSubjects from "../components/HashSubjects.vue";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";

useTitle("Élève - soklaki.fr");

const store = useStore();
const route = useRoute();
const router = useRouter();

const saveLastname = async (value) => {
  student.value.lastname = value;
  await store.dispatch("saveStudentLastname", {
    id: route.params.id,
    lastname: value,
  });
};
const saveFirstname = async (value) => {
  student.value.firstname = value;
  await store.dispatch("saveStudentFirstname", {
    id: route.params.id,
    firstname: value,
  });
};
const saveBirthdate = async (value) => {
  student.value.birthdate = value;
  await store.dispatch("saveStudentBirthdate", {
    id: route.params.id,
    birthdate: value,
  });
};
const saveSchoolEntry = async (value) => {
  student.value.school_entry = value;
  await store.dispatch("saveStudentSchoolEntry", {
    id: route.params.id,
    schoolEntry: value,
  });
};
const addSchoolExit = ref(false);
const saveSchoolExit = async (value) => {
  addSchoolExit.value = false;
  student.value.school_exit = value;
  await store.dispatch("saveStudentSchoolExit", {
    id: route.params.id,
    schoolExit: value,
  });
};
const setActiveFalse = async () => {
  await store.dispatch("saveStudentActive", {
    id: route.params.id,
    active: false,
  });
  router.push("/students");
};

const competencyById = computed(() => store.getters.competencyById);

const selectedCompetency = ref(null);

const showCompetencyModal = ref(false);
const selectCompetency = (id) => {
  selectedCompetency.value = id;
  showCompetencyModal.value = true;
};
const closeCompetencyModal = () => {
  showCompetencyModal.value = false;
};
const competencyModalTitle = computed(() => {
  if (selectedCompetency.value == null) {
    return null;
  }
  const competency = competencyById.value(selectedCompetency.value);
  return `Compétence - ${competency.full_rank}`;
});
const competencyFathers = computed(() =>
  fathers(store, selectedCompetency.value)
);

const loading = ref(true);
const student = ref(null);
const cycle = ref(null);
const summary = ref(null);
const stats = ref(null);

const loadStudent = async () => {
  loading.value = true;
  let id = Number(route.params.id);
  if (!id) {
    // id is not a number :(
    return;
  }

  let data = await store.dispatch("student", id);
  student.value = data.student;
  cycle.value = data.cycle;
  summary.value = data.summary;
  stats.value = data.eval;
  useTitle(
    `Élève ${data.student.firstname} ${data.student.lastname} - soklaki.fr`
  );
  loading.value = false;
};

onMounted(async () => {
  await loadStudent();
});
watch(() => route.params.id, loadStudent);
</script>
