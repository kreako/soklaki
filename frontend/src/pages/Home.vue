<template>
    <div class="flex flex-row">
        <div class="hidden flex-grow-0">
            Accueil
            Observations
            Élèves
            Rapports
            Socle
            Réglages
            Aide
        </div>
        <div class="">
            <NewObservation :students="students" :socle="socle"/>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import NewObservation from '../components/NewObservation.vue'

const store = useStore()
const router = useRouter()

const token = computed(() => store.state.login.token)
const students = computed(() => store.state.students)
const socle = computed(() => store.state.socle)

onMounted(() => {
    if (token.value == null) {
        router.push("/login")
    }
    store.dispatch('students')
    store.dispatch('socle')
})

</script>