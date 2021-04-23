<template>
  <div class="flex flex-row">
    <div class="w-16"></div>
    <div
      v-for="studentId in students"
      class="text-xs w-8 self-end writing-mode-vertical-lr"
    >
      {{ studentById(studentId).firstname }}
      {{ studentById(studentId).lastname }}
    </div>
  </div>
  <div class="mt-2">
    <div
      v-for="(statByStudents, competencyId) in stats.stats"
      class="flex flex-row items-center leading-tight"
    >
      <div class="w-16 text-gray-700 text-right pr-2">
        {{ competencyById(competencyId).full_rank }}
      </div>
      <div
        v-for="(stat, studentId) in statByStudents"
        class="flex flex-row space-x-1 w-8"
      >
        <div
          :class="stat.observations > 0 ? 'bg-green-500' : 'bg-red-500'"
          class="w-2 h-2"
        ></div>
        <div
          :class="stat.evaluations > 0 ? 'bg-green-500' : 'bg-red-500'"
          class="w-2 h-2"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from "vue";
import { useStore } from "vuex";
import ProgressBar from "./ProgressBar.vue";

const props = defineProps({
  stats: Object,
});

const store = useStore();

const studentById = computed(() => store.getters.studentById);
const competencyById = computed(() => store.getters.competencyById);

// extract the list of students id
const students = computed(() => Object.keys(props.stats.commentsCount));
</script>

<style>
.writing-mode-vertical-lr {
  writing-mode: vertical-lr;
}
</style>
