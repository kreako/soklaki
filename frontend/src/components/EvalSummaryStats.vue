<template>
  <div>
    <div class="flex flex-row space-x-2 text-xs text-gray-500 justify-end">
      <div>{{ stats.studentsCount }} élèves</div>
      <div class="text-xs text-gray-500">
        {{ stats.competenciesCount }} Compétences
      </div>
    </div>
    <div>
      <div class="flex flex-row items-end">
        <div class="flex-grow">Commentaires</div>
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
        <div class="flex-grow">Évaluations</div>
        <div class="text-gray-700 text-xs">
          {{ stats.evaluations.current }} / {{ stats.evaluations.total }}
        </div>
      </div>
      <ProgressBar
        :current="stats.evaluations.current"
        :total="stats.evaluations.total"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed } from "vue";
import { useStore } from "vuex";
import ProgressBar from "./ProgressBar.vue";

const props = defineProps({
  stats: Object,
});
</script>
