<template>
  <div class="my-4 px-2">
    <div class="form-label">Mon équipe</div>
    <div class="mt-12">
      <div v-for="user in users" class="mt-4">
        <div class="flex flex-row items-center space-x-4">
          <div>{{ user.firstname }} {{ user.lastname }}</div>
          <div class="text-xs rounded-full px-1 border border-gray-600">
            {{ userInitials(user) }}
          </div>
          <button
            v-if="user.id !== currentUserId"
            @click="removeUser(user.id)"
            class="text-gray-500 hover:text-teal-500"
          >
            <IconTrash class="w-4" />
          </button>
        </div>
        <div class="pl-2 text-sm text-gray-700">
          {{ user.email }}
        </div>
      </div>
    </div>
    <ModalConfirmCancel
      title="Confirmation"
      :show="showRemoveUserModal"
      @confirm="confirmRemoveUser"
      @cancel="cancelRemoveUser"
    >
      <div>
        Êtes-vous sûr de vouloir supprimer l'utilisateur
        {{ userById(selectedUserId).firstname }}
        {{ userById(selectedUserId).lastname }} ?
      </div>
    </ModalConfirmCancel>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { userInitials } from "../utils/user";
import IconTrash from "../icons/IconTrash.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";

const store = useStore();

const users = computed(() => store.state.users);

const currentUserId = computed(() => store.state.login.userId);

const userById = computed(() => store.getters.userById);
const showRemoveUserModal = ref(false);
const selectedUserId = ref(null);
const removeUser = (userId) => {
  selectedUserId.value = userId;
  showRemoveUserModal.value = true;
};
const cancelRemoveUser = () => {
  selectedUserId.value = null;
  showRemoveUserModal.value = false;
};
const confirmRemoveUser = async () => {
  await store.dispatch("updateUserActive", {
    id: selectedUserId.value,
    active: false,
  });
  selectedUserId.value = null;
  showRemoveUserModal.value = false;
};
</script>
