<template>
  <div class="my-4 px-2">
    <div class="form-label">Les rapports de la période {{ period.name }}</div>
    <div class="form-sub-label">{{ period.start }} - {{ period.end }}</div>
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
          <div>
            <router-link
              :to="`/report-draft/${route.params.periodId}/${report.cycle}/${report.studentId}`"
            >
              <IconDocumentReport
                class="h-4 text-gray-400 hover:text-teal-500"
              />
            </router-link>
          </div>
        </div>
        <div class="flex flex-row items-center space-x-6">
          <div class="flex-grow text-sm">
            <div v-if="report.reportId == null" class="text-gray-700">
              <router-link
                :to="`/report-draft/${route.params.periodId}/${report.cycle}/${report.studentId}`"
              >
                Pas encore de rapport
              </router-link>
            </div>
            <div v-else>Voir le rapport</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import IconDocumentReport from "../icons/IconDocumentReport.vue";
import ProgressBar from "../components/ProgressBar.vue";

const store = useStore();
const route = useRoute();

const studentById = computed(() => store.getters.studentById);
const period = computed(() => store.getters.periodById(route.params.periodId));

const reportsPerStudent = computed(() => {
  const reports = [];
  const periodId = period.value.id;
  const src = store.state.reports.sorted[Number(route.params.periodId)];
  for (const s of period.value.students) {
    const studentId = s.student_id;
    const cycle = s.cycle;
    let reportId = null;
    if (src != null) {
      const f = src.find((x) => x.student_id === studentId);
      if (f != null) {
        reportId = f.id;
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
