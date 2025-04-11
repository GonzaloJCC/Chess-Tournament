<template>
  <LoginForm
    @confirm-form="handleLogin"
  />
</template>

<script setup>
  import LoginForm from '@/components/LoginForm.vue'
  import { useTokenStore } from '@/stores/token';
  import { useRouter } from 'vue-router';

  const tokenStore = useTokenStore();
  const router = useRouter();

  /* NOTE: Function to log in the user, with the API data */
  const handleLogin = (data) => {
    tokenStore.setToken(data.auth_token);
    router.push('/')
  }
</script>

<style scope>
</style>