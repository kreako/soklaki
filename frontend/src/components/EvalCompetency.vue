<template>
  <div>
    <div v-if="inEdit || props.edit">
      <div class="mt-2">
        <textarea v-model="commentText" class="mt-2 input w-full" rows="2" />
      </div>
      <div class="flex flex-row space-x-1 items-center mt-2">
        <button
          @click="cancel"
          class="flex-grow-0 rounded-md py-1 shadow-sm border border-gray-300 hover:border-gray-500 text-gray-600 hover:text-gray-800 text-xs"
        >
          Annuler
        </button>
        <button
          v-if="status === 'NotAcquired'"
          @click="save('NotAcquired')"
          class="rounded-md px-1 py-1 shadow-sm border bg-teal-700 font-bold text-white border-teal-700 hover:text-teal-200 hover:border-teal-200 focus:text-teal-200 focus:border-teal-200 text-sm"
        >
          Insuffisant
        </button>
        <button
          v-else
          @click="save('NotAcquired')"
          class="rounded-md px-1 py-1 shadow-sm border border-teal-700 hover:text-teal-500 hover:border-teal-500 focus:text-teal-500 focus:border-teal-500 text-sm"
        >
          Insuffisant
        </button>

        <button
          v-if="status === 'InProgress'"
          @click="save('InProgress')"
          class="rounded-md px-1 py-1 shadow-sm border bg-teal-700 font-bold text-white border-teal-700 hover:text-teal-200 hover:border-teal-200 focus:text-teal-200 focus:border-teal-200 text-sm"
        >
          Fragile
        </button>
        <button
          v-else
          @click="save('InProgress')"
          class="rounded-md px-1 py-1 shadow-sm border border-teal-700 hover:text-teal-500 hover:border-teal-500 focus:text-teal-500 focus:border-teal-500 text-sm"
        >
          Fragile
        </button>

        <button
          v-if="status === 'Acquired'"
          @click="save('Acquired')"
          class="rounded-md px-1 py-1 shadow-sm border bg-teal-700 font-bold text-white border-teal-700 hover:text-teal-200 hover:border-teal-200 focus:text-teal-200 focus:border-teal-200 text-sm"
        >
          Satisfaisant
        </button>
        <button
          v-else
          @click="save('Acquired')"
          class="rounded-md px-1 py-1 shadow-sm border border-teal-700 hover:text-teal-500 hover:border-teal-500 focus:text-teal-500 focus:border-teal-500 text-sm"
        >
          Satisfaisant
        </button>

        <button
          v-if="status === 'TipTop'"
          @click="save('TipTop')"
          class="rounded-md px-1 py-1 shadow-sm border bg-teal-700 font-bold text-white border-teal-700 hover:text-teal-200 hover:border-teal-200 focus:text-teal-200 focus:border-teal-200 text-sm"
        >
          Très&nbsp;bon
        </button>
        <button
          v-else
          @click="save('TipTop')"
          class="rounded-md px-1 py-1 shadow-sm border border-teal-700 hover:text-teal-500 hover:border-teal-500 focus:text-teal-500 focus:border-teal-500 text-sm"
        >
          Très&nbsp;bon
        </button>
      </div>
    </div>
    <div v-else>
      <div class="flex flex-row items-center space-x-2">
        <div class="form-sub-label">Commentaire</div>
        <button @click="goInEdit">
          <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
        </button>
      </div>
      <div class="font-serif">
        <div v-if="comment == null">Sans commentaire</div>
        <div v-else>
          {{ comment }}
        </div>
      </div>
      <div class="flex flex-row items-center space-x-2 mt-2">
        <div class="form-sub-label">Maîtrise</div>
        <button @click="goInEdit">
          <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
        </button>
      </div>
      <div class="font-serif">
        <div v-if="status === 'NotAcquired'">Maîtrise insuffisante</div>
        <div v-else-if="status === 'InProgress'">Maîtrise fragile</div>
        <div v-else-if="status === 'Acquired'">Maîtrise satisfaisante</div>
        <div v-else-if="status === 'TipTop'">Très bonne maîtrise</div>
        <div v-else>Non évalué</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref, watch } from "vue";
import IconCheck from "../icons/IconCheck.vue";
import IconPencil from "../icons/IconPencil.vue";

const props = defineProps({
  comment: String,
  status: String,
  edit: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmit(["save", "cancel"]);

const inEdit = ref(props.edit);
const commentText = ref(props.comment);
const save = (status) => {
  emit("save", { comment: commentText.value, status: status });
  inEdit.value = false;
};
const cancel = () => {
  emit("cancel");
  inEdit.value = false;
};
const goInEdit = () => {
  commentText.value = props.comment;
  inEdit.value = true;
};
watch(props, () => {
  commentText.value = props.comment;
});
</script>
