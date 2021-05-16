<template>
  <div class="my-4 px-2">
    <div class="form-label">Nouvelle période</div>
    <div class="mt-8">
      <div class="form-sub-label">Le nom de la période</div>
      <input type="text" v-model="name" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date de début</div>
      <DatePicker :value="start" @selected="start = $event" class="mt-2" />
      <input type="text" v-model="start" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date de fin</div>
      <DatePicker :value="end" @selected="end = $event" class="mt-2" />
      <input type="text" v-model="end" class="mt-2 input w-full" />
    </div>
    <div class="flex flex-row space-x-2 items-center mt-8">
      <button @click="cancel" class="button-minor-action flex-grow-0">
        Annuler
      </button>
      <button @click="save" class="button-main-action flex-grow">
        Sauvegarder
      </button>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import DatePicker from "../components/DatePicker.vue";

const store = useStore();
const router = useRouter();

const name = ref("");
const start = ref("");
const end = ref("");

const cancel = () => {
  router.back();
};

const save = async (value) => {
  // TODO date validity check
  const id = await store.dispatch("insertPeriod", {
    name: name.value,
    start: start.value,
    end: end.value,
  });
  router.push("/settings/periods");
};
</script>
