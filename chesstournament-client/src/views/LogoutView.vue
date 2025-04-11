<template>
  <div class="logout-wrapper">
    <div class="logout-box">
      <h1>Log Out</h1>
      <p>You will be redirected to home in 5 seconds.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
    setTimeout(() => {
        router.push('/');
    }, 5000);
});
</script>

<style scoped>
.logout-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    //padding-top: 100px;
    height: 100vh;
    background-color: #ffffff;

    transform: translateY(-50px);
}

.logout-box {
    background-color: rgba(22, 209, 90, 0.34);
    padding: 2rem;
    border-radius: 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 600px;

}


</style>
