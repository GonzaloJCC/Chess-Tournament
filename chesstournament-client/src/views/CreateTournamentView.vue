<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <h1 class="text-center mb-4">Create a Tournament</h1>
        <form @submit.prevent="registerTournament">
          <fieldset class="border rounded p-3 mb-4">
            <legend class="float-none w-auto px-2">General</legend>
            
            <!-- Tournament name -->
            <TextInput
              id="tournamentNameInput"
              v-model="tournamentName"
              label="Tournament Name"
              type="text"
              placeholder="My Tournament Name"
              helpText="Tournament full name"
            />
            <hr class="divider">

            <!-- Admin Update -->
            <CheckboxInput
              id="adminUpdateInput"
              v-model="adminUpdate"
              label="Only administrators can update games"
              helpText="Set to false if users can update games. Otherwise, only administrators can input the results."
            />
          </fieldset>

          <fieldset class="border rounded p-3 mb-4">
            <legend class="float-none w-auto px-2">Configuration</legend>

            <!-- Pairing System -->
            <SelectInput
              id="pairingSystemInput"
              v-model="pairingSystem"
              label="Pairing System"
              :options="[
                { label: 'Round Robin', value: 'Round Robin' },
                { label: 'Swiss', value: 'Swiss' }
              ]"
              helpText="Select the pairing system (Round Robin, Swiss…)"
            />
            <hr class="divider">

            <!-- Board Type -->
            <SelectInput
              id="boardTypeInput"
              v-model="boardType"
              label="Board Type"
              :options="[
                { label: 'Lichess', value: 'lichess' },
                { label: 'On the board', value: 'board'}
              ]"
              helpText="Games played on lichess or OTB"
            />
            <hr class="divider">

            <!-- Points -->
            <div class="mb-4">
              <p class="fw-bold">Points given</p>
              <div class="row g-3">
                <TextInput
                  id="winPointsInput"
                  v-model.number="winPoints"
                  class="col"
                  label="Wins"
                  type="number"
                />
                <TextInput
                  id="drawPointsInput"
                  v-model.number="drawPoints"
                  class="col"
                  label="Draws"
                  type="number"
                />
                <TextInput
                  id="losePointsInput"
                  v-model.number="losePoints"
                  class="col"
                  label="Loses"
                  type="number"
                />
              </div>
            </div>
            <hr class="divider">

            <!-- Ranking methods -->
            <MultipleSelectInput
              id-prefix="rank"
              title="Ranking method used in the tournament"
              label="Select ranking methods in the order in which they should be applied"
              v-model="selectedMethods"
              :options="[
                { label: 'Number of wins', value: 'WI'},
                { label: 'Number of times player as Black', value: 'BT'}
              ]"
              helpText="Order in which ranking methods are applied"
            />
            <hr class="divider">

            <!-- Tournament category -->
            <SelectInput
              id="tournamentCategoryInput"
              v-model="tournamentCategory"
              label="Tournament Category"
              :options="[
                { label: 'Classical', value: 'classical' },
                { label: 'Rapid', value: 'rapid' },
                { label: 'Blitz', value: 'blitz' },
                { label: 'Bullet', value: 'bullet' }
              ]"
              helpText="Select the tournament category"
            />
          </fieldset>

          <fieldset class="border rounded p-3 mb-4">
            <legend class="float-none w-auto px-2">Players</legend>

            <!-- Player csv -->
            <TextAreaForm
              id="playersInput"
              v-model="playersCsv"
              label="List of players"
              rows="4"
              placeholder="Introduce players using the CSV format (see FAQ for details). Do NOT add trailing spaces"
              helpText="NOTE: The format is explained in the FAQ Page"
            />
          </fieldset>

          <button type="submit" class="btn btn-primary w-100">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import TextInput from '@/components/form/TextInput.vue';
  import CheckboxInput from '@/components/form/CheckboxInput.vue';
  import TextAreaForm from '@/components/form/TextAreaForm.vue';
  import SelectInput from '@/components/form/SelectInput.vue';
  import MultipleSelectInput from '@/components/form/MultipleSelectInput.vue';

  const tournamentName     = ref('');
  const adminUpdate        = ref(false);
  const pairingSystem      = ref('Round Robin');
  const boardType          = ref('lichess');
  const winPoints          = ref(1.0);
  const drawPoints         = ref(0.0);
  const losePoints         = ref(0.0);
  const tournamentCategory = ref('classical');
  const playersCsv         = ref('');
  const selectedMethods    = ref([]);

  function onRankingChange(value, checked) {
    if (checked) {
      selectedMethods.value.push(value);
    } else {
      selectedMethods.value = selectedMethods.value.filter(v => v !== value);
    }
  }

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
      playersCsv: playersCsv.value,
      selectedMethods: selectedMethods.value
    });
  }
</script>

<style scope>
  .divider {
    margin-top: 40px;
    margin-bottom: 40px
  }
</style>