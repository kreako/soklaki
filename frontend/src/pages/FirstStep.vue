<template>
  <div class="px-2">
    <MascotteTip class="mt-4">
      <template v-slot:title>Encore quelques infos... 🙇</template>
      <template v-slot:default>
        Pour de beaux rapports et pour faciliter les interactions dans votre
        équipe !
      </template>
    </MascotteTip>
    <!-- Group name -->
    <div v-if="groupName == null || groupNameInEdit" class="mt-4">
      <div class="flex flex-row items-center space-x-3">
        <div class="form-label">Le nom de votre école</div>
      </div>
      <div>
        <input
          type="text"
          @keyup.enter="saveGroupName"
          v-model="groupNameEdit"
          class="mt-2 input w-full"
        />
        <button @click="saveGroupName" class="button-main-action mt-2">
          Sauvegarder
        </button>
      </div>
    </div>
    <div v-else class="mt-4">
      <div class="flex flex-row items-center space-x-3">
        <div class="form-label">Le nom de votre école</div>
        <button @click="editGroupName">
          <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
        </button>
      </div>
      <div class="font-serif">{{ groupName }}</div>
    </div>

    <div v-if="currentPeriodId == null">Current period</div>

    <div v-if="currentUser.firstname == null">firstname</div>

    <div v-if="currentUser.lastname == null">lastname</div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import MascotteTip from "../components/MascotteTip.vue";
import IconPencil from "../icons/IconPencil.vue";

const store = useStore();

const currentPeriodId = computed(() => store.state.currentPeriodId);

const groupName = computed(() => store.state.group.name);
const groupNameInEdit = ref(false);
const groupNameEdit = ref("");
const editGroupName = () => {
  groupNameEdit.value = groupName.value;
  groupNameInEdit.value = true;
};
const saveGroupName = async () => {
  await store.dispatch("updateGroupName", {
    groupId: store.state.login.groupId,
    groupName: groupNameEdit.value,
  });
  groupNameInEdit.value = false;
};

const currentUser = computed(() => {
  if (store.state.login.userId in store.state.users) {
    return store.state.users[store.state.login.userId];
  }
  // Fake
  return {
    email: null,
    firstname: null,
    lastname: null,
    manager: false,
  };
});
</script>
