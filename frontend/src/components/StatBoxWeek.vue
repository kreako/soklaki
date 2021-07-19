<template>
  <div
    class="
      bg-gray-800
      h-40
      border-2 border-gray-200
      shadow-2xl
      rounded-xl
      p-2
      relative
    "
  >
    <div
      class="
        absolute
        top-0
        inset-x-0
        text-sm text-white
        font-bold
        flex
        justify-center
      "
    >
      {{ week.week_start }}
    </div>
    <div class="absolute top-8 left-6 right-0 flex flex-col space-y-1">
      <div
        class="
          text-3xl text-teal-500
          flex
          justify-center
          items-center
          space-x-2
        "
      >
        <span>
          {{ week.observations }}
        </span>
        <IconEye class="h-4" />
      </div>
      <div
        class="
          text-3xl text-pink-500
          flex
          justify-center
          items-center
          space-x-2
        "
      >
        <span>
          {{ week.evaluations }}
        </span>
        <IconAnnotation class="h-4" />
      </div>
      <div
        class="
          text-3xl text-gray-200
          flex
          justify-center
          items-center
          space-x-2
        "
      >
        <span>
          {{ week.counts.length }}
        </span>
        <IconUser class="h-4" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import IconUser from "../icons/IconUser.vue";
import IconEye from "../icons/IconEye.vue";
import IconAnnotation from "../icons/IconAnnotation.vue";

const props = defineProps({
  week: Object,
});
</script>
