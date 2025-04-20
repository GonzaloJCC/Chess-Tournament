<template>
  <div class="container">
    <h1 class="text-center">
      Login
    </h1>

    <form @submit.prevent="handleLogin">
      <!-- Error message -->
      <div
        v-if="error.value"
        class="alert alert-danger text-center"
        role="alert"
        data-cy="error-message"
      >
        {{ error.msg }}
      </div>

      <!-- Username input --> 
      <div class="mb-3">
        <input
          v-model="user.username"
          type="text"
          placeholder="username"
          class="form-control rounded-pill border-0 shadow-sm px-4"
          data-cy="username"
          required
        >
      </div>

      <!-- Password input -->
      <div class="mb-3">
        <input
          v-model="user.password"
          type="password"
          placeholder="password"
          class="form-control rounded-pill border-0 shadow-sm px-4"
          data-cy="password"
          required
        >
      </div>

      <!-- Submit button -->
      <div class="d-grid gap-2 mt-2">
        <button
          type="submit"
          class="btn btn-primary btn-block text-uppercase mb-2 rounded-pill shadow-sm"
          data-cy="login-button"
        >
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue';
  const emit = defineEmits(['confirm-form'])
  const APIURL = import.meta.env.VITE_APIURL;

  /* NOTE: Object where the data will be saved */
  const user = ref({
    username: '',
    password: ''
  })

  /* NOTE: Computed properties to validate the inputs */
  const usernameValid = computed(() => {
    return user.value.username.length > 0;
  });

  const passwordValid = computed(() => {
    return user.value.password.length > 0;
  });

  /* NOTE: Possible errors */
  const error = ref({
    value: false,
    msg: '',
  
    /* Function to set an error */
    set(msg) {
      this.value = true;
      this.msg = msg;
    },

    /* Function to reset the error state */
    reset() {
      this.value = false;
      this.msg = '';
    }
  });

  /* NOTE: Function to clear the fields */

  /* NOTE: Function called when the form is submitted */
  const handleLogin = async () => {
    /* Reset state */
    error.value.reset()

    /* Check the inputs */
    if (!usernameValid.value || !passwordValid.value) {
      error.value.set('All the fields has to be filled');
      return;
    }

    /* The data has been provided: request to API */
    try {
      const response = await fetch(`${APIURL}/api/v1/token/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: user.value.username,
          password: user.value.password
        })
      });

      if (!response.ok) throw new Error('Invalid username or password')
      
      /* Send the information to the parent */
      emit('confirm-form', await response.json())

    }
    catch(e){
      error.value.set(`Error: ${e.message}`);
    }
  }
</script>

<style scoped>
  .container {
    width: 50%;
    border: 2px solid #d6d7d0;
    border-radius: 5px;
    padding: 20px;
  }
</style>