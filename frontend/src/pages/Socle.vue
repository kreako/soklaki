<template>
  <div class="my-4 px-2">
    <div class="flex flex-row justify-end space-x-2">
      <router-link to="/socle/edit" class="button-minor-action text-xs"
        >Modifier</router-link
      >
      <ElegantSelect v-model="cycleFilter" :options="allCyclesOptions" />
      <ElegantSelect v-model="subjectFilter" :options="allSubjectsOptions" />
    </div>
    <div v-if="cycleFilter === 'all' || cycleFilter === 'c1'">
      <div class="form-label text-xl mt-4">Socle - cycle 1</div>
      <div class="mt-4">
        <SocleDisplay
          :socle="socle"
          cycle="c1"
          :subjectFilter="subjectFilter"
        />
      </div>
    </div>
    <div v-if="cycleFilter === 'all' || cycleFilter === 'c2'">
      <div class="form-label text-xl mt-4">Socle - cycle 2</div>
      <div class="mt-4">
        <SocleDisplay
          :socle="socle"
          cycle="c2"
          :subjectFilter="subjectFilter"
        />
      </div>
    </div>
    <div v-if="cycleFilter === 'all' || cycleFilter === 'c3'">
      <div class="form-label text-xl mt-4">Socle - cycle 3</div>
      <div class="mt-4">
        <SocleDisplay
          :socle="socle"
          cycle="c3"
          :subjectFilter="subjectFilter"
        />
      </div>
    </div>
    <div v-if="cycleFilter === 'all' || cycleFilter === 'c4'">
      <div class="form-label text-xl mt-4">Socle - cycle 4</div>
      <div class="mt-4">
        <SocleDisplay
          :socle="socle"
          cycle="c4"
          :subjectFilter="subjectFilter"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { useTitle } from "@vueuse/core";
import SocleDisplay from "../components/SocleDisplay.vue";
import ElegantSelect from "../components/ElegantSelect.vue";

useTitle("Socle - soklaki.fr");

const store = useStore();
const route = useRoute();
const router = useRouter();

const socle = computed(() => store.state.socle);

// TODO route for deep navigation with filters option
const cycleFilter = ref("all");
const allCyclesOptions = [
  { value: "all", text: "Tous" },
  { value: "c1", text: "Cycle 1" },
  { value: "c2", text: "Cycle 2" },
  { value: "c3", text: "Cycle 3" },
  { value: "c4", text: "Cycle 4" },
];

const subjectFilter = ref("all");
const allSubjectsOptions = computed(() => {
  const subjects = [{ value: "all", text: "Tous" }];
  for (const subject of Object.values(store.state.socle.subjects)) {
    subjects.push({ value: subject.id.toString(), text: subject.title });
  }
  return subjects;
});
</script>
