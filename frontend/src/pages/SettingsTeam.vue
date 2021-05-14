<template>
  <div class="my-4 px-2">
    <div class="flex flex-row items-center space-x-4">
      <div class="form-label">Mon équipe</div>
      <button @click="openInvitationModal" class="text-gray-700 text-sm">
        Inviter de nouveaux membres
      </button>
    </div>
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
      <div class="mt-12">
        <button @click="openInvitationModal" class="button-minor-action">
          Inviter de nouveaux membres
        </button>
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
    <Modal
      title="Invitation"
      :show="showInvitationModal"
      @close="closeInvitationModal"
    >
      <div>
        Pour inviter de nouveaux membres à participer à l'évaluation du socle,
        envoyez leur le lien d'inscription suivant (bien en entier!) :
      </div>
      <div class="font-mono mt-8 overflow-y-auto">
        {{ invitationLink }}
      </div>
      <div class="mt-8">
        Le lien sera valable pendant les 3 prochains jours (à partir de
        maintenant...)
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { userInitials } from "../utils/user";
import IconTrash from "../icons/IconTrash.vue";
import ModalConfirmCancel from "../components/ModalConfirmCancel.vue";
import Modal from "../components/Modal.vue";

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

const showInvitationModal = ref(false);
const invitationLink = ref("");
const openInvitationModal = async () => {
  const token = await store.dispatch("invitationGenerateToken");
  invitationLink.value = `${window.location.origin}/#/invitation-signup?token=${token}`;
  showInvitationModal.value = true;
};
const closeInvitationModal = () => {
  showInvitationModal.value = false;
};
</script>
