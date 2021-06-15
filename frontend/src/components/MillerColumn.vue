<template>
  <div class="flex flex-row">
    <div class="flex flex-col" v-if="!hide">
      <div class="text-sm uppercase text-gray-700 tracking-wider font-semibold">
        {{ title }}
      </div>
      <hr class="bg-gray-700" />
      <div class="mt-2">
        <div v-for="(item, index) in list" class="cursor-pointer">
          <div @click="selectLabel(item.id)">
            <slot :item="item" :index="index"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit, ref } from "vue";
const props = defineProps({
  title: String,
  list: Array,
  hide: Boolean,
});

const emit = defineEmit(["selected"]);

const selectLabel = (id) => {
  emit("selected", id);
};
</script>
