<template>
  <div class="flex flex-row items-center space-x-2">
    <div>
      {{ stats.students_count }}
    </div>
    <div>élèves</div>
    <div class="text-xs text-gray-500">
      {{ stats.competencies_count }} Compétences
    </div>
  </div>
  <div>
    <div class="flex flex-row items-end">
      <div class="flex-grow text-sm text-gray-700">Commentaires</div>
      <div class="text-gray-700 text-xs">
        {{ stats.comments.current }} / {{ stats.comments.total }}
      </div>
    </div>
    <ProgressBar
      :current="stats.comments.current"
      :total="stats.comments.total"
    />
  </div>
  <div>
    <div class="flex flex-row items-end">
      <div class="flex-grow text-sm text-gray-700">Observations</div>
      <div class="text-gray-700 text-xs">
        {{ stats.observations.current }} / {{ stats.observations.total }}
      </div>
    </div>
    <ProgressBar
      :current="stats.observations.current"
      :total="stats.observations.total"
    />
  </div>
  <div>
    <div class="flex flex-row items-end">
      <div class="flex-grow text-sm text-gray-700">Évaluations</div>
      <div class="text-gray-700 text-xs">
        {{ stats.evaluations.current }} / {{ stats.evaluations.total }}
      </div>
    </div>
    <ProgressBar
      :current="stats.evaluations.current"
      :total="stats.evaluations.total"
    />
  </div>
</template>

<script setup>
import { defineProps, computed } from "vue";
import ProgressBar from "./ProgressBar.vue";

const props = defineProps({
  stats: Object,
});
</script>
