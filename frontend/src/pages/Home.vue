<template>
  <!-- error panel from right -->
  <div class="relative">
    <div
      v-if="inError"
      class="w-5/6 absolute top-0 right-0 bg-red-700 min-h-screen max-w-screen-sm z-50"
    >
      <div>
        <div class="flex flex-col px-1 text-white py-4">
          <div class="font-bold text-xl">
            Une erreur est survenue et j'en suis bien désolé 😭
          </div>
          <div class="mt-2">
            Vous pouvez copier-coller tout ce qui s'affiche en dessous de ce
            message et me l'envoyer par mail ?
          </div>
          <div>Merci 🙏</div>
          <div
            class="mt-8 whitespace-pre font-serif bg-red-500 px-1 w-10/12 h-48 overflow-y-scroll overflow-x-scroll"
          >
            {{ errorMessage }}
          </div>
          <div class="mt-8 self-center">
            <a
              :href="`mailto:olivier@kreako.fr?subject=${encodeURIComponent(
                '[Soklaki] error'
              )}&body=${encodeURIComponent(errorMessage)}`"
              class="bg-white hover:bg-red-200 text-red-700 hover:text-red-900 font-bold px-4 py-2 rounded-md shadow-sm"
            >
              Envoyez-moi un mail !
            </a>
          </div>
          <div class="mt-8 self-center">
            <button
              @click="clearError"
              class="bg-white hover:bg-red-200 text-red-700 hover:text-red-900 font-bold px-4 py-2 rounded-md shadow-sm"
            >
              Fermez cette abomination
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Menu panel on left -->
  <div class="relative">
    <div v-if="showMobileMenu" class="w-4/5 absolute top-0 left-0 z-50">
      <MainMenu :mobile="true" @close="showMobileMenu = false" />
    </div>
  </div>
  <div class="flex flex-col">
    <div
      class="flex flex-row items-center mt-2 mx-2 p-2 border border-gray-300 rounded-md justify-between md:hidden"
    >
      <button @click="showMobileMenu = !showMobileMenu">
        <IconMenu class="h-10 text-gray-600 hover:text-teal-500" />
      </button>
      <router-link
        to="/new-observation"
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

    <div class="flex flex-row">
      <div class="hidden md:block md:w-1/5">
        <MainMenu :mobile="false" />
      </div>
      <div class="mb-20 flex-grow md:ml-4 md:max-w-screen-md">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { useRouter, onBeforeRouteUpdate } from "vue-router";
import Mascotte from "../components/Mascotte.vue";
import MainMenu from "../components/MainMenu.vue";
import IconMenu from "../icons/IconMenu.vue";
import IconPlus from "../icons/IconPlus.vue";

const store = useStore();
const router = useRouter();

const token = computed(() => store.state.login.token);
const students = computed(() => store.state.students);
const socle = computed(() => store.state.socle);

const currentUser = computed(() => {
  if (store.state.login.userId in store.state.users) {
    return store.state.users[store.state.login.userId];
  }
  // Fake
  return {
    email: null,
    firstname: null,
    lastname: null,
    manager: false,
  };
});

const inError = computed(() => store.state.error.inError);
const errorMessage = computed(() => store.state.error.message);
const clearError = () => {
  store.dispatch("clearError");
};

const showMobileMenu = ref(false);
onBeforeRouteUpdate((updateGuard) => {
  // Close the menu on navigation
  showMobileMenu.value = false;
});

onMounted(async () => {
  if (token.value == null) {
    router.push("/login");
  }
  await store.dispatch("boot");
  await store.dispatch("socle");
  // First steps conditions
  // TODO : maybe refine socle conditions (take in account the rest...)
  if (
    store.state.currentPeriod == null ||
    store.state.group.name == null ||
    currentUser.value.firstname == null ||
    currentUser.value.lastname == null ||
    Object.keys(store.state.socle.containers).length === 0
  ) {
    // TODO email confirmed
    router.push("/first-step");
  }
});
</script>
