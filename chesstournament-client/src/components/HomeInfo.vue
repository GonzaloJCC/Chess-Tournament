<template>
    <div class="info">
        <p>
            Welcome to the Chess Tournament Database. This database features the unique ability for players to update the results of their games. To create tournaments, an administrative account is required. However, any player can enter the result of a game.
        </p>
        <p>
            You can use the search button to find tournaments by name. For further information, please refer to the
            <router-link to="/faq" class="">FAQ</router-link> section.
        </p>
    </div>
</template>

<script setup>
</script>

<style scoped>
html {
    font-size: 16px;
}

.info {
    background-color: rgba(22, 209, 90, 0.34);
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    text-align: left;
    width: 100%;
    max-width: 76.875rem;
    font-size: 1.25rem;
    font-family: 'Cascadia Code', Arial, sans-serif;
    margin: 0 auto;
    box-sizing: border-box;
}

.create-tournament-button {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #2c3e50;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
}

.create-tournament-button:hover {
    background-color: #1a252f;
}

@media (max-width: 48rem) {
    .info {
        width: 90%;
        padding: 1.5rem;
    }
}

@media (max-width: 30rem) {
    .info {
        font-size: 1rem;
        padding: 1rem;
    }
}
</style>
