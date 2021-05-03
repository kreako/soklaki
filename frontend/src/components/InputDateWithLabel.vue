<template>
  <div>
    <div class="flex flex-row items-center space-x-2">
      <div class="form-sub-label">{{ label }}</div>
      <button v-if="inEdit || props.edit" @click="save">
        <IconCheck class="h-4 text-gray-600 hover:text-teal-500" />
      </button>
      <button v-else @click="goInEdit">
        <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
      </button>
    </div>
    <div v-if="inEdit || props.edit">
      <DatePicker :value="text" @selected="dateSelected" class="mt-2" />
      <div class="mt-2 flex flex-row items-center">
        <input
          type="text"
          v-model="text"
          @keyup.enter="save"
          class="input w-full"
        />
        <button
          v-if="nullable === true"
          @click="selectNull"
          class="ml-2 text-gray-700"
        >
          <IconBackSpace class="h-6" />
        </button>
      </div>
      <div class="flex flex-row space-x-2 items-center mt-2">
        <button @click="cancel" class="button-minor-action flex-grow-0">
          Annuler
        </button>
        <button @click="save" class="button-main-action flex-grow">
          Sauvegarder
        </button>
      </div>
    </div>
    <div v-else class="font-serif whitespace-pre">{{ value }}</div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref } from "vue";
import IconCheck from "../icons/IconCheck.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconBackSpace from "../icons/IconBackSpace.vue";
import DatePicker from "../components/DatePicker.vue";

const props = defineProps({
  label: String,
  value: String,
  edit: {
    type: Boolean,
    default: false,
  },
  nullable: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmit(["save", "cancel"]);

const inEdit = ref(false);
const text = ref("");
const save = () => {
  emit("save", text.value);
  inEdit.value = false;
};
const cancel = () => {
  emit("cancel");
  inEdit.value = false;
};
const goInEdit = () => {
  text.value = props.value;
  inEdit.value = true;
};
const dateSelected = (value) => {
  text.value = value;
};
const selectNull = () => {
  text.value = null;
};
</script>
