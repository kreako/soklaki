<template>
  <div class="flex flex-row">
    <div class="flex flex-col">
      <div>{{ title }} {{ list.length }}</div>
      <div>
        <div v-for="(item, index) in list" class="cursor-pointer">
          <div @click="selectLabel(item.id)">
            <slot name="label" :item="item" :index="index"></slot>
          </div>
        </div>
      </div>
    </div>
    <div>
      <slot name="child"></slot>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref } from "vue";
const props = defineProps({
  title: String,
  list: Array,
});

const emit = defineEmit(["selected"]);

const selectLabel = (id) => {
  emit("selected", id);
};
</script>
