<template>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <router-link
      class="navbar-brand"
      to="/"
    >
      Chess-T-DB
    </router-link>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon" />
    </button>
    <div
      id="navbarNav"
      class="collapse navbar-collapse"
    >
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link
            class="nav-link"
            to="/"
          >
            Home
          </router-link>
        </li>
        <li class="nav-item">
          <!-- TODO : Add disable when the user is logged -->
          <router-link
            class="nav-link"
            to="/log-in"
          >
            Admin Log-In
          </router-link>
        </li>
        <li class="nav-item">
          <!-- TODO : Add disable when the user is not logged -->
          <router-link
            class="nav-link"
            to="/log-out"
          >
            Log-Out
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            to="/faq"
          >
            FAQ
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
console.log("a")
</script>

<style scoped>
	nav a {
	  padding-left: 10px;
	}
</style>