<template>
  <div class="tournament-detail">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else-if="error">
      {{ error }}
    </div>
    <div v-else>
      <h1 data-cy="tournament-title">
        Tournament: {{ tournament.name }}
      </h1>

      <div class="content-container">
        <!-- Standing Accordion -->
        <div class="accordion">
          <button
            class="accordion-button"
            data-cy="standing-accordion-button"
            @click="toggleAccordion('standing')"
          >
            Standing
          </button>
          <div
            v-show="activeAccordion === 'standing'"
            class="accordion-content"
            data-cy="standing-accordion-content"
          >
            <h3>Standing</h3>
            <table class="ranking-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player</th>
                  <th>Score</th> <!-- Nueva columna para Points -->
                  <!-- Generar dinámicamente las columnas según rankingList -->
                  <th
                    v-for="field in tournament.rankingList"
                    :key="field"
                  >
                    {{ getRankingHeader(field) }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="entry in ranking"
                  :key="entry.id"
                  :data-cy="`ranking-${entry.rank}`"
                >
                  <td>{{ entry.rank }}</td>
                  <td>{{ entry.username }}</td>
                  <td>{{ entry.score || 0 }}</td> <!-- Nueva celda para Points -->
                  <!-- Generar dinámicamente las celdas según rankingList -->
                  <td
                    v-for="field in tournament.rankingList"
                    :key="field"
                  >
                    {{ entry[field] || 0.00 }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pairings/Results Accordion -->
        <div class="accordion">
          <button
            class="accordion-button"
            data-cy="pairings-accordion-button"
            @click="toggleAccordion('pairings')"
          >
            Pairings/Results
          </button>
          <div
            v-show="activeAccordion === 'pairings'"
            class="accordion-content"
            data-cy="pairings-accordion-content"
          >
            <h2>Pairings/Results</h2>
            <h3 class="tournament-type">
              {{ tournament.board_type === 'OTB' ? 'OTB' : 'LICHESS' }}
            </h3>
            <div v-if="tournament.board_type === 'LIC'">
              <p>
                Press <i class="bi bi-send" /> to update the game result. See the
                <router-link
                  to="/faq"
                  class=""
                >
                  FAQ
                </router-link> for more information.
              </p>
            </div>
            <div v-else>
              <p>
                The abbreviations used in the "result" column are explained at the end of the page.
                Press <i class="bi bi-send" /> to update the game result. See the
                <router-link
                  to="/faq"
                  class=""
                >
                  FAQ
                </router-link> for more information.
              </p>
            </div>

            <div
              v-for="round in rounds"
              :key="round.id"
              class="round-table"
            >
              <h3 :data-cy="round.name.toLowerCase().replace(/\s+/g, '_')">
                {{ round.formatted_name }}
              </h3>
              <table>
                <thead>
                  <tr>
                    <th>White Player</th>
                    <th>Result</th>
                    <th>Black Player</th>
                    <th v-if="isLoggedIn">
                      Result (Admin)
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="game in gamesByRound[round.id] || []"
                    :key="game.id"
                    :data-cy="`game_${round.number}_${game.count}`"
                  >
                    <td>{{ game.white_player_name }}</td>
                    <td>
                      <!-- Mostrar el campo de texto si el torneo es de tipo LIC -->
                      <template v-if="tournament.board_type === 'LIC'">
                        <template v-if="!game.resultLocked">
                          <input
                            v-model="game.lichessGameID"
                            type="text"
                            placeholder="type gameID"
                            :data-cy="`input-${round.number}-${game.count}`"
                          >
                          <button
                            :data-cy="`button-${round.number}-${game.count}`"
                            @click="submitLichessGameID(game)"
                          >
                            <i class="bi bi-send" />
                          </button>
                        </template>
                        <template v-else>
                          <div v-if="game.result === 'w'">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              1-0
                            </p>
                          </div>
                          <div v-else-if="game.result === 'b'">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              0-1
                            </p>
                          </div>
                          <div v-else-if="game.result === '='">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              ½-½
                            </p>
                          </div>
                          <div v-else>
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              *
                            </p>
                          </div>
                        </template>
                      </template>

                      <!-- Mostrar el campo select si el torneo es de tipo OTB -->
                      <template v-else>
                        <template v-if="!game.resultLocked">
                          <select
                            v-model="game.result"
                            :data-cy="`select-${round.number}-${game.count}`"
                          >
                            <option
                              value="White wins (1-0)"
                              data-cy="White wins (1-0)"
                            >
                              White wins (1-0)
                            </option>
                            <option
                              value="Black wins (0-1)"
                              data-cy="Black wins (0-1)"
                            >
                              Black wins (0-1)
                            </option>
                            <option
                              value="Draw (1/2-1/2)"
                              data-cy="Draw (1/2-1/2)"
                            >
                              Draw (1/2-1/2)
                            </option>
                            <option
                              value="Unknown Result (*)"
                              data-cy="Unknown Result (*)"
                            >
                              Unknown Result (*)
                            </option>
                          </select>
                          <button
                            :data-cy="`button-${round.number}-${game.count}`"
                            @click="promptConfirmGameResult(game)"
                          >
                            <i class="bi bi-send" />
                          </button>
                        </template>
                        <template v-else>
                          <div v-if="game.result === 'w'">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              1-0
                            </p>
                          </div>
                          <div v-else-if="game.result === 'b'">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              0-1
                            </p>
                          </div>
                          <div v-else-if="game.result === '='">
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              ½-½
                            </p>
                          </div>
                          <div v-else>
                            <p :data-cy="`input-${round.number}-${game.count}`">
                              *
                            </p>
                          </div>
                        </template>
                      </template>
                    </td>
                    <td>{{ game.black_player_name }}</td>
                    <td v-if="isLoggedIn">
                      <select
                        v-model="game.adminResult"
                        :data-cy="`select-admin-${round.number}-${game.count}`"
                      >
                        <option
                          value="White wins (1-0)"
                          data-cy="White wins (1-0)"
                        >
                          White wins (1-0)
                        </option>
                        <option
                          value="Black wins (0-1)"
                          data-cy="Black wins (0-1)"
                        >
                          Black wins (0-1)
                        </option>
                        <option
                          value="Draw (1/2-1/2)"
                          data-cy="Draw (1/2-1/2)"
                        >
                          Draw (1/2-1/2)
                        </option>
                        <option
                          value="Unknown Result (*)"
                          data-cy="Unknown Result (*)"
                        >
                          Unknown Result (*)
                        </option>
                      </select>
                      <button
                        :data-cy="`button-admin-${round.number}-${game.count}`"
                        @click="handleAdminResultChange(game)"
                      >
                        <i class="bi bi-send" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useTokenStore } from '@/stores/token';
import { computed } from 'vue';

const tournament = ref(null);
const rounds = ref([]);
const gamesByRound = ref({});
const ranking = ref([]);
const loading = ref(true);
const error = ref(null);
const showModal = ref(false);
const email = ref('');
const selectedGame = ref(null);
const activeAccordion = ref('pairings'); // Por defecto, abre el acordeón de Pairings/Results

const route = useRoute();

const tokenStore = useTokenStore();
const isLoggedIn = computed(() => tokenStore.token !== null);

function toggleAccordion(section) {
    activeAccordion.value = activeAccordion.value === section ? null : section;
}

async function fetchTournament() {
    const id = route.query.id;
    if (!id) {
        throw new Error('No tournament ID provided');
    }
    const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/tournaments/${id}/`);
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
    const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/get_round_results/${id}/`);
    if (!res.ok) {
        throw new Error('Failed to fetch rounds');
    }
    let data = await res.json();

    /* Convert "Round 1" in "round_001" */
    let count = 0;
    data.forEach(item => {
        item.formatted_name = item.name.toLowerCase().replace(/\s+/g, '_').replace(/(\d+)$/, (_, num) => {
            return num.padStart(3, '0');
        });
        item.number = ++count;
    });

    rounds.value = data;

    count = -1;
    gamesByRound.value = data.reduce((acc, round) => {
        acc[round.id] = round.games.map(game => {
            count++;
            console.log(`Game result for round ${round.number}, game ${game.count}:`, game.result);
            return {
                id: game.id,
                count: count % ((rounds.value.length + 1) / 2) + 1,
                white_player_name: game.white_player_name || game.white_lichess_username || "Unknown",
                black_player_name: game.black_player_name || game.black_lichess_username || "Unknown",
                white_player_email: game.white_player_email,
                black_player_email: game.black_player_email,
                result: game.result,
                lichessGameID: '', // Nuevo campo para almacenar el gameID de LIC
                adminResult: '', // Nuevo campo para el selector Admin
                status: game.finished ? "Finished" : "Ongoing",
                emailInput: '',
                emailValidated: false,
                // Si el resultado es "*", desbloquea el selector
                resultLocked: game.result !== "*", // Bloquea solo si el resultado no es "*"
            };
        });
        return acc;
    }, {});
}

