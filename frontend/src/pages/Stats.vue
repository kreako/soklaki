<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <Disclosure>
        <DisclosureButton class="">
          <div class="flex flex-row items-center space-x-2">
            <div class="form-label">
              Plein de statistiques sur le cycle
              {{ cycleNb(route.params.cycle) }}
            </div>
            <IconQuestionMark class="w-6 h-6 text-gray-500" />
          </div>
        </DisclosureButton>
        <DisclosurePanel class="py-2">
          <MascotteTip class="my-2">
            <template v-slot:title>
              Bienvenue sur la page des statistiques détaillées ! 🧐
            </template>
            <template v-slot:default>
              <div class="mt-4">
                Un grand tableau avec :
                <ul class="list-disc list-inside">
                  <li>une colonne par élève</li>
                  <li>une ligne par compétence du socle</li>
                </ul>
              </div>
              <div class="mt-4">
                À la croisée de chaque colonne et de chaque ligne, 2 indicateurs
                :
                <ul class="list-disc list-inside">
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
                  couleur sur cette page ! 🎨
                </div>
              </div>
            </template>
          </MascotteTip>
        </DisclosurePanel>
      </Disclosure>
      <div
        class="
          my-4
          overflow-auto
          w-full
          h-[calc(100vh-8rem)]
          md:h-[calc(100vh-4rem)]
          max-w-[calc(100vw-2*1rem)]
        "
      >
        <table class="relative table-fixed border-collapse w-full">
          <thead>
            <tr>
              <th class="w-16 sticky top-0 left-0 z-[3] bg-white">&nbsp;</th>
              <th
                v-for="(student, idx) in stats2.students"
                :key="student.id"
                colspan="2"
                class="font-bold w-16 sticky top-0 z-[2] text-center"
                :class="idx % 2 === 1 ? 'bg-gray-200' : 'bg-white'"
              >
                <div
                  class="
                    w-8
                    flex-shrink-0 flex flex-row
                    justify-center
                    py-2
                    mx-auto
                  "
                >
                  <div class="writing-mode-vertical-lr font-normal">
                    {{ student.firstname }}
                    {{ student.lastname }}
                  </div>
                </div>
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="byCompetency in stats2.stats"
              :key="byCompetency.competency.id"
            >
              <td class="sticky left-0 h-6 z-[1] bg-white text-center">
                <button @click="selectCompetency(byCompetency.competency.id)">
                  {{ byCompetency.competency.full_rank }}
                </button>
              </td>
              <template
                v-for="(byStudent, idx) in byCompetency.by_students"
                :key="byStudent.id"
              >
                <td
                  class="w-8 h-6 text-center"
                  :class="idx % 2 === 1 ? 'bg-gray-200' : 'bg-white'"
                >
                  <div class="block ml-2">
                    <button
                      @click="
                        selectObservation(
                          byCompetency.competency.id,
                          byStudent.student_id
                        )
                      "
                      :class="
                        byStudent.observations > 0
                          ? 'bg-green-500'
                          : 'bg-gray-500'
                      "
                      class="
                        align-middle
                        w-5
                        h-5
                        text-xs
                        rounded-md
                        block
                        mx-auto
                      "
                    >
                      {{ byStudent.observations }}
                    </button>
                  </div>
                </td>
                <td
                  class="w-8 h-6 text-center"
                  :class="idx % 2 === 1 ? 'bg-gray-200' : 'bg-white'"
                >
                  <div class="block mr-2">
                    <router-link
                      :to="`/evaluation-single/${route.params.cycle}/${byCompetency.competency.id}/${byStudent.student_id}`"
                      :class="{
                        'bg-gray-500': byStudent.evaluation === 'Empty',
                        'bg-red-500': byStudent.evaluation === 'NotAcquired',
                        'bg-yellow-500': byStudent.evaluation === 'InProgress',
                        'bg-green-500': byStudent.evaluation === 'Acquired',
                        'bg-pink-500': byStudent.evaluation === 'TipTop',
                      }"
                      class="w-5 h-5 rounded-md align-middle block mx-auto"
                    ></router-link>
                  </div>
                </td>
              </template>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>

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
      <Modal
        :title="observationModalTitle"
        :show="showObservationModal"
        @close="closeObservationModal"
      >
        <div>
          <div class="uppercase tracking-wide text-gray-700 text-xs">
            {{ competencyFathers[0].rank }}.
            {{ competencyFathers[0].text }}
          </div>
          <div
            v-if="competencyFathers[1].rank != null"
            class="text-gray-700 text-xs"
          >
            {{ competencyFathers[1].rank }}.
            {{ competencyFathers[1].text }}
          </div>
          <div class="text-sm">
            {{ competencyById(selectedCompetency).rank }}.
            {{ competencyById(selectedCompetency).text }}
          </div>
          <div class="pl-2">
            <HashSubjects
              :subjects="competencyById(selectedCompetency).subjects"
            />
          </div>
          <div
            v-if="competencyById(selectedCompetency).templates.length > 0"
            class="mt-8 pl-2"
          >
            <div class="font-bold">
              Créer une nouvelle observation à partir d'un modèle
            </div>
            <ul class="mt-2">
              <li
                v-for="template in competencyById(selectedCompetency).templates"
                class="mt-1 hover:text-teal-500"
              >
                <router-link
                  :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${template.id}`"
                >
                  {{ templateById(template.id).text }}
                </router-link>
              </li>
              <li class="mt-3 hover:text-teal-500">
                <router-link
                  :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${-1}`"
                >
                  Sans modèle
                </router-link>
              </li>
            </ul>
          </div>
          <div v-else class="mt-8 pl-2">
            <div class="hover:text-teal-500">
              <router-link
                :to="`/new-observation-from-template/${selectedStudent}/${selectedCompetency}/${-1}`"
              >
                Créer une nouvelle observation
              </router-link>
            </div>
          </div>
        </div>
      </Modal>
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until, useTitle } from "@vueuse/core";
import { cycleNb } from "../utils/cycle";
import { fathers } from "../utils/competency";
import Modal from "../components/Modal.vue";
import Loading from "../components/Loading.vue";
import MascotteTip from "../components/MascotteTip.vue";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";
import HashSubjects from "../components/HashSubjects.vue";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

