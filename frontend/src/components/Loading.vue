<template>
  <div v-if="loading" class="min-h-full flex items-center justify-center p-4">
    <div class="thing">
      <div class="thing">
        <div class="thing">
          <div class="thing">
            <div class="thing">
              <div class="thing">
                <div class="thing">
                  <div class="thing">
                    <div class="thing"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <slot></slot>
  </div>
</template>

<script setup>
const props = defineProps({
  loading: Boolean,
});
</script>

<style scope>
.thing {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 5px;
  border: 10px solid transparent;
  border-color: #0d9488 #eab308 #dc2626 #db2777;
  border-radius: 25%;
  animation: thing 5s cubic-bezier(0.35, -0.14, 0.79, 1.22) infinite;
}

@keyframes thing {
  100% {
    transform: rotateZ(1turn);
  }
}
</style>
