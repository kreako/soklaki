<template>
  <div>
    <div class="flex flex-row space-x-2 text-xs text-gray-500 justify-end">
      <div>{{ stats.student_count }} élèves</div>
      <div class="text-xs text-gray-500">
        {{ stats.competencies_count }} Compétences
      </div>
    </div>
    <div>
      <div class="flex flex-row items-end">
        <div class="flex-grow">Commentaires</div>
        <div class="text-gray-700 text-xs">
          {{ stats.comment_count }} / {{ stats.comment_total }}
        </div>
      </div>
      <ProgressBar
        :current="stats.comment_count"
        :total="stats.comment_total"
      />
    </div>
    <div>
      <div class="flex flex-row items-end">
        <div class="flex-grow">Évaluations</div>
        <div class="text-gray-700 text-xs">
          {{ stats.eval_count }} / {{ stats.eval_total }}
        </div>
      </div>
      <ProgressBar :current="stats.eval_count" :total="stats.eval_total" />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed } from "vue";
import ProgressBar from "./ProgressBar.vue";

const props = defineProps({
  stats: Object,
});
</script>
