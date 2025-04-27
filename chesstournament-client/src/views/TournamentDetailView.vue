<template>
    <div class="tournament-detail">
        <div v-if="loading">Loading tournament...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else-if="tournament">
            <h2>{{ tournament.name }}</h2>
            <p><strong>Start Date:</strong> {{ tournament.start_date }}</p>
            <p><strong>End Date:</strong> {{ tournament.end_date }}</p>
            <p><strong>Location:</strong> {{ tournament.location }}</p>
        </div>
        <div v-else>
            Tournament not found.
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const tournament = ref(null);
const loading = ref(true);
const error = ref(null);

const route = useRoute();

const fetchTournament = async () => {
    try {
        const tournamentId = route.query.id;
        if (!tournamentId) {
            error.value = 'No tournament ID provided';
            return;
        }

        const url = `${import.meta.env.VITE_DJANGOURL}tournaments/${tournamentId}/`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch tournament');
        }

        tournament.value = await response.json();
    } catch (err) {
        console.error(err);
        error.value = 'Error loading tournament';
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchTournament();
});
</script>

<style scoped>
.tournament-detail {
    padding: 2rem;
    max-width: 40rem;
    margin: 0 auto;
    background: rgba(69, 81, 99, 0.46);
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    font-family: 'Cascadia Code', Arial, sans-serif;
}

h2 {
    margin-bottom: 1rem;
    color: #2c3e50;
}

p {
    margin-bottom: 0.75rem;
    font-size: 1.125rem;
}

strong {
    color: #34495e;
}
</style>
