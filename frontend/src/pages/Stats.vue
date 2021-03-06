<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div v-if="stats.students.length > 0">
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
                  À la croisée de chaque colonne et de chaque ligne, 2
                  indicateurs :
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
                      L'évaluation associée à cet élève pour cette compétence
                      (sur la droite), avec :
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
                      est cliquable et vous emmène là où vous pourrez observer
                      ou évaluer !
                    </div>
                    <div>
                      D'ailleurs, les numéros de chaque compétence sont
                      cliquables également !
                    </div>
                  </div>
                  <div class="mt-4">
                    Et maintenant, votre mission, si vous l'acceptez, mettre de
                    la couleur sur cette page ! 🎨
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
                  v-for="(student, idx) in stats.students"
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
                v-for="byCompetency in stats.stats"
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
                      <StatObservationBox
                        :link="`/new-observation-prefill/${byStudent.student_id}/${byCompetency.competency.id}`"
                        :observations="byStudent.observations"
                      />
                    </div>
                  </td>
                  <td
                    class="w-8 h-6 text-center"
                    :class="idx % 2 === 1 ? 'bg-gray-200' : 'bg-white'"
                  >
                    <div class="block mr-2">
                      <StatEvaluationBox
                        :link="`/evaluation-single/${route.params.cycle}/${byCompetency.competency.id}/${byStudent.student_id}`"
                        :status="byStudent.evaluation"
                      />
                    </div>
                  </td>
                </template>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else>
        <MascotteTip class="my-2">
          <template v-slot:title>
            Bienvenue sur la page des statistiques détaillées ! 🧐
          </template>
          <template v-slot:default>
            <div class="mt-4">
              Il n'y a rien ici, parce que (pour l'instant...) aucun élève n'est
              en cycle
              {{ cycleNb(route.params.cycle) }} !
            </div>
            <div class="mt-4">
              Vous pouvez en rajouter un
              <router-link
                class="font-extrabold text-teal-500"
                to="/new-student"
              >
                ici
              </router-link>
              !
            </div>
          </template>
        </MascotteTip>
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
    </Loading>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until, useTitle } from "@vueuse/core";
import { cycleNb, cycleValid } from "../utils/cycle";
import { fathers } from "../utils/competency";
import Modal from "../components/Modal.vue";
import Loading from "../components/Loading.vue";
import MascotteTip from "../components/MascotteTip.vue";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import HashSubjects from "../components/HashSubjects.vue";
import CompetencyTemplates from "../components/CompetencyTemplates.vue";
import StatEvaluationBox from "../components/StatEvaluationBox.vue";
import StatObservationBox from "../components/StatObservationBox.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

const store = useStore();
const route = useRoute();

useTitle(`Statistiques avancées ${route.params.cycle}  - soklaki.fr`);

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
const stats = ref({});

const loadStats = async () => {
  if (!cycleValid(route.params.cycle)) {
    return;
  }
  loading.value = true;
  stats.value = await store.dispatch("statsByCycle", route.params.cycle);
  useTitle(`Statistiques avancées ${route.params.cycle}  - soklaki.fr`);
  loading.value = false;
};

onMounted(async () => {
  await loadStats();
});
watch(() => route.params.cycle, loadStats);
</script>

<style>
.writing-mode-vertical-lr {
  writing-mode: vertical-lr;
}
.full-width {
  width: calc(100vw - 3 * 0.5rem);
}
</style>
