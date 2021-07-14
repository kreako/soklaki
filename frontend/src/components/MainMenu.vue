<template>
  <div class="bg-gray-50 h-screen">
    <div class="flex flex-row">
      <div class="flex-grow flex flex-col py-4">
        <div class="px-4 flex flex-col space-y-4">
          <div v-if="!mobile" class="flex flex-row items-center space-x-2 mb-4">
            <div class="self-left">
              <div
                class="
                  rounded-full
                  h-10
                  w-10
                  bg-white
                  flex flex-row
                  justify-center
                  p-1
                "
              >
                <Mascotte class="h-8" />
              </div>
            </div>
            <div class="font-bold text-pink-500 text-xs">Soklaki</div>
          </div>
          <div class="flex-grow flex flex-col text-gray-900 py-4 space-y-2">
            <router-link to="/">
              <div class="group flex flex-row items-center space-x-2">
                <IconHome class="w-4 text-gray-400 group-hover:text-teal-500" />
                <div class="group-hover:text-teal-500">Accueil</div>
              </div>
            </router-link>
            <div>
              <router-link to="/observations">
                <div class="group flex flex-row items-center space-x-2">
                  <IconEye
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Observations</div>
                </div>
              </router-link>
              <div v-if="!mobile" class="pl-2 self-start">
                <div></div>
                <router-link to="/new-observation">
                  <div class="group">
                    <div class="flex flex-row space-x-2 items-center">
                      <IconPlus
                        class="w-4 text-gray-400 group-hover:text-teal-500"
                      />
                      <div class="group-hover:text-teal-500">
                        Nouvelle observation
                      </div>
                    </div>
                  </div>
                </router-link>
              </div>
            </div>
            <div class="hover:text-teal-500">
              <router-link to="/evaluations">
                <div class="group flex flex-row items-center space-x-2">
                  <IconAnnotation
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Évaluations</div>
                </div>
              </router-link>
            </div>
            <div class="hover:text-teal-500">
              <router-link to="/students">
                <div class="group flex flex-row items-center space-x-2">
                  <IconUser
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Élèves</div>
                </div>
              </router-link>
            </div>
            <div class="hover:text-teal-500">
              <router-link to="/reports">
                <div class="group flex flex-row items-center space-x-2">
                  <IconDocumentReport
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Rapports</div>
                </div>
              </router-link>
            </div>
            <div class="hover:text-teal-500">
              <router-link to="/settings">
                <div class="group flex flex-row items-center space-x-2">
                  <IconCog
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Réglages</div>
                </div>
              </router-link>
            </div>
            <div class="hover:text-teal-500">
              <router-link to="/">
                <div class="group flex flex-row items-center space-x-2">
                  <IconSupport
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Aide</div>
                </div>
              </router-link>
            </div>
            <div>
              <button @click="logout">
                <div class="group flex flex-row items-center space-x-2">
                  <IconLogout
                    class="w-4 text-gray-400 group-hover:text-teal-500"
                  />
                  <div class="group-hover:text-teal-500">Déconnexion</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="mobile" class="flex-grow-0">
        <button @click="$emit('close')">
          <IconX class="text-gray-900 w-12" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmit } from "vue";
import IconX from "../icons/IconX.vue";
import IconHome from "../icons/IconHome.vue";
import IconEye from "../icons/IconEye.vue";
import IconAnnotation from "../icons/IconAnnotation.vue";
import IconUser from "../icons/IconUser.vue";
import IconDocumentReport from "../icons/IconDocumentReport.vue";
import IconCog from "../icons/IconCog.vue";
import IconSupport from "../icons/IconSupport.vue";
import IconPlus from "../icons/IconPlus.vue";
import IconLogout from "../icons/IconLogout.vue";
import Mascotte from "./Mascotte.vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();

const props = defineProps({
  mobile: Boolean,
});

defineEmit(["close"]);

const logout = async () => {
  await store.dispatch("logout");
  router.push("/login");
};
</script>
