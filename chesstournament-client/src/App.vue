<template>
  <div id="container">
    <AppNav id="AppNav" />
    <div id="RouterView">
      <RouterView />
    </div>
    <AppFooter id="AppFooter" />
  </div>
</template>

<script setup>
  import { RouterView } from 'vue-router'
  import AppNav from '@/components/AppNav.vue';
  import AppFooter from '@/components/AppFooter.vue';
</script>

<style scoped>
  #container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  #AppNav {
    flex: 0 0 auto;
  }

  #RouterView {
    flex: 1 1 auto;
    overflow: auto;
  }

  #AppFooter {
    flex: 0 0 auto;
  }
</style>
