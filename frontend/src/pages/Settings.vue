<template>
  <div class="my-4 px-2">
    <div class="form-label">Quelques réglages</div>
    <div class="mt-8 flex flex-col space-y-4">
      <div class="flex flex-row space-x-2 items-center group">
        <IconCog class="h-4 text-gray-700 group-hover:text-teal-500" />
        <router-link to="/settings/profile" class="group-hover:text-teal-500">
          Mon profil
        </router-link>
      </div>
      <div class="flex flex-row space-x-2 items-center group">
        <IconCog class="h-4 text-gray-700 group-hover:text-teal-500" />
        <router-link to="/settings/team" class="group-hover:text-teal-500">
          Mon équipe
        </router-link>
      </div>
      <div class="flex flex-row space-x-2 items-center group">
        <IconCog class="h-4 text-gray-700 group-hover:text-teal-500" />
        <router-link to="/settings/periods" class="group-hover:text-teal-500">
          Les périodes d'évaluations
        </router-link>
      </div>
      <div class="flex flex-row space-x-2 items-center group">
        <IconCog class="h-4 text-gray-700 group-hover:text-teal-500" />
        <router-link to="/socle" class="group-hover:text-teal-500">
          Le socle
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import IconCog from "../icons/IconCog.vue";
import { useTitle } from "@vueuse/core";

useTitle("Réglages - soklaki.fr");
</script>
