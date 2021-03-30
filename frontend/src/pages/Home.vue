<template>
  <div class="relative">
    <div
      v-if="showMobileMenu"
      class="w-4/5 absolute top-0 left-0 bg-teal-700 h-screen"
    >
      <div class="flex flex-row">
        <div
          class="flex-grow flex flex-col px-4 text-white font-bold text-xl space-y-4 py-4"
        >
          <div>
            <router-link to="/"> Accueil </router-link>
          </div>
          <div>Observations</div>
          <div>Élèves</div>
          <div>Rapports</div>
          <div>Socle</div>
          <div>Réglages</div>
          <div>Aide</div>
        </div>
        <div class="flex-grow-0">
          <button @click="showMobileMenu = false">
            <IconX class="text-white w-12" />
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="flex flex-col">
    <div
      class="flex flex-row items-center mt-2 mx-2 p-2 border border-gray-300 rounded-md justify-between"
    >
      <button @click="showMobileMenu = !showMobileMenu">
        <IconMenu class="h-10 text-gray-600 hover:text-teal-500" />
      </button>
      <router-link
        to="new-observation"
        class="bg-teal-700 font-bold px-3 py-1 text-white rounded-md"
      >
        <div class="flex flex-row space-x-4">
          <IconPlus class="h-6" />
          <div>Nouvelle observation</div>
        </div>
      </router-link>
      <div class="flex flex-row h-full items-center mr-2">
        <Mascotte class="h-6" />
      </div>
    </div>

    <div class>
      <router-view></router-view>
      <!--
      <NewObservation :students="students" :socle="socle" />

        -->
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRouter, onBeforeRouteUpdate } from "vue-router";
import NewObservation from "../components/NewObservation.vue";
import Mascotte from "../components/Mascotte.vue";
import IconMenu from "../icons/IconMenu.vue";
import IconPlus from "../icons/IconPlus.vue";
import IconX from "../icons/IconX.vue";

const store = useStore();
const router = useRouter();

const token = computed(() => store.state.login.token);
const students = computed(() => store.state.students);
const socle = computed(() => store.state.socle);

const showMobileMenu = ref(false);

onBeforeRouteUpdate((updateGuard) => {
  // Close the menu on navigation
  showMobileMenu.value = false;
});

onMounted(() => {
  if (token.value == null) {
    router.push("/login");
  }
  store.dispatch("students");
  store.dispatch("socle");
});
</script>
