<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand"><router-link class="navbar-brand" to="/">Chess-T-DB</router-link></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link"><router-link class="nav-link" to="/">Home</router-link></a>
        </li>
        <li class="nav-item">
          <!-- TODO : Add disable when the user is logged -->
          <a class="nav-link"><router-link class="nav-link" to="/log-in">Admin Log-In</router-link></a>
        </li>
        <li class="nav-item">
          <!-- TODO : Add disable when the user is not logged -->
          <a class="nav-link"><router-link class="nav-link" to="/log-out">Log-Out</router-link></a>
        </li>
        <li class="nav-item">
          <a class="nav-link"><router-link class="nav-link" to="/faq">FAQ</router-link></a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
	nav a {
	  padding-left: 10px;
	}
</style>