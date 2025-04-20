<template>
  <div class="login-container">
    <LoginForm
      @confirm-form="handleLogin"
    />
  </div>
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
  .login-container {
    position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* Asegura que el contenedor esté centrado */
  padding: 1rem;
  box-sizing: border-box;
  width: 100%;
  }
</style>