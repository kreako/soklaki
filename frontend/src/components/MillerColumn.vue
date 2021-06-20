<template>
  <div class="flex flex-row">
    <div class="flex flex-col" v-if="!hide">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">
        {{ title }}
      </div>
      <hr class="bg-gray-700" />
      <div class="mt-2">
        <div v-for="item in list" :key="item.id">
          <div
            class="cursor-pointer group flex flex-row space-x-2 items-center"
          >
            <div @click="selectLabel(item.id)" class="hover:text-teal-500">
              <slot :item="item"></slot>
            </div>
            <IconPencil
              v-if="editable"
              @click="edit(item.id)"
              class="h-3 hidden group-hover:block hover:text-teal-500"
            />
            <IconTrash
              v-if="editable"
              @click="trash(item.id)"
              class="h-3 hidden group-hover:block hover:text-teal-500"
            />
            <IconChevronUp
              v-if="editable"
              @click="moveUp(item.id)"
              class="h-3 hidden group-hover:block hover:text-teal-500 handle"
            />
            <IconChevronDown
              v-if="editable"
              @click="moveDown(item.id)"
              class="h-3 hidden group-hover:block hover:text-teal-500 handle"
            />
            <IconUpload
              v-if="editable"
              @click="move(item.id)"
              class="h-3 hidden group-hover:block hover:text-teal-500 handle"
            />
          </div>
        </div>
      </div>
      <div v-if="editable" class="mt-2">
        <button
          @click="addItem"
          class="
            mt-2
            rounded-md
            px-3
            border border-teal-700
            hover:border-teal-300
          "
        >
          {{ addLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, computed, ref } from "vue";
import IconPencil from "../icons/IconPencil.vue";
import IconTrash from "../icons/IconTrash.vue";
import IconChevronUp from "../icons/IconChevronUp.vue";
import IconChevronDown from "../icons/IconChevronDown.vue";
import IconUpload from "../icons/IconUpload.vue";

const props = defineProps({
  title: String,
  list: Array,
  hide: Boolean,
  editable: {
    type: Boolean,
    default: true,
  },
  addLabel: {
    type: String,
    default: "Ajouter",
  },
});

const emit = defineEmit([
  "selected",
  "edit",
  "trash",
  "moveUp",
  "moveDown",
  "move",
  "add",
]);

const selectLabel = (id) => {
  emit("selected", id);
};

const edit = (id) => {
  emit("edit", id);
};

const trash = (id) => {
  emit("trash", id);
};

const moveUp = (id) => {
  emit("moveUp", id);
};

const moveDown = (id) => {
  emit("moveDown", id);
};

const move = (id) => {
  emit("move", id);
};

const addItem = () => {
  emit("add");
};
</script>
