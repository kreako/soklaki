<template>
<router-view>

</router-view>
</template>

<script setup>
import { useStore } from 'vuex'

// Load maybe previously saved login data from the local storage
const store = useStore()
store.commit("loadFromLocalStorage")

</script>

<style>
</style>