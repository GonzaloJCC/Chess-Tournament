<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">Chess-T-DB</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <!-- TODO : Add route -->
          <a class="nav-link" href="#">Home</a>
        </li>
        <li class="nav-item">
          <!-- TODO : Add route -->
          <!-- TODO : Add disable when the user is logged -->
          <a class="nav-link" href="#">Admin Log-In</a>
        </li>
        <li class="nav-item">
          <!-- TODO : Add route -->
          <!-- TODO : Add disable when the user is not logged -->
          <a class="nav-link" href="/a">Log-Out</a>
        </li>
        <li class="nav-item">
          <!-- TODO : Add route -->
          <a class="nav-link" href="#">FAQ</a>
        </li>
      </ul>
    </div>
  </nav>
  <RouterView />
</template>

<style scoped>
nav a {
  padding-left: 10px;
}

</style>
