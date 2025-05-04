<template>
    <div class="tournament-detail">
        <div v-if="loading">Loading...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <h1>Tournament: {{ tournament.name }}</h1>

            <div class="content-container">
                <!-- Ranking Section -->
                <div class="ranking-section">
                    <h3>Standing</h3>
                    <table class="ranking-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Player</th>
                                <th v-if="tournament.rankingList.includes('PS')">Points</th>
                                <th v-if="tournament.rankingList.includes('WI')">Wins</th>
                                <th v-if="tournament.rankingList.includes('BT')">Black Times</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="entry in ranking" :key="entry.id">
                                <td>{{ entry.rank }}</td>
                                <td>{{ entry.username }}</td>
                                <td v-if="tournament.rankingList.includes('PS')">{{ entry.score }}</td>
                                <td v-if="tournament.rankingList.includes('WI')">{{ entry.WI || 0 }}</td>
                                <td v-if="tournament.rankingList.includes('BT')">{{ entry.BT || 0 }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Rounds Section -->
                <div class="rounds-section" v-if="rounds.length">
                    <!-- Mostrar el tipo de torneo -->
                    <h2>Pairings/Results</h2>
                    <h3 class="tournament-type">{{ tournament.board_type === 'OTB' ? 'OTB' : 'LICHESS' }}</h3>
					<div v-if="tournament.board_type === 'LIC'">
						<p>Press <i class="bi bi-send" /> to update the game result. See the <router-link to="/faq" class="">FAQ</router-link> for more information.</p>
					</div>
						<div v-else>	
                    <p>The abbreviations used in the "result" column are explained at the end of the page.
                        Press <i class="bi bi-send" /> to update the game result. See the <router-link to="/faq" class="">FAQ</router-link> for more information.</p>
                    </div>
					
                    <div v-for="round in rounds" :key="round.id" class="round-table">
                        <h3>{{ round.name }}</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>White Player</th>
                                    <th>Result</th>
                                    <th>Black Player</th>
                                    <th v-if="isLoggedIn">Result (Admin)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="game in gamesByRound[round.id] || []" :key="game.id">
                                    <td>{{ game.white_player_name }}</td>
                                    <td>
                                        <!-- Mostrar un campo de texto si el torneo es de tipo LIC y el resultado no está bloqueado -->
                                        <template v-if="tournament.board_type === 'LIC'">
                                            <template v-if="!game.resultLocked">
                                                <input
                                                    type="text"
                                                    v-model="game.lichessGameID"
                                                    placeholder="type gameID"
                                                />
                                                <button @click="submitLichessGameID(game)">
                                                    <i class="bi bi-send" />
                                                </button>
                                            </template>
                                            <template v-else>
												<div v-if="game.result === 'w'">
													<p>1-0</p>
												</div>
												<div v-else-if="game.result === 'b'">
													<p>0-1</p>
												</div>
												<div v-else-if="game.result === '='">
													<p>1/2-1/2</p>
												</div>
												<div v-else>
													<p>*</p>
												</div>
                                            </template>
                                        </template>

                                        <!-- Mostrar el campo select si el torneo es de tipo OTB -->
                                        <template v-else>
                                            <template v-if="!game.resultLocked">
                                                <select v-model="game.result">
                                                    <option value="w">White wins (1-0)</option>
                                                    <option value="b">Black wins (0-1)</option>
                                                    <option value="=">Draw (1/2-1/2)</option>
                                                    <option value="*">Unknown Result (*)</option>
                                                </select>
                                                <button @click="promptConfirmGameResult(game)">
                                                    <i class="bi bi-send" />
                                                </button>
                                            </template>
                                            <template v-else>
                                                <div v-if="game.result === 'w'">
													<p>1-0</p>
												</div>
												<div v-else-if="game.result === 'b'">
													<p>0-1</p>
												</div>
												<div v-else-if="game.result === '='">
													<p>1/2-1/2</p>
												</div>
												<div v-else>
													<p>*</p>
												</div>
                                            </template>
                                        </template>
                                    </td>
                                    <td>{{ game.black_player_name }}</td>
                                    <td v-if="isLoggedIn">
                                        <select v-model="game.adminResult">
                                            <option value="w">White wins (1-0)</option>
                                            <option value="b">Black wins (0-1)</option>
                                            <option value="=">Draw (1/2-1/2)</option>
                                            <!-- <option value="*">Unknown Result (*)</option> -->
                                        </select>
                                        <button @click="confirmAdminResult(game)"><i class="bi bi-send" /></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Modal -->
            <div v-if="showModal" class="modal-overlay">
                <div class="modal">
                    <h3>Confirm Result</h3>
                    <p>Please enter the email used to join this tournament:</p>
                    <input type="email" v-model="email" placeholder="Enter your email" />
                    <div class="modal-actions">
                        <button @click="validateAndConfirmResult">Confirm</button>
                        <button @click="closeModal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTokenStore } from '@/stores/token';
import { computed } from 'vue';

const tournament = ref(null)
const rounds = ref([])
const gamesByRound = ref({})
const ranking = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const email = ref('')
const selectedGame = ref(null)

const route = useRoute()

const tokenStore = useTokenStore();
const isLoggedIn = computed(() => tokenStore.token !== null);

async function fetchTournament() {
    const id = route.query.id;
    if (!id) {
        throw new Error('No tournament ID provided');
    }
    const res = await fetch(`${import.meta.env.VITE_DJANGOURL}tournaments/${id}/`);
    if (!res.ok) {
        throw new Error('Failed to fetch tournament');
    }
    const data = await res.json();
    tournament.value = {
        ...data,
        win_points: data.win_points,
        draw_points: data.draw_points,
        lose_points: data.lose_points,
        board_type: data.board_type,
    };
}

async function fetchRounds() {
    const id = route.query.id;
    const res = await fetch(`${import.meta.env.VITE_DJANGOURL}get_round_results/${id}/`);
    if (!res.ok) {
        throw new Error('Failed to fetch rounds');
    }
    const data = await res.json();
    rounds.value = data;

    gamesByRound.value = data.reduce((acc, round) => {
        acc[round.id] = round.games.map(game => ({
            id: game.id,
            white_player_name: game.white_player_name,
            black_player_name: game.black_player_name,
            white_player_email: game.white_player_email,
            black_player_email: game.black_player_email,
            result: game.result,
            lichessGameID: '', // Nuevo campo para almacenar el gameID de LIC
            adminResult: '', // Nuevo campo para el selector Admin
            status: game.finished ? 'Finished' : 'Ongoing',
            emailInput: '',
            emailValidated: false,
            resultLocked: game.finished, // Sincroniza con el campo "finished" del backend
        }));
        return acc;
    }, {});
}

async function fetchRanking() {
    const id = route.query.id;
    try {
        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}get_ranking/${id}/`);
        if (!res.ok) {
            throw new Error('Failed to fetch ranking');
        }
        const data = await res.json();

        // Si no hay jugadores, asigna un array vacío
        if (!data || Object.keys(data).length === 0) {
            ranking.value = [];
            return;
        }

        // Si hay jugadores, procesa los datos
        ranking.value = Object.values(data).map(entry => ({
            id: entry.id,
            username: entry.username,
            score: entry.score,
            rank: entry.rank,
            WI: entry.WI,
            BT: entry.BT,
        }));
    } catch (error) {
        console.error('Error fetching ranking:', error);
        ranking.value = []; // Asigna un array vacío en caso de error
    }
}

function openEmailModal(game) {
    console.log('Opening modal for game:', game);
    selectedGame.value = game;
    showModal.value = true;
    console.log('Modal state:', showModal.value); // Verifica si cambia a true
}

function closeModal() {
    showModal.value = false;
    email.value = '';
    selectedGame.value = null;
}

async function promptConfirmGameResult(game) {
    const userEmail = window.prompt(
        `Please enter the email used to join this tournament:`
    );

    if (!userEmail) {
        console.log("Email confirmation canceled.");
        alert("Email confirmation canceled.");
        return;
    }

    const whitePlayerEmail = game.white_player_email;
    const blackPlayerEmail = game.black_player_email;

    if (userEmail === whitePlayerEmail || userEmail === blackPlayerEmail) {
        try {
            const res = await fetch(`${import.meta.env.VITE_DJANGOURL}update_otb_game/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    game_id: game.id,
                    otb_result: game.result,
                    email: userEmail,
                }),
            });

            if (!res.ok) {
                throw new Error("Failed to update game result");
            }

            game.resultLocked = true;
            game.status = "Finished";
            alert("Result confirmed successfully!");

            await fetchRanking();
        } catch (error) {
            console.error("Error updating game result:", error);
            alert("Error updating game result. Please try again.");
        }
    } else {
        console.log("Email does not match with any player in the game.");
        alert("Email does not match with any player in the game.");
    }
}

