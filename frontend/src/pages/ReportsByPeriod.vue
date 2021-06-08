<template>
  <div class="my-4 px-2">
    <div class="form-label">Les rapports de la période {{ period.name }}</div>
    <div class="form-sub-label">{{ period.start }} - {{ period.end }}</div>
    <div class="flex flex-row justify-end">
      <button @click="updateReports" class="button-minor-action">
        Générer les rapports
      </button>
    </div>
    <div class="flex flex-row justify-end mt-1">
      <a
        :href="`/zip_reports/${groupId}/${period.id}`"
        target="_blank"
        class="button-minor-action"
      >
        Tout télécharger
      </a>
    </div>
    <div class="mt-8">
      <div class="flex flex-row items-end">
        <div class="flex-grow">Rapports</div>
        <div class="text-gray-700 text-xs">
          {{ reportsStats.current }} / {{ reportsStats.total }}
        </div>
      </div>
      <ProgressBar
        :current="reportsStats.current"
        :total="reportsStats.total"
      />
    </div>
    <div class="mt-12">
      <div v-for="report in reportsPerStudent" class="mt-8">
        <div class="flex flex-row items-center space-x-6">
          <div>
            {{ studentById(report.studentId).firstname }}
            {{ studentById(report.studentId).lastname }}
          </div>
          <div class="text-sm text-gray-600 uppercase tracking-wide font-bold">
            {{ report.cycle }}
          </div>
        </div>
        <div class="flex flex-row items-center space-x-6">
          <div class="flex-grow text-sm">
            <div
              v-if="report.reportId == null"
              class="text-gray-700 hover:text-teal-500"
            >
              <button @click="generateReport(report.studentId)">
                Générer un rapport
              </button>
            </div>
            <div v-else class="flex items-center space-x-4">
              <a
                :href="reportById(report.reportId).pdf_path"
                target="_blank"
                class="hover:text-teal-500"
              >
                Voir le rapport
              </a>
              <button @click="updateReport(report.studentId)">
                <IconRefresh class="h-4 text-gray-400 hover:text-teal-500" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ModalConfirmCancel
    title="Confirmation"
    :show="showUpdateModal"
    @confirm="confirmUpdate"
    @cancel="cancelUpdate"
  >
    <div>
      Êtes-vous sûr de vouloir mettre à jour le rapport pour
      {{ studentById(selectedStudentId).firstname }}
      {{ studentById(selectedStudentId).lastname }} ?
    </div>
  </ModalConfirmCancel>
  <ModalConfirmCancel
    title="Confirmation"
    :show="showUpdatesModal"
    @confirm="confirmUpdates"
    @cancel="cancelUpdates"
  >
    <div>Êtes-vous sûr de vouloir mettre à jour tous les rapports ?</div>
    <div class="mt-4">
      <div class="flex flex-row items-end">
        <div class="flex-grow text-sm">Progression</div>
        <div class="text-gray-700 text-xs">
          {{ updatesCount }} / {{ period.students.length }}
        </div>
      </div>
      <ProgressBar :current="updatesCount" :total="period.students.length" />
    </div>
  </ModalConfirmCancel>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import IconRefresh from "../icons/IconRefresh.vue";
import ProgressBar from "../components/ProgressBar.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";
import { useTitle } from "@vueuse/core";

useTitle("Rapports - soklaki.fr");

const store = useStore();
const route = useRoute();

const studentById = computed(() => store.getters.studentById);
const reportById = computed(() => store.getters.reportById);
const period = computed(() => store.getters.periodById(route.params.periodId));
const groupId = computed(() => store.state.login.groupId);

const reportsPerStudent = computed(() => {
  const reports = [];
  const periodId = period.value.id;
  const src = store.state.reports.sorted[Number(route.params.periodId)];
  for (const s of period.value.students) {
    const studentId = s.student_id;
    const cycle = s.cycle;
    let reportId = null;
    if (src != null) {
      const f = src.find(
        (x) => store.state.reports.store[x].student_id === studentId
      );
      if (f != null) {
        reportId = f;
      }
    }
    reports.push({
      studentId: studentId,
      cycle: cycle,
      reportId: reportId,
    });
  }
  return reports;
});

const generateReport = async (studentId) => {
  await store.dispatch("generateReport", {
    periodId: Number(route.params.periodId),
    studentId: studentId,
  });
  await store.dispatch("reports");
};

const showUpdateModal = ref(false);
const selectedStudentId = ref(null);
const updateReport = (studentId) => {
  selectedStudentId.value = studentId;
  showUpdateModal.value = true;
};
const cancelUpdate = () => {
  selectedStudentId.value = null;
  showUpdateModal.value = false;
};
const confirmUpdate = async () => {
  await store.dispatch("generateReport", {
    periodId: Number(route.params.periodId),
    studentId: selectedStudentId.value,
  });
  await store.dispatch("reports");
  selectedStudentId.value = null;
  showUpdateModal.value = false;
};

const showUpdatesModal = ref(false);
const updateReports = (studentId) => {
  updatesCount.value = 0;
  showUpdatesModal.value = true;
};
const cancelUpdates = () => {
  showUpdatesModal.value = false;
};
const confirmUpdates = async () => {
  updatesCount.value = 0;
  for (const student of period.value.students) {
    await store.dispatch("generateReport", {
      periodId: Number(route.params.periodId),
      studentId: student.student_id,
    });
    updatesCount.value += 1;
  }
  await store.dispatch("reports");
  showUpdatesModal.value = false;
};
const updatesCount = ref(0);

const reportsStats = ref({ total: 0, current: 0 });
watch(reportsPerStudent, () => {
  reportsStats.value.total = reportsPerStudent.value.length;
  reportsStats.value.current = reportsPerStudent.value.filter(
    (x) => x.reportId != null
  ).length;
});

onMounted(async () => {
  await store.dispatch("reports");
});
</script>
