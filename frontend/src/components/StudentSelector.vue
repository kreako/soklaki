<template>
  <div>
    <input
      v-model="filter"
      class="input w-full mt-2"
      type="text"
      placeholder="Filtre..."
    />
    <div class="grid grid-cols-1 max-h-46 overflow-y-auto mt-2 bg-gray-50">
      <div
        v-for="id in filteredStudents"
        :key="id"
        class="px-2 flex flex-row items-center gap-2"
      >
        <button class="flex flex-row" @click="$emit('select', id)">
          <IconPlusCircle class="w-4 text-gray-300 mr-2" />
          {{ students[id].firstname }} {{ students[id].lastname }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmit, defineProps, ref, computed } from "vue";
import IconX from "../icons/IconX.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

defineEmit(["select"]);

const props = defineProps({
  students: Object,
  sortedStudents: Array,
});

const filter = ref("");

const filteredStudents = computed(() =>
  props.sortedStudents.filter((id) => {
    if (filter.value.length === 0) {
      return true;
    }
    let r = new RegExp(filter.value, "i");
    return (
      r.test(props.students[id].firstname) ||
      r.test(props.students[id].lastname)
    );
  })
);
</script>
