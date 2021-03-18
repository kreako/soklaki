<template>
    <div>
        <div class="text-gray-800">Votre adresse email</div>
        <input
            @change="$emit('change', $event.target.value)"
            class="input mt-2"
            :class="{ 'input-error': error }"
            type="email"
            placeholder="mon-email@example.com"
            autocomplete="username"
            required
        />
        <div v-if="error" class="text-right text-red-600">
            <slot name="error"></slot>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmit } from 'vue'

defineProps({
    email: String,
    error: Boolean,
})

defineEmit(['change'])

</script>