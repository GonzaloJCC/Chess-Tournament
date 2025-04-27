<template>
    <div class="tournaments">
        <div class="tournament-content">
            <div v-if="paginatedTournaments.length === 0">No tournaments available</div>

            <table v-else>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="tournament in paginatedTournaments" :key="tournament.id">
                        <td>
                            <router-link :to="{ name: 'tournamentdetail', query: { id: tournament.id } }">
                                {{ tournament.name }}
                            </router-link>
                        </td>
                        <td>{{ tournament.start_date }}</td>
                    </tr>
                </tbody>
            </table>

            <div class="pagination">
                <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
                <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const tournaments = ref([]);
const currentPage = ref(1);
const pageSize = 5;

const fetchTournaments = async () => {
    try {
        const url = `${import.meta.env.VITE_DJANGOURL}tournaments/`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Error fetching tournaments');
        const data = await response.json();
        tournaments.value = data.results;
    } catch (error) {
        console.error('Error loading tournaments:', error);
    }
};

onMounted(() => {
    fetchTournaments();
});

const totalPages = computed(() => Math.ceil(tournaments.value.length / pageSize));

const paginatedTournaments = computed(() => {
    const start = (currentPage.value - 1) * pageSize;
    return tournaments.value.slice(start, start + pageSize);
});

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};
</script>

<style scoped>
.tournaments {
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    width: 37.5rem;
    font-size: 1.25rem;
    font-family: 'Cascadia Code', Arial, sans-serif;
    background-color: rgba(69, 81, 99, 0.46);
    display: flex;
    justify-content: center;
}

.tournament-content {
    width: 100%;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
}

th, td {
    border: 1px solid rgb(5, 0, 0);
    padding: 1.25rem 2rem;
    text-align: left;
}

th {
    background-color: rgba(18, 114, 209, 0.61);
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
}

.pagination button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    background-color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
}

.pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 48rem) {
    .tournaments {
        width: 90%;
    }
}

@media (max-width: 30rem) {
    .tournaments {
        font-size: 1rem;
        padding: 1rem;
    }

    .pagination button {
        font-size: 0.9rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>
