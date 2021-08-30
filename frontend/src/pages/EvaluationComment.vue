<template>
  <div class="my-4 px-2">
    <Disclosure>
      <DisclosureButton class="">
        <div class="flex flex-row items-center space-x-2">
          <div class="form-label">Commentaires généraux</div>
          <IconQuestionMark class="w-6 h-6 text-gray-500" />
        </div>
      </DisclosureButton>
      <DisclosurePanel class="py-2">
        <MascotteTip class="my-2">
          <template v-slot:title>
            Bienvenue sur la page des commentaires ! 🧐
          </template>
          <template v-slot:default>
            <div class="mt-4">
              Il s'agit du commentaire final de l'évaluation.
              <span class="text-xs">
                (Il apparaîtra dans le rapport sur sa propre page, après le
                tableau des évaluations...)
              </span>
            </div>
            <div class="mt-4">
              C'est un texte libre qui peut parler, par exemple, de :
              <ul class="list-disc list-inside">
                <li class="mt-1">
                  L'engagement, l'implication dans le groupe et le
                  fonctionnement de l'école
                </li>
                <li>Le rapport aux apprentissages</li>
                <li>Le rapport aux autres</li>
                <li>Les intérêts, les projets de l'élève</li>
                <li>Les forces et les difficultés de l'élève</li>
              </ul>
            </div>
            <div class="mt-4">
              Et maintenant, votre mission, si vous l'acceptez, écrivez ! ✍️
              <span class="text-xs">(Quelques lignes suffiront...)</span>
            </div>
          </template>
        </MascotteTip>
      </DisclosurePanel>
    </Disclosure>
    <div class="">
      <div v-for="student in students" class="mt-14">
        <div class="form-label">
          {{ student.firstname }}
          {{ student.lastname }}
        </div>
        <div class="mt-2">
          <div v-if="editByStudent[student.id]">
            <div>
              <textarea
                v-model="textByStudent[student.id]"
                class="input w-full"
                rows="5"
              />
            </div>
            <div class="mt-8">
              <button
                @click="saveCommentByStudent[student.id]"
                class="button-main-action"
              >
                Enregistrer
              </button>
            </div>
          </div>
          <div v-else>
            <div class="flex flex-row items-center space-x-2">
              <div class="form-sub-label">Commentaire</div>
              <button @click="editByStudent[student.id] = true">
                <IconPencil class="h-4 text-gray-600 hover:text-teal-500" />
              </button>
            </div>
            <div class="font-serif">
              {{ commentByStudent[student.id].text }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-20 flex flex-row justify-center space-x-4">
      <router-link
        :to="previousCompetency"
        class="
          border border-gray-300
          rounded-md
          shadow-md
          hover:text-teal-500 hover:border-teal-500
        "
      >
        <IconChevronLeft class="h-8" />
      </router-link>
      <router-link
        :to="`/evaluations-by-cycle/${route.params.cycle}`"
        class="
          border border-gray-300
          rounded-md
          shadow-md
          hover:text-teal-500 hover:border-teal-500
        "
      >
        <IconChevronUp class="h-8" />
      </router-link>
      <router-link
        :to="`/evaluations-by-cycle/${route.params.cycle}`"
        class="
          border border-gray-300
          rounded-md
          shadow-md
          hover:text-teal-500 hover:border-teal-500
        "
      >
        <IconChevronRight class="h-8" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { until } from "@vueuse/core";
import { today } from "../utils/date";
import MascotteTip from "../components/MascotteTip.vue";
import IconQuestionMark from "../icons/IconQuestionMark.vue";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";
import IconChevronUp from "../icons/IconChevronUp.vue";
import IconPencil from "../icons/IconPencil.vue";
import { useTitle } from "@vueuse/core";

useTitle("Commentaires généraux - soklaki.fr");

const store = useStore();
const route = useRoute();

const studentById = computed(() => store.getters.studentById);
const students = computed(() => {
  if (store.state.currentPeriod == null) {
    return [];
  }
  const period = store.state.periods[store.state.currentPeriod];
  const full = period.students.map((x) => studentById.value(x.student.id));
  return full.filter(
    (x) => x.current_cycle.current_cycle === route.params.cycle
  );
});

const previousCompetency = computed(() => {
  const competencies = Object.keys(store.state.stats[route.params.cycle].stats);
  if (competencies.length === 0) {
    return "";
  } else {
    const last = competencies[competencies.length - 1];
    return `/evaluation/${route.params.cycle}/${last}`;
  }
});

const editByStudent = ref({});
const textByStudent = ref({});
watch(students, () => {
  for (const student of students.value) {
    editByStudent.value[student.id] = true;
    if (!(student.id in textByStudent.value)) {
      textByStudent.value[student.id] = null;
    }
  }
});

const commentByStudent = computed(() => {
  const comments = {};
  for (const student of students.value) {
    const filtered = Object.values(store.state.comments.store).filter(
      (c) => c.student_id === student.id
    );
    if (filtered.length > 0) {
      const comment = filtered[0];
      comments[student.id] = {
        id: comment.id,
        text: comment.text,
      };
      textByStudent.value[student.id] = comment.text;
    } else {
      comments[student.id] = { id: null, text: null };
    }
  }
  return comments;
});

const saveCommentByStudent = computed(() => {
  const handlers = {};
  for (const student of students.value) {
    handlers[student.id] = async () => {
      const comment = commentByStudent.value[student.id];
      let text = textByStudent.value[student.id];
      text = text == null ? "" : text;
      if (comment.id == null) {
        await store.dispatch("insertComment", {
          studentId: student.id,
          periodId: store.state.currentPeriod,
          date: today(),
          text: text,
        });
      } else {
        await store.dispatch("updateComment", {
          id: comment.id,
          text: text,
          date: today(),
          periodId: store.state.currentPeriod,
        });
      }
      editByStudent.value[student.id] = false;
      textByStudent.value[student.id] = text;
    };
  }
  return handlers;
});

onMounted(async () => {
  await until(() => store.state.currentPeriod).not.toBeNull();
  await store.dispatch("evaluations", {
    periodId: store.state.currentPeriod,
  });
  for (const student of students.value) {
    editByStudent.value[student.id] = true;
    textByStudent.value[student.id] = commentByStudent.value[student.id].text;
  }
});
</script>
