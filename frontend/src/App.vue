<template>
<router-view>

</router-view>
</template>

<script setup>
import { useStore } from 'vuex'

const store = useStore()
store.commit("loadFromLocalStorage")

</script>

<style>
</style>