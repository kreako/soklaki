<template>
  <div class="my-4 px-2">
    <div class="form-label">Une période d'évaluation</div>
    <InputTextWithLabel
      class="mt-8"
      label="Le nom de la période"
      :value="period.name"
      @save="savePeriodName"
    />
    <InputDateWithLabel
      class="mt-8"
      label="Le début"
      :value="period.start"
      @save="savePeriodStart"
    />
    <InputDateWithLabel
      class="mt-8"
      label="La fin"
      :value="period.end"
      @save="savePeriodEnd"
    />
  </div>
  <div class="mt-12">
    <div class="flex flex-row items-center space-x-2 button-minor-action">
      <button @click="deletePeriod">
        <IconTrash class="h-4" />
      </button>
      <button @click="deletePeriod">Supprimer cette période</button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";
import InputDateWithLabel from "../components/InputDateWithLabel.vue";
import IconTrash from "../icons/IconTrash.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const period = computed(() => store.getters.periodById(route.params.periodId));

const savePeriodName = async (value) => {
  const id = Number(route.params.periodId);
  await store.dispatch("updatePeriod", {
    id: id,
    start: period.value.start,
    end: period.value.end,
    name: value,
  });
};

const savePeriodStart = async (value) => {
  const id = Number(route.params.periodId);
  await store.dispatch("updatePeriod", {
    id: id,
    start: value,
    end: period.value.end,
    name: period.value.name,
  });
};

const savePeriodEnd = async (value) => {
  const id = Number(route.params.periodId);
  await store.dispatch("updatePeriod", {
    id: id,
    start: period.value.start,
    end: value,
    name: period.value.name,
  });
};

const deletePeriod = async () => {
  const id = Number(route.params.periodId);
  await store.dispatch("updatePeriodActive", { id: id, active: false });
  router.push("/settings/periods");
};
</script>
