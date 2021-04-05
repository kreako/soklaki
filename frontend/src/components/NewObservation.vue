<template>
  <div class="px-2 w-full">
    <div class="w-full">
      <div class="text-gray-800">Observation</div>
      <textarea class="mt-2 input w-full" rows="5"></textarea>
    </div>
    <div class="mt-10">
      <div class="text-gray-800">Élèves</div>
      <div class="mt-2 text-sm space-x-1 space-y-1">
        <button
          v-for="obsStudent in obsStudentsFull"
          :key="obsStudent.id"
          @click="removeStudent(obsStudent.id)"
          class="bg-teal-800 text-white px-2 rounded-md flex flex-row space-x-2 items-center"
        >
          <span> {{ obsStudent.firstname }} {{ obsStudent.lastname }} </span>
          <IconX class="w-3 text-gray-200" />
        </button>
      </div>
      <input
        v-model="studentFilter"
        class="input w-full mt-2"
        type="text"
        placeholder="Filtre..."
      />
      <div class="grid grid-cols-1 max-h-46 overflow-y-auto mt-2 bg-gray-50">
        <div
          v-for="student in filteredStudents"
          :key="student.id"
          class="px-2 flex flex-row items-center gap-2"
        >
          <button class="flex flex-row" @click="selectStudent(student.id)">
            <IconPlusCircle class="w-4 text-gray-300 mr-2" />
            {{ student.firstname }} {{ student.lastname }}
          </button>
        </div>
      </div>
    </div>
    <div class="mt-10">
      <CompetenciesSelector
        @selected="selectCompetency"
        :socle="socle"
        cycle="c2"
      />
    </div>
    <div class="mt-8">
      <button @click="save" class="button-main-action">Enregistrer</button>
    </div>
  </div>
</template>

<script setup>
import { defineEmit, defineProps, ref, computed } from "vue";
import IconX from "../icons/IconX.vue";
import IconPlusCircle from "../icons/IconPlusCircle.vue";

defineEmit(["save"]);

const props = defineProps({
  socle: Object,
  students: Array,
});

const obsText = ref("");

const obsStudents = ref([]);

const studentFilter = ref("");

const filteredStudents = computed(() =>
  props.students
    .filter((student) => {
      if (studentFilter.value.length === 0) {
        return true;
      }
      let r = new RegExp(studentFilter.value, "i");
      return r.test(student.firstname) || r.test(student.lastname);
    })
    .filter((student) => obsStudents.value.indexOf(student.id) === -1)
);

const obsStudentsFull = computed(() =>
  props.students.filter(
    (student) => obsStudents.value.indexOf(student.id) !== -1
  )
);

const selectStudent = (id) => {
  obsStudents.value.push(id);
};

const removeStudent = (id) => {
  let idx = obsStudents.value.indexOf(id);
  obsStudents.value.splice(idx, 1);
};

const obsCompetencies = ref([]);
const selectCompetency = (id) => {
  window.console.log("selectCompetency", id);
};

const socleFilter = ref("");

const socleFiltered = computed(() => props.socle.filter());

const save = () => {
  this.$emit("save", { obsText, obsStudents, obsCompetencies });
};
</script>
