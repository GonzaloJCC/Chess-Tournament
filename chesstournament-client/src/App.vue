<script setup>
  import { RouterView } from 'vue-router'
  import AppNav from '@/components/AppNav.vue';
  import AppFooter from '@/components/AppFooter.vue';
</script>

<template>
  <AppNav />
  <RouterView />
  <AppFooter />
</template>

<style scoped>
</style>
