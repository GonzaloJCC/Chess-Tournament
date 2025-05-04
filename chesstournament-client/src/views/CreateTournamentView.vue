<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <h1 class="text-center mb-4" data-cy="create-tournament-title">Create a Tournament</h1>
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
              cypress="name-cypress-test"
            />
            <hr class="divider">

            <!-- Admin Update -->
            <CheckboxInput
              id="adminUpdateInput"
              v-model="adminUpdate"
              label="Only administrators can update games"
              helpText="Set to false if users can update games. Otherwise, only administrators can input the results."
              cypress="only_administrative-cypress-test"
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
                { label: 'Round Robin', value: 'SR' },
                { label: 'Swiss', value: 'SW' }
              ]"
              helpText="Select the pairing system (Round Robin, Swiss…)"
              cypress="single_round_robin-cypress-test"
            />
            <hr class="divider">

            <!-- Board Type -->
            <SelectInput
              id="boardTypeInput"
              v-model="boardType"
              label="Board Type"
              :options="[
                { label: 'Lichess', value: 'LIC' },
                { label: 'On the board', value: 'OTB' }
              ]"
              helpText="Games played on lichess or OTB"
              cypress="boardtype-cypress-test"
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
                  step="0.1"
                  cypress="win-points-input"
                />
                <TextInput
                  id="drawPointsInput"
                  v-model.number="drawPoints"
                  class="col"
                  label="Draws"
                  type="number"
                  step="0.1"
                  cypress="draw-points-input"
                />
                <TextInput
                  id="losePointsInput"
                  v-model.number="losePoints"
                  class="col"
                  label="Loses"
                  type="number"
                  step="0.1"
                  cypress="lose-points-input"
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
              cypress="ranking-methods-select"
            />
            <hr class="divider">

            <!-- Tournament category -->
            <SelectInput
              id="tournamentCategoryInput"
              v-model="tournamentCategory"
              label="Tournament Category"
              :options="[
                { label: 'Classical', value: 'CL' },
                { label: 'Rapid', value: 'RA' },
                { label: 'Blitz', value: 'BL' },
                { label: 'Bullet', value: 'BU' }
              ]"
              helpText="Select the tournament category"
              cypress="tournament_speed-cypress-test"
            />
          </fieldset>

          <fieldset class="border rounded p-3 mb-4">
            <legend class="float-none w-auto px-2">Players</legend>

            <!-- Player csv -->
            <TextAreaForm
              id="input_9"
              v-model="playersCsv"
              label="List of players"
              rows="4"
              placeholder="Introduce players using the CSV format (see FAQ for details). Do NOT add trailing spaces"
              helpText="NOTE: The format is explained in the FAQ Page"
              cypress="players-csv-input"
            />
          </fieldset>

          <div
            v-if="error_msg"
            class="alert alert-danger text-center"
            role="alert"
            data-cy="error-message"
          >
            {{ error_msg }}
          </div>
          <button type="submit" class="btn btn-primary w-100" data-cy="submit-tournament-button">Register</button>
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

  import { useTokenStore } from '@/stores/token';
  import { useRouter } from 'vue-router';

  /* Form values */
  const tournamentName     = ref('');
  const adminUpdate        = ref(false);
  const pairingSystem      = ref('SR');
  const boardType          = ref('LIC');
  const winPoints          = ref(2.0);
  const drawPoints         = ref(1.0);
  const losePoints         = ref(0.0);
  const tournamentCategory = ref('CL');
  const playersCsv         = ref('');
  const selectedMethods    = ref([]);

  const error_msg = ref(null)

  /* Session token */
  const tokenStore = useTokenStore();

  /* Router data */
  const router = useRouter();

  /* API URL */
  const APIURL = import.meta.env.VITE_APIURL;

  /* Function to register the tournament */
  const registerTournament = async () => {
    error_msg.value = null;
    
    /* Send the request to the API */
    try
    {
      const result = await fetch(`${APIURL}/api/v1/tournament_create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${tokenStore.token}`
        },
        body: JSON.stringify({
          name: tournamentName.value,
          players: playersCsv.value,
          only_administrative: adminUpdate.value,
          tournament_type: pairingSystem.value,
          tournament_speed: tournamentCategory.value,
          board_type: boardType.value,
          win_points: winPoints.value,
          draw_points: drawPoints.value,
          lose_points: losePoints.value,
          rankingList: selectedMethods.value
        })
      })
      const data = await result.json()
      if (!result.ok)
        throw new Error();
  
      /* All OK, redirect to / */
      router.push('/tournamentdetail/?id=' + data.id);
    }
    catch (error)
    {
      error_msg.value = 'Error creating tournament. Please, check the data provided';
    }

  }
</script>

<style scope>
  .divider {
    margin-top: 40px;
    margin-bottom: 40px
  }
</style>