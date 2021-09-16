<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
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
        <div v-for="student in students" class="mt-6">
          <div class="flex flex-row items-center space-x-4">
            <div>
              <router-link :to="`/student/${student.id}`">
                {{ student.firstname }}
                {{ student.lastname }}
              </router-link>
            </div>
            <div class="text-xs rounded-full px-1 border border-gray-600">
              {{ student.cycle.toUpperCase() }}
            </div>
          </div>
          <div class="text-sm">Anniversaire : {{ student.birthdate }}</div>
          <div class="text-sm">Date d'entrée : {{ student.school_entry }}</div>
          <div v-if="student.school_exit != null" class="text-sm">
            Date de sortie : {{ student.school_exit }}
          </div>
        </div>
      </div>
      <div class="mt-8">
        <div class="flex flex-row items-center space-x-2 button-minor-action">
          <router-link to="/new-student">
            <IconPlus class="h-4" />
          </router-link>
          <router-link to="/new-student">Ajouter un élève</router-link>
        </div>
      </div>
    </Loading>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useTitle } from "@vueuse/core";
import { computed, ref, onMounted, watch } from "vue";
import ElegantSelect from "../components/ElegantSelect.vue";
import IconPlus from "../icons/IconPlus.vue";
import Loading from "../components/Loading.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();
const loading = ref(true);
const students = ref([]);
const periods = ref([]);
const currentPeriod = ref(null);

useTitle("Élèves - soklaki.fr");

const allCyclesOptions = [
  { value: "all", text: "Tous" },
  { value: "c1", text: "Cycle 1" },
  { value: "c2", text: "Cycle 2" },
  { value: "c3", text: "Cycle 3" },
  { value: "c4", text: "Cycle 4" },
];

const allPeriodsOptions = computed(() => {
  if (currentPeriod.value == null) {
    // not ready
    return [];
  }
  const options = [];
  // First push the current period
  options.push({
    value: currentPeriod.value.id.toString(),
    text: "Courante",
  });
  for (const period of periods.value) {
    options.push({ value: period.id.toString(), text: period.name });
  }
  options.push({ value: "all", text: "Toutes" });
  return options;
});

const periodFilter = ref(route.query.period);
watch(periodFilter, async (f, prevF) => {
  if (route.query.period != f) {
    router.replace({
      query: {
        period: f,
        cycle: route.query.cycle,
      },
    });
    await loadStudents(f, route.query.cycle);
  }
});

const cycleFilter = ref(route.query.cycle);
watch(cycleFilter, async (f, prevF) => {
  if (route.query.cycle != f) {
    router.replace({
      query: {
        period: route.query.period,
        cycle: f,
      },
    });
    await loadStudents(route.query.period, f);
  }
});

watch(route, () => {
  if (route.path !== "/students") {
    // Not my page
    return;
  }
  if (route.query.period != periodFilter.value) {
    if (route.query.period == null) {
      if (currentPeriod.value == null) {
        periodFilter.value = null;
      } else {
        periodFilter.value = currentPeriod.value.id.toString();
      }
    } else {
      periodFilter.value = route.query.period;
    }
  }
  if (route.query.cycle != cycleFilter.value) {
    if (route.query.cycle == null) {
      cycleFilter.value = "all";
    } else {
      cycleFilter.value = route.query.cycle;
    }
  }
});

onMounted(async () => {
  await loadStudents(null, null);
});

// period : null - period=null && current=true
//          all  - period=null && current=false
//          <id> - period=id && current=false
// cycle : null - cycle="all"
//         all  - cycle="all"
//         c1   - cycle=c1
const loadStudents = async (period, cycle) => {
  loading.value = true;

  let _period = null;
  let _current = true;
  if (period != null) {
    if (period == "all") {
      _period = null;
      _current = false;
    } else {
      _period = period;
      _current = false;
    }
  }

  let _cycle = "all";
  if (cycle != null) {
    _cycle = cycle;
  }

  let data = await store.dispatch("students", {
    period: _period,
    cycle: _cycle,
    current: _current,
  });
  students.value = data.students;
  periods.value = data.periods;
  currentPeriod.value = data.current_period;

  if (route.query.period == null || route.query.cycle == null) {
    router.replace({
      query: {
        period: currentPeriod.value.id,
        cycle: _cycle,
      },
    });
    // Do not update periodFilter and cycleFilter yet
    // It will be done by the watch on route
  }

  loading.value = false;
};
</script>
