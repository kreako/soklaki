<template>
  <div class="bg-teal-700 h-screen">
    <div class="flex flex-row">
      <div class="flex-grow flex flex-col text-white font-bold text-xl py-4">
        <div class="px-4 flex flex-col space-y-4">
          <div v-if="!mobile" class="self-center mb-4">
            <div
              class="rounded-full h-12 w-12 bg-white flex flex-row justify-center p-1"
            >
              <Mascotte class="h-12" />
            </div>
          </div>
          <div>
            <router-link to="/"> Accueil </router-link>
          </div>
          <div>
            <router-link to="/observations"> Observations </router-link>
          </div>
          <div>Évaluations</div>
          <div><router-link to="/students">Élèves</router-link></div>
          <div>Rapports</div>
          <div>
            <router-link to="/socle">Socle</router-link>
          </div>
          <div>
            <router-link to="/stats">Statistiques</router-link>
          </div>
          <div>Réglages</div>
          <div>Aide</div>
        </div>
        <div v-if="!mobile" class="mt-12 px-1">
          <router-link to="/new-observation">
            <div
              class="bg-white rounded-md text-teal-700 shadow-sm px-2 py-1 text-base"
            >
              <div class="flex flex-row space-x-1 items-center">
                <IconPlus class="h-8" />
                <div>Nouvelle observation</div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
      <div v-if="mobile" class="flex-grow-0">
        <button @click="$emit('close')">
          <IconX class="text-white w-12" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit } from "vue";
import IconX from "../icons/IconX.vue";
import IconPlus from "../icons/IconPlus.vue";
import Mascotte from "./Mascotte.vue";

const props = defineProps({
  mobile: Boolean,
});

defineEmit(["close"]);
</script>
