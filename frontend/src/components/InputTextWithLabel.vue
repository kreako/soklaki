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
      <input
        type="text"
        v-model="text"
        @keyup.enter="save"
        class="mt-2 input w-full"
      />
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

const props = defineProps({
  label: String,
  value: String,
  edit: {
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
</script>
