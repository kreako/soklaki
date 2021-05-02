<template>
  <div class="px-2">
    <MascotteTip class="mt-4">
      <template v-slot:title>Encore quelques infos... 🙇</template>
      <template v-slot:default>
        C'est pour commencer, rien de définitif, tout sera modifiable dans la
        partie <span class="font-mono">Réglages</span>.
      </template>
    </MascotteTip>
    <div class="mt-8 form-label">Nos premiers pas ensemble...</div>
    <!-- Group name -->
    <InputTextWithLabel
      class="mt-8"
      label="Le nom de votre école"
      :value="groupName"
      @save="saveGroupName"
    />

    <!-- period -->
    <div v-if="sortedPeriods.length == 0" class="mt-4">
      <div class="form-sub-label">Une période d'évaluation</div>
      <div class="mt-2 form-sub-label">Son petit nom</div>
      <div>
        <input type="text" v-model="periodNameEdit" class="mt-2 input w-full" />
      </div>
      <div class="mt-2 form-sub-label">La date de départ</div>
      <div>
        <input
          type="text"
          v-model="periodStartEdit"
          @focus="periodStartFocus = true"
          @blur="periodStartFocus = false"
          class="mt-2 input w-full"
        />
        <div
          v-if="!periodStartFocus && periodStartError != null"
          class="whitespace-pre-line text-red-500 text-sm"
        >
          {{ periodStartError }}
        </div>
      </div>
      <div class="mt-2 form-sub-label">La date d'arrivée</div>
      <div>
        <input
          type="text"
          v-model="periodEndEdit"
          class="mt-2 input w-full"
          :class="periodEndError != null ? 'input-error' : ''"
          @focus="periodEndFocus = true"
          @blur="periodEndFocus = false"
        />
        <div
          v-if="!periodEndFocus && periodEndError != null"
          class="whitespace-pre-line text-red-500 text-sm"
        >
          {{ periodEndError }}
        </div>
      </div>
      <div>
        <div
          v-if="periodDateError != null"
          class="whitespace-pre-line text-red-500 text-sm"
        >
          {{ periodDateError }}
        </div>
        <button
          @click="savePeriod"
          class="button-main-action mt-2"
          :disabled="!periodDateValid"
        >
          Sauvegarder
        </button>
      </div>
    </div>
    <div v-else class="mt-8">
      <div class="form-sub-label">Une période d'évaluation</div>
      <div class="font-serif">
        {{ period0.name }}
      </div>
      <div class="flex flex-row space-x-2 font-serif">
        <div>
          {{ period0.start }}
        </div>
        <div class="text-gray-500">➡</div>
        <div>
          {{ period0.end }}
        </div>
      </div>
    </div>

    <!-- Firstname and lastname -->

    <InputTextWithLabel
      class="mt-8"
      label="Votre prénom"
      :value="currentUser.firstname"
      @save="saveUserFirstname"
    />
    <InputTextWithLabel
      class="mt-8"
      label="Votre nom"
      :value="currentUser.lastname"
      @save="saveUserLastname"
    />
    <div class="mt-8">
      <div class="form-sub-label">La génération du socle</div>
      <div v-if="!socleValid" class="font-serif text-red-500">En cours...</div>
      <div v-else class="flex flex-row items-center">
        <div class="font-serif">Fait !</div>
        <IconCheck class="h-4 text-green-500" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { dateJsObj } from "../utils/date";
import MascotteTip from "../components/MascotteTip.vue";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";

const store = useStore();
const router = useRouter();

const groupName = computed(() => store.state.group.name);
const saveGroupName = async (value) => {
  await store.dispatch("updateGroupName", {
    groupId: store.state.login.groupId,
    groupName: value,
  });
  checkEnd();
};

