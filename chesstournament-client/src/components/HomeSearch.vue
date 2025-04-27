<template>
    <div class="search-box">
        <div class="search-content">
            <div class="search-input-container">
                <input
                    v-model="searchTerm"
                    type="text"
                    placeholder="Tournament"
                    class="search-input"
                />
                <button v-if="searchTerm" @click="clearSearch" class="clear-button">x</button>
                <button @click="searchTournaments" class="search-button">Search</button>
            </div>

            <table v-if="isTableVisible">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="tournament in filteredTournaments" :key="tournament.id">
                        <td>
                            <router-link :to="{ path: '/tournamentdetail', query: { id: tournament.id } }">
                                {{ tournament.name }}
                            </router-link>
                        </td>
                        <td>{{ tournament.start_date }}</td>
                    </tr>
                </tbody>
            </table>

            <p v-if="filteredTournaments.length === 0 && isTableVisible">No tournaments found.</p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const tournaments = ref([]);
const searchTerm = ref('');
const filteredTournaments = ref([]);
const isTableVisible = ref(false);

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

const searchTournaments = () => {
    if (searchTerm.value.trim() === '') {
        isTableVisible.value = true;
    } else {
        filteredTournaments.value = tournaments.value.filter(tournament =>
            tournament.name.toLowerCase().includes(searchTerm.value.toLowerCase())
        );
        isTableVisible.value = true;
    }
};

const clearSearch = () => {
    searchTerm.value = '';
    filteredTournaments.value = [];
    isTableVisible.value = false;
};

fetchTournaments();
</script>

<style scoped>
.search-box {
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    width: 37.5rem;
    font-size: 1.25rem;
    font-family: 'Cascadia Code', Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 9.375rem;
    background-color: rgba(195, 22, 22, 0.34);
}

.search-content {
    width: 100%;
}

.search-input-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.search-input {
    width: 80%;
    padding: 0.75rem;
    font-size: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #ccc;
    margin-bottom: 1rem;
    box-sizing: border-box;
}

.search-button {
    padding: 0.75rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
}

.search-button:hover {
    background-color: #45a049;
}

.clear-button {
    background: none;
    border: none;
    color: #999;
    font-size: 1.25rem;
    cursor: pointer;
}

.clear-button:hover {
    color: #333;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Cascadia Code', Arial, sans-serif;
    table-layout: auto;
    margin-top: 1rem;
}

th, td {
    border: 1px solid rgb(5, 0, 0);
    padding: 1.25rem 2rem;
    text-align: left;
}

th {
    background-color: rgba(18, 114, 209, 0.61);
}

@media (max-width: 48rem) {
    .search-box {
        width: 90%;
    }
}

@media (max-width: 30rem) {
    .search-box {
        font-size: 1rem;
        padding: 1rem;
    }

    .search-input {
        font-size: 0.9rem;
    }

    .search-button {
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }
}
</style>
