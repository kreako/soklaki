<template>
  <div
    v-if="selectedParent"
    @click="selectedParent = null"
    class="cursor-pointer hover:text-teal-500 mb-4"
  >
    {{ containerById(selectedParent).full_rank }}
    {{ containerById(selectedParent).text }}
  </div>
  <div v-for="item in list" :class="selectedParent == null ? '' : 'pl-2'">
    <div
      @click="selectContainer(item.id)"
      class="cursor-pointer hover:text-teal-500"
      :class="selectedContainer == item.id ? 'font-bold' : ''"
    >
      {{ containerById(item.id).full_rank }}
      {{ containerById(item.id).text }}
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { defineProps, defineEmit, computed, ref } from "vue";

const store = useStore();

const containerById = computed(() => store.getters.containerById);

const props = defineProps({
  cycle: String,
});

const emit = defineEmit(["selected"]);

const selectedParent = ref(null);
const selectedContainer = ref(null);

const list = computed(() => {
  if (selectedParent.value == null) {
    return store.state.socle[props.cycle];
  } else {
    const parent = store.state.socle[props.cycle].find(
      (x) => x.id == selectedParent.value
    );
    return parent.children;
  }
});

const selectContainer = (id) => {
  if (selectedParent.value == null) {
    const c = store.state.socle[props.cycle].find((x) => x.id == id);
    if (c.children.length == 0) {
      selectedContainer.value = id;
      emit("selected", id);
    } else {
      selectedParent.value = id;
    }
  } else {
    selectedContainer.value = id;
    emit("selected", id);
  }
};
</script>
