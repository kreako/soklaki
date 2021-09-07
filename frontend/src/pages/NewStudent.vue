<template>
  <div class="my-4 px-2">
    <div class="form-label">Nouvel élève</div>
    <div class="mt-8">
      <div class="form-sub-label">Prénom</div>
      <input type="text" v-model="firstname" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Nom</div>
      <input type="text" v-model="lastname" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date d'anniversaire</div>
      <DatePicker
        :value="birthdate"
        @selected="birthdate = $event"
        class="mt-2"
      />
      <input type="text" v-model="birthdate" class="mt-2 input w-full" />
      <div
        v-if="!birthdateValid"
        class="
          mt-2
          border border-red-600
          p-2
          whitespace-pre-wrap
          font-mono
          text-red-600
          rounded-md
        "
      >
        <div>
          {{ birthdateFormatMsg }}
        </div>
      </div>
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date d'entrée à l'école</div>
      <DatePicker
        :value="schoolEntry"
        @selected="schoolEntry = $event"
        class="mt-2"
      />
      <input type="text" v-model="schoolEntry" class="mt-2 input w-full" />
      <div
        v-if="!schoolEntryValid"
        class="
          mt-2
          border border-red-600
          p-2
          whitespace-pre-wrap
          font-mono
          text-red-600
          rounded-md
        "
      >
        <div>
          {{ schoolEntryFormatMsg }}
        </div>
      </div>
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date de sortie de l'école</div>
      <DatePicker
        :value="schoolExit"
        @selected="schoolExit = $event"
        class="mt-2"
      />
      <input type="text" v-model="schoolExit" class="mt-2 input w-full" />
      <div
        v-if="!schoolExitValid"
        class="
          mt-2
          border border-red-600
          p-2
          whitespace-pre-wrap
          font-mono
          text-red-600
          rounded-md
        "
      >
        <div>
          {{ schoolExitFormatMsg }}
        </div>
      </div>
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
import { useTitle } from "@vueuse/core";
import { dateJsObj } from "../utils/date";

useTitle("Nouvel élève - soklaki.fr");

const store = useStore();
const router = useRouter();

const firstname = ref("");
const lastname = ref("");
const birthdate = ref("");
const schoolEntry = ref("");
const schoolExit = ref("");

const schoolEntryValid = ref(true);
const schoolExitValid = ref(true);
const birthdateValid = ref(true);

const schoolEntryFormatMsg = ref(true);
const schoolExitFormatMsg = ref(true);
const birthdateFormatMsg = ref(true);

const cancel = () => {
  router.back();
};

const save = async (value) => {
  // Check birthdate format
  try {
    dateJsObj(birthdate.value);
    birthdateValid.value = true;
  } catch (e) {
    birthdateFormatMsg.value = e.message;
    birthdateValid.value = false;
  }
  // Check school entry format
  try {
    dateJsObj(schoolEntry.value);
    schoolEntryValid.value = true;
  } catch (e) {
    schoolEntryFormatMsg.value = e.message;
    schoolEntryValid.value = false;
  }
  // Check school exit format
  try {
    if (schoolExit.value != "") {
      dateJsObj(schoolExit.value);
    }
    schoolExitValid.value = true;
  } catch (e) {
    schoolExitFormatMsg.value = e.message;
    schoolExitValid.value = false;
  }
  if (
    !birthdateValid.value ||
    !schoolEntryValid.value ||
    !schoolExitValid.value
  ) {
    // one of the date is invalid - so do nothing
    return;
  }
  const id = await store.dispatch("insertStudent", {
    birthdate: birthdate.value,
    firstname: firstname.value,
    lastname: lastname.value,
    groupId: store.state.login.groupId,
    schoolEntry: schoolEntry.value,
    schoolExit: schoolExit.value == "" ? null : schoolExit.value,
  });
  router.push(`/student/${id}`);
};
</script>
