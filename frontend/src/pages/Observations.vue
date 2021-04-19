<template>
  <div class="mt-4 px-2">
    <div class="form-label">Observations</div>
    <div class="flex flex-row justify-end relative">
      <select
        v-model="selectedFilter"
        class="appearance-none block bg-transparent py-1 pr-3 text-gray-500 font-medium text-sm focus:outline-none focus:text-gray-900 transition-colors duration-200"
      >
        <option value="all">Filtres</option>
        <option value="incomplete">Les incomplètes</option>
        <option value="mine">Mes observations</option>
      </select>
      <IconChevronDown
        class="h-4 absolute top-1/2 right-0 -mt-2 pointer-events-none"
      />
    </div>
    <div>
      <div v-for="observationId in sortedObservations" class="mt-6">
        <div class="flex flex-row items-center space-x-4">
          <div>
            <router-link :to="`/observation/${observationId}`">
              {{ observations[observationId].date }}
            </router-link>
          </div>
          <div class="text-xs rounded-full px-1 border border-gray-600">
            {{ userInitials(userById(observations[observationId].user_id)) }}
          </div>
          <div class="flex-grow"></div>
          <div class="flex flex-row items-center space-x-2">
            <div>
              {{ observations[observationId].students.length }}
            </div>
            <IconUser class="h-4 text-gray-500" />
          </div>
          <div class="flex flex-row items-center space-x-2">
            <div>
              {{ observations[observationId].competencies.length }}
            </div>
            <IconCompetency class="h-4 text-gray-500" />
          </div>
        </div>
        <div class="truncate">
          <router-link :to="`/observation/${observationId}`">
            {{ observations[observationId].text }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { userInitials } from "../utils/user";
import IconChevronDown from "../icons/IconChevronDown.vue";
import IconUser from "../icons/IconUser.vue";
import IconCompetency from "../icons/IconCompetency.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const userById = computed(() => store.getters.userById);

const selectedFilter = ref(route.query.filter || "all");
watch(selectedFilter, (filter, prevFilter) => {
  if (route.query.filter !== filter) {
    router.push({
      query: {
        limit: route.query.limit,
        offset: route.query.offset,
        filter: filter,
      },
    });
  }
});

watch(route, async () => {
  await updateObservations();
});
const updateObservations = async () => {
  if (route.query.filter !== selectedFilter.value) {
    selectedFilter.value = route.query.filter;
  }
  if (route.query.filter === "all") {
    await store.dispatch("observations", {
      limit: Number(route.query.limit),
      offset: Number(route.query.offset),
    });
  } else if (route.query.filter === "mine") {
    await store.dispatch("observationsByUser", {
      userId: store.state.login.userId,
      limit: Number(route.query.limit),
      offset: Number(route.query.offset),
    });
  }
};

const observations = computed(() => store.state.observations);
const sortedObservations = computed(
  () => store.state.sortedCreatedAtObservations
);
onMounted(async () => {
  const limit = route.query.limit || 50;
  const offset = route.query.offset || 0;
  const filter = route.query.filter || "all";

  if (
    route.query.limit == null ||
    route.query.offset == null ||
    route.query.filter == null
  ) {
    router.replace({
      query: {
        limit: limit,
        offset: offset,
        filter: filter,
      },
    });
  } else {
    await updateObservations();
  }
});
</script>