const store = useStore();
const route = useRoute();

useTitle(`Statistiques avancées ${route.params.cycle}  - soklaki.fr`);

const studentById = computed(() => store.getters.studentById);
const competencyById = computed(() => store.getters.competencyById);

const stats = computed(() => store.state.stats[route.params.cycle]);

const breakpoints = useBreakpoints(breakpointsTailwind);
const mobile = breakpoints.smaller("md");

const selectedCompetency = ref(null);
const selectedStudent = ref(null);

const showObservationModal = ref(false);
const selectObservation = (competencyId, studentId) => {
  selectedCompetency.value = competencyId;
  selectedStudent.value = studentId;
  showObservationModal.value = true;
};
const closeObservationModal = () => {
  showObservationModal.value = false;
};
const observationModalTitle = computed(() => {
  if (selectedCompetency.value == null) {
    return null;
  }
  const competency = competencyById.value(selectedCompetency.value);
  const student = studentById.value(selectedStudent.value);
  return `Observation de ${competency.full_rank} pour ${student.firstname} ${student.lastname}`;
});
const templateById = computed(() => store.getters.templateById);

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
const stats2 = ref({});

onMounted(async () => {
  stats2.value = await store.dispatch("statsByCycle", route.params.cycle);
  loading.value = false;
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("stats", { periodId: store.state.currentPeriod });
});
</script>

<style>
.writing-mode-vertical-lr {
  writing-mode: vertical-lr;
}
.full-width {
  width: calc(100vw - 3 * 0.5rem);
}
</style>
