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
              class="h-3 hidden group-hover:block hover:text-teal-500"
            />
            <IconTrash
              v-if="editable"
              class="h-3 hidden group-hover:block hover:text-teal-500"
            />
            <IconChevronUp
              v-if="editable"
              class="h-3 hidden group-hover:block hover:text-teal-500 handle"
            />
            <IconChevronDown
              v-if="editable"
              class="h-3 hidden group-hover:block hover:text-teal-500 handle"
            />
          </div>
        </div>
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

const props = defineProps({
  title: String,
  list: Array,
  hide: Boolean,
  editable: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmit(["selected"]);

const selectLabel = (id) => {
  emit("selected", id);
};
</script>