// const periods = computed(() => store.state.periods);
const sortedPeriods = computed(() => store.state.sortedPeriods);
const periodNameDefault = () => {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = month < 8 ? today.getFullYear() - 1 : today.getFullYear();
  return `${year}/${year + 1}`;
};
const periodNameEdit = ref(periodNameDefault());
const periodStartDefault = () => {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = month < 8 ? today.getFullYear() - 1 : today.getFullYear();
  return `${year}-09-01`;
};
const periodStartEdit = ref(periodStartDefault());
const periodStartFocus = ref(false);
const periodEndDefault = () => {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = month < 8 ? today.getFullYear() : today.getFullYear() + 1;
  return `${year}-06-30`;
};
const periodEndEdit = ref(periodEndDefault());
const periodEndFocus = ref(false);
const periodStartError = computed(() => {
  if (periodStartEdit.value === "") {
    // Not yet filled
    return null;
  }
  try {
    const start = dateJsObj(periodStartEdit.value);
    return null;
  } catch (error) {
    return error.message;
  }
});
const periodEndError = computed(() => {
  if (periodEndEdit.value === "") {
    // Not yet filled
    return null;
  }
  try {
    const end = dateJsObj(periodEndEdit.value);
    return null;
  } catch (error) {
    return error.message;
  }
});
const periodDateValid = computed(() => {
  if (
    periodStartEdit.value === "" ||
    periodEndEdit.value === "" ||
    periodNameEdit.value === ""
  ) {
    return false;
  }
  if (periodStartError.value != null || periodEndError.value != null) {
    return false;
  }
  if (periodDateError.value != null) {
    return false;
  }
  return true;
});
const periodDateError = computed(() => {
  if (
    periodStartEdit.value === "" ||
    periodEndEdit.value === "" ||
    periodNameEdit.value === ""
  ) {
    // Not ready
    return null;
  }
  if (periodStartError.value != null || periodEndError.value != null) {
    // Individual errors, do not loose my time here
    return null;
  }
  try {
    const start = dateJsObj(periodStartEdit.value).valueOf();
    const end = dateJsObj(periodEndEdit.value).valueOf();
    if (start >= end) {
      return `J'ai l'impression que la date de départ '${periodStartEdit.value}' est
      après la date d'arrivée '${periodEndEdit.value}'. \n
      Ça me chagrine beaucoup !`;
    }
    return null;
  } catch (error) {
    return error.message;
  }
});
const savePeriod = async () => {
  await store.dispatch("insertPeriod", {
    groupId: store.state.login.groupId,
    name: periodNameEdit.value,
    start: periodStartEdit.value,
    end: periodEndEdit.value,
  });
  checkEnd();
};
const period0 = computed(() => {
  if (store.state.sortedPeriods.length > 0) {
    return store.state.periods[store.state.sortedPeriods[0]];
  }
  return null;
});

const currentUser = computed(() =>
  store.getters.userById(store.state.login.userId)
);
const saveUserFirstname = async (value) => {
  await store.dispatch("saveUserName", {
    userId: store.state.login.userId,
    firstname: value,
    lastname: currentUser.value.lastname,
  });
  checkEnd();
};
const saveUserLastname = async (value) => {
  await store.dispatch("saveUserName", {
    userId: store.state.login.userId,
    firstname: currentUser.value.firstname,
    lastname: value,
  });
  checkEnd();
};

const socleValid = computed(
  () => Object.keys(store.state.socle.containers).length !== 0
);

const checkEnd = () => {
  const periods = store.state.periods;
  const group = store.state.group;
  const users = store.state.users;
  if (periods.length === 0) {
    return;
  }
  if (group.name == null) {
    return;
  }
  const userId = store.state.login.userId;
  if (!(userId in users)) {
    return;
  }
  const firstname = users[userId].firstname;
  if (firstname == null) {
    return;
  }
  const lastname = users[userId].lastname;
  if (lastname == null) {
    return;
  }
  if (!socleValid.value) {
    return;
  }
  // router.push("/");
};

onMounted(async () => {
  console.log("onMounted 1");
  if (!socleValid.value) {
    console.log("onMounted 2");
    await store.dispatch("loadSocle");
    console.log("onMounted 3");
  }
  console.log("onMounted 4");
});
</script>