async function confirmAdminResult(game) {
    try {
        if (!tokenStore.token) {
            console.error("Token is missing.");
            alert("You must be logged in to perform this action.");
            return;
        }

        console.log("Token being sent:", tokenStore.token);

        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}admin_update_game/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Token ${tokenStore.token}`,
            },
            body: JSON.stringify({
                game_id: game.id,
                otb_result: game.adminResult,
            }),
        });

        if (!res.ok) {
            const errorData = await res.json();
            console.error("Error response from backend:", errorData);
            alert(`Error: ${errorData.message || "Failed to update game result"}`);
            return;
        }

        game.result = game.adminResult;
        game.resultLocked = true;

        await fetchRanking();
    } catch (error) {
        console.error("Error updating admin game result:", error);
        alert("An unexpected error occurred while updating the game result. Please try again.");
    }
}

async function submitLichessGameID(game) {
    try {
        if (!game.lichessGameID) {
            alert("Please enter a valid game ID.");
            return;
        }

        // Enviar el gameID al backend
        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}update_lichess_game/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Token ${tokenStore.token}`, // Asegúrate de enviar el token si es necesario
            },
            body: JSON.stringify({
                game_id: game.id,
                lichess_game_id: game.lichessGameID,
            }),
        });

        if (!res.ok) {
            const errorData = await res.json();
            console.error("Error response from backend:", errorData);
            alert(`Error: ${errorData.message || "Failed to update game result"}`);
            return;
        }

        const responseData = await res.json();

        // Actualizar el estado del juego localmente
        game.result = responseData.result; // Asigna el resultado directamente desde el backend
        game.resultLocked = true; // Bloquea el resultado
        game.status = "Finished"; // Cambia el estado del juego
        alert("Game ID submitted successfully!");

        // Actualizar el ranking
        await fetchRanking();
    } catch (error) {
        console.error("Error submitting Lichess game ID:", error);
        alert("An unexpected error occurred while submitting the game ID. Please try again.");
    }
}

