<template>
  <div class="my-4 px-2">
    <div class="flex flex-row space-x-4 items-center">
      <div class="form-label">Élèves</div>
      <router-link
        to="/new-student"
        class="text-gray-700 text-xs hover:text-teal-500"
      >
        Ajouter un élève
      </router-link>
    </div>
    <div class="flex flex-row justify-end space-x-2">
      <ElegantSelect v-model="periodFilter" :options="allPeriodsOptions" />
      <ElegantSelect v-model="cycleFilter" :options="allCyclesOptions" />
    </div>
    <div>
      <div v-for="studentId in students" class="mt-6">
        <div class="flex flex-row items-center space-x-4">
          <div>
            <router-link :to="`/student/${studentId}`">
              {{ studentById(studentId).firstname }}
              {{ studentById(studentId).lastname }}
            </router-link>
          </div>
          <div class="text-xs rounded-full px-1 border border-gray-600">
            {{
              studentById(studentId).current_cycle.current_cycle.toUpperCase()
            }}
          </div>
        </div>
        <div class="text-sm">
          Anniversaire : {{ studentById(studentId).birthdate }}
        </div>
        <div class="text-sm">
          Date d'entrée : {{ studentById(studentId).school_entry }}
        </div>
        <div v-if="studentById(studentId).school_exit != null" class="text-sm">
          Date de sortie : {{ studentById(studentId).school_exit }}
        </div>
      </div>
    </div>
    <div class="mt-8">
      <div class="flex flex-row items-center space-x-2 button-minor-action">
        <router-link to="/new-student">
          <IconPlus class="h-4" />
        </router-link>
        <router-link to="/new-student"> Ajouter un élève </router-link>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import ElegantSelect from "../components/ElegantSelect.vue";
import IconPlus from "../icons/IconPlus.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

useTitle("Élèves - soklaki.fr");

const allCyclesOptions = [
  { value: "all", text: "Tous" },
  { value: "c1", text: "Cycle 1" },
  { value: "c2", text: "Cycle 2" },
  { value: "c3", text: "Cycle 3" },
  { value: "c4", text: "Cycle 4" },
];

const allPeriodsOptions = computed(() => {
  if (store.state.currentPeriod == null) {
    // store not ready
    return [];
  }
  const periods = [];
  // First push the current period
  const currentPeriod = store.getters.periodById(store.state.currentPeriod);
  periods.push({
    value: store.state.currentPeriod.toString(),
    text: "Courante",
  });
  for (const id of store.state.sortedPeriods) {
    const period = store.getters.periodById(id);
    periods.push({ value: id.toString(), text: period.name });
  }
  periods.push({ value: String(-1), text: "Toutes" });
  return periods;
});
const periodFilter = ref(route.query.period);
watch(periodFilter, (f, prevF) => {
  if (route.query.period != f) {
    router.replace({
      query: {
        period: f,
        cycle: route.query.cycle,
      },
    });
  }
});
const cycleFilter = ref(route.query.cycle);
watch(cycleFilter, (f, prevF) => {
  if (route.query.cycle != f) {
    router.replace({
      query: {
        period: route.query.period,
        cycle: f,
      },
    });
  }
});

watch(route, () => {
  if (route.path !== "/students") {
    // Not my page
    return;
  }
  if (route.query.period != periodFilter.value) {
    periodFilter.value = route.query.period;
  }
  if (route.query.cycle != cycleFilter.value) {
    cycleFilter.value = route.query.cycle;
  }
});

const students = computed(() => {
  if (periodFilter.value == null || cycleFilter.value == null) {
    // not ready yet
    return [];
  }
  // First set students base on period
  let students = [];
  if (periodFilter.value === "-1") {
    students = store.state.sortedStudents;
  } else {
    const period = store.getters.periodById(Number(periodFilter.value));
    students = period.students.map((x) => x.student.id);
  }
  // And now on current cycle
  if (cycleFilter.value !== "all") {
    const cycle = cycleFilter.value;
    students = students.filter(
      (id) =>
        store.getters.studentById(id).current_cycle.current_cycle === cycle
    );
  }
  return students;
});
const studentById = computed(() => store.getters.studentById);

onMounted(async () => {
  if (route.query.period == null || route.query.cycle == null) {
    if (store.state.currentPeriod != null) {
      // If when mounted the store is not warm the next watch will kick in
      router.replace({
        query: {
          period: store.state.currentPeriod,
          cycle: "all",
        },
      });
    }
  }
});
// In case the store was not ready, set period to currentPeriod
watch(
  () => store.state.currentPeriod,
  (current, prevCurrent) => {
    if (prevCurrent != null) {
      return;
    }
    if (current == null) {
      return;
    }
    if (route.query.period != null || route.query.cycle != null) {
      return;
    }
    router.replace({
      query: {
        period: store.state.currentPeriod,
        cycle: "all",
      },
    });
  }
);
</script>
