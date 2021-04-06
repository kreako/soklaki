<template>
  <div>
    <div class="flex flex-row items-center mt-2">
      <input
        v-model="filter"
        class="input w-full flex-grow"
        type="text"
        placeholder="Filtre..."
      />
      <button alt="Abandonner la sélection" @click="$emit('cancel')">
        <IconXCircle class="text-gray-300 h-4 mx-2 hover:text-gray-600" />
      </button>
    </div>
    <div class="grid grid-cols-1 max-h-46 overflow-y-auto mt-2 bg-gray-50">
      <div
        v-for="id in filteredStudents"
        :key="id"
        class="px-2 flex flex-row items-center gap-2"
      >
        <button class="group flex flex-row" @click="$emit('select', id)">
          <IconPlusCircle
            class="w-4 text-gray-300 group-hover:text-gray-600 mr-2"
          />
          <div>{{ students[id].firstname }} {{ students[id].lastname }}</div>
        </button>
      </div>
      <div class="px-2 flex flex-row items-center gap-2">
        <button class="group flex flex-row" @click="$emit('cancel')">
          <IconXCircle class="w-4 text-red-300 group-hover:text-red-600 mr-2" />
          <div>Ne sélectionnez... personne !</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmit, defineProps, ref, computed } from "vue";
import IconX from "../icons/IconX.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";
import IconXCircle from "../icons/IconXCircle.vue";

defineEmit(["select", "cancel"]);

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