onMounted(async () => {
    try {
        await fetchTournament()
        await fetchRounds()
        await fetchRanking()
    } catch (e) {
        console.error(e)
        error.value = e.message
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.tournament-detail {
    padding: 2rem;
    max-width: 100%;
    margin: 0 auto;
    background: rgb(255, 255, 255);
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    font-family: 'Cascadia Code', Arial, sans-serif;
}

h2, h3 {
    color: #2c3e50;
}

p {
    margin-bottom: 0.75rem;
    font-size: 1.125rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
}

thead {
    background-color: #2c3e50;
    color: white;
}

th, td {
    padding: 0.75rem;
    border: 1px solid #ccc;
    text-align: center;
}

.ranking-table {
    margin-bottom: 2rem;
}

.round-table {
    margin-top: 2rem;
}

/* New styles for layout */
.content-container {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
}

.ranking-section {
    flex: 1;
    max-width: 40%;
}

.rounds-section {
    flex: 2;
    max-width: 60%;
    overflow-y: auto;
}

/* Modal styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
    width: 300px;
    text-align: center;
}

.modal input {
    width: 100%;
    padding: 0.5rem;
    margin: 1rem 0;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.modal-actions {
    display: flex;
    justify-content: space-between;
}

.modal-actions button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.modal-actions button:first-child {
    background-color: #2c3e50;
    color: white;
}

.modal-actions button:first-child:hover {
    background-color: #1a252f;
}

.modal-actions button:last-child {
    background-color: #ccc;
    color: black;
}

.modal-actions button:last-child:hover {
    background-color: #aaa;
}

/* Button styles */
button {
    margin-left: 0.5rem;
    padding: 0.25rem 0.5rem;
    background-color: #ffffff;
    color: rgb(0, 0, 0);
    border: 1px solid black; /* Agrega un borde negro */
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #3d8bd4;
    color: white; /* Cambia el color del texto al pasar el mouse */
}
</style>
