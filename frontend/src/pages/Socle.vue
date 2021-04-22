<template>
  <div class="my-4 px-2">
    <div class="form-label text-xl">Socle - cycle 1</div>
    <div class="mt-4">
      <SocleDisplay :socle="socle" cycle="c1" />
    </div>
    <div class="form-label text-xl mt-20">Socle - cycle 2</div>
    <div class="mt-4">
      <SocleDisplay :socle="socle" cycle="c2" />
    </div>
    <div class="form-label text-xl mt-20">Socle - cycle 3</div>
    <div class="mt-4">
      <SocleDisplay :socle="socle" cycle="c3" />
    </div>
    <div class="form-label text-xl mt-20">Socle - cycle 4</div>
    <div class="mt-4">
      <SocleDisplay :socle="socle" cycle="c4" />
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import SocleDisplay from "../components/SocleDisplay.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const socle = computed(() => store.state.socle);
</script>