async function fetchRanking() {
    const id = route.query.id;
    try {
        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/get_ranking/${id}/`);
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
            WI: entry.WI.toFixed(2),
            BT: entry.BT.toFixed(2),
        }));
    } catch (error) {
        console.error('Error fetching ranking:', error);
        ranking.value = []; // Asigna un array vacío en caso de error
    }
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

    if (game.result === "White wins (1-0)")
            game.result = "w";
        else if (game.result === "Black wins (0-1)") 
           game.result = "b";
        else if (game.result === "Draw (1/2-1/2)") 
            game.result = "=";
        else
            game.result = "*";

    const whitePlayerEmail = game.white_player_email;
    const blackPlayerEmail = game.black_player_email;

    if (userEmail === whitePlayerEmail || userEmail === blackPlayerEmail) {
        try {
            const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/update_otb_game/`, {
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

async function handleAdminResultChange(game) {
    try {
        if (!tokenStore.token) {
            console.error("Token is missing.");
            return;
        }
        if (game.adminResult === "White wins (1-0)")
            game.adminResult = "w";
        else if (game.adminResult === "Black wins (0-1)") 
           game.adminResult = "b";
        else if (game.adminResult === "Draw (1/2-1/2)") 
            game.adminResult = "=";
        else
            game.adminResult = "*";
        

        const isUnknownResult = game.adminResult === "*";

        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/admin_update_game/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Token ${tokenStore.token}`,
            },
            body: JSON.stringify({
                game_id: game.id,
                otb_result: game.adminResult, // Enviar el resultado seleccionado por el administrador
            }),
        });

        if (!res.ok) {
            const errorData = await res.json();
            console.error("Error response from backend:", errorData);
            return;
        }

        // Actualizar el estado del juego localmente
        if (isUnknownResult) {
            game.resultLocked = false; // Desbloquear el campo result
            game.result = ""; // Restablecer el resultado para que regrese al selector
        } else {
            game.result = game.adminResult; // Actualizar el resultado localmente
            game.resultLocked = true; // Bloquear el resultado
        }

        // Actualizar el ranking
        await fetchRanking();
    } catch (error) {
        console.error("Error updating admin game result:", error);
    }
}

async function submitLichessGameID(game) {
    try {
        if (!game.lichessGameID) {
            alert("Please enter a valid game ID.");
            return;
        }

        // Enviar el gameID al backend
        const res = await fetch(`${import.meta.env.VITE_DJANGOURL}/update_lichess_game/`, {
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
        console.log("Response from backend:", responseData);

        // Actualizar el estado del juego localmente
        game.result = responseData.game_result; // Usar el resultado devuelto por el backend
        game.resultLocked = true; // Bloquear el resultado inmediatamente
        game.status = "Finished"; // Cambia el estado del juego
        alert("Game ID submitted successfully!");

        // Actualizar el ranking
        await fetchRanking();
    } catch (error) {
        console.error("Error submitting Lichess game ID:", error);
        alert("An unexpected error occurred while submitting the game ID. Please try again.");
    }
}

function getRankingHeader(field) {
    const headers = {
        PS: 'Points',
        WI: 'Wins',
        BT: 'Black Times',
    };
    return headers[field] || field;
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
    overflow: visible; /* Asegúrate de que las tablas no recorten contenido */
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
    overflow-y: visible; /* Cambiar de auto a visible para evitar recortes */
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
    z-index: 10; /* Asegúrate de que los botones estén por encima de otros elementos */
    position: relative;
}

button:hover {
    background-color: #3d8bd4;
    color: white; /* Cambia el color del texto al pasar el mouse */
}

select {
    z-index: 10; /* Asegúrate de que los selectores estén por encima de otros elementos */
    position: relative; /* Asegura que el selector no sea afectado por contenedores padres */
}

/* Accordion styles */
.accordion {
    margin-bottom: 1rem;
}

.accordion-button {
    width: 100%;
    text-align: left;
    padding: 1rem;
    background-color: #2c3e50;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 1.25rem;
    border-radius: 4px;
}

.accordion-button:hover {
    background-color: #1a252f;
}

.accordion-content {
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f9f9f9;
}
</style>
