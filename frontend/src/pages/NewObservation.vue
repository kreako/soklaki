<template>
  <div class="mt-4 px-2 w-full">
    <div class="w-full">
      <div class="text-gray-800">Décrivez votre observation</div>
      <textarea v-model="text" class="mt-2 input w-full" rows="8"></textarea>
    </div>
    <div class="mt-8">
      <button @click="save" class="button-main-action">Enregistrer</button>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ref } from "vue";

const router = useRouter();
const store = useStore();
const text = ref("");

const save = async () => {
  let id = await store.dispatch("insertObservation", {
    text: text.value,
  });
  router.push(`/observation/${id}`);
};
</script>
