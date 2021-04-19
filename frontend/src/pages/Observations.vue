<template>
  <div class="mt-4 px-2">
    <div>Observations</div>
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
import { computed, ref, onMounted, watch } from "vue";
import { userInitials } from "../utils/user";
import IconUser from "../icons/IconUser.vue";
import IconCompetency from "../icons/IconCompetency.vue";

const store = useStore();

const userById = computed(() => store.getters.userById);

const observations = computed(() => store.state.observations);
const sortedObservations = computed(
  () => store.state.sortedCreatedAtObservations
);
onMounted(() => {
  store.dispatch("observations", { limit: 4, offset: 0 });
});
</script>
