<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <h1 class="text-center mb-4">Create a Tournament</h1>
        <form @submit.prevent="registerTournament">
          <!-- Tournament name -->
          <div class="mb-3">
            <label for="tournamentNameInput" class="form-label">Tournament Name</label>
            <input
              v-model="tournamentName"
              type="text"
              class="form-control"
              id="tournamentNameInput"
              placeholder="My Tournament Name"
            >
            <div class="form-text">Tournament full name</div>
          </div>

          <!-- Admin Update -->
          <div class="form-check mb-3">
            <input
              v-model="adminUpdate"
              class="form-check-input"
              type="checkbox"
              id="adminUpdateInput"
            >
            <label class="form-check-label" for="adminUpdateInput">
              Only administrators can update games
            </label>
            <div class="form-text">
              Set to false if users can update games. Otherwise, only administrators can input the results.
            </div>
          </div>

          <!-- Pairing System -->
          <div class="mb-3">
            <label for="pairingSystemInput" class="form-label">Pairing System</label>
            <select
              v-model="pairingSystem"
              class="form-select"
              id="pairingSystemInput"
            >
              <option value="Round Robin">Round Robin</option>
              <option value="Swiss">Swiss</option>
              <!-- añade más opciones si es necesario -->
            </select>
            <div class="form-text">Select the pairing system (Round Robin, Swiss…)</div>
          </div>

          <!-- Board Type -->
          <div class="mb-3">
            <label for="boardTypeInput" class="form-label">Board Type</label>
            <select
              v-model="boardType"
              class="form-select"
              id="boardTypeInput"
            >
              <option value="lichess">Lichess</option>
              <option value="board">On the board</option>
            </select>
            <div class="form-text">Games played on lichess or OTB</div>
          </div>

          <!-- Points -->
          <div class="mb-4">
            <p>Provided points awarded to player if:</p>
            <div class="row g-3">
              <div class="col">
                <label for="winPointsInput" class="form-label">Wins</label>
                <input
                  v-model.number="winPoints"
                  type="number"
                  step="0.1"
                  id="winPointsInput"
                  class="form-control"
                >
              </div>
              <div class="col">
                <label for="drawPointsInput" class="form-label">Draws</label>
                <input
                  v-model.number="drawPoints"
                  type="number"
                  step="0.1"
                  id="drawPointsInput"
                  class="form-control"
                >
              </div>
              <div class="col">
                <label for="losePointsInput" class="form-label">Loses</label>
                <input
                  v-model.number="losePoints"
                  type="number"
                  step="0.1"
                  id="losePointsInput"
                  class="form-control"
                >
              </div>
            </div>
          </div>

          <!-- Tournament category -->
          <div class="mb-4">
            <label for="tournamentCategoryInput" class="form-label">Tournament Category</label>
            <select
              v-model="tournamentCategory"
              class="form-select"
              id="tournamentCategoryInput"
            >
              <option value="classical">Classical</option>
              <option value="tapid">Rapid</option>
              <option value="blitz">Blitz</option>
              <option value="bullet">Bullet</option>
            </select>
            <div class="form-text">Select the tournament category</div>
          </div>

          <button type="submit" class="btn btn-primary w-100">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  
  const tournamentName     = ref('');
  const adminUpdate        = ref(false);
  const pairingSystem      = ref('Round Robin');
  const boardType          = ref('lichess');
  const winPoints          = ref(1.0);
  const drawPoints         = ref(0.0);
  const losePoints         = ref(0.0);
  const tournamentCategory = ref('classical');
  
  function registerTournament() {
    /* Print the data */
    console.log({
      tournamentName: tournamentName.value,
      adminUpdate: adminUpdate.value,
      pairingSystem: pairingSystem.value,
      boardType: boardType.value,
      winPoints: winPoints.value,
      drawPoints: drawPoints.value,
      losePoints: losePoints.value,
      tournamentCategory: tournamentCategory.value,
    });
  }
</script>

<style scope>
</style>