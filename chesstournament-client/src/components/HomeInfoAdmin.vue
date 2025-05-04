<template>
    <div class="info">
        <p data-cy="admin-log">
            Hello, you are logged in as an administrator. Remember, with great power comes great responsibility.
        </p>
        <p>
            As an administrator, you can create tournaments and edit or update the results of games, rounds, and tournaments.
        </p>
        <p>
            To create a new tournament, press the "Create Tournament" button. To edit or update games, rounds, or tournaments, select the desired tournament.
        </p>
        <router-link to="/createtournament" class="create-tournament-button">
            Create Tournament
        </router-link>
    </div>
</template>

<script setup>
</script>

<style scoped>
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