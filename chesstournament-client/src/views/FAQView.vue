<template>
  <div class="container my-5">
    <h2 class="mb-4">
      FAQ
    </h2>
    <div
      id="faqAccordion"
      class="accordion"
    >
      <!-- FAQ Item 1 -->
      <div class="accordion-item">
        <h2
          id="headingOne"
          class="accordion-header"
        >
          <button
            class="accordion-button collapsed shadow-sm"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseOne"
            aria-expanded="false"
            aria-controls="collapseOne"
          >
            How can players update the result of a game?
          </button>
        </h2>
        <div
          id="collapseOne"
          class="accordion-collapse collapse"
          aria-labelledby="headingOne"
          data-bs-parent="#faqAccordion"
        >
          <div class="accordion-body">
            <p>
              Go to the tournament page, open the "pairing/results" tab, provide de lichess game id in the input field (for lichess games)
              or select the result from the dropdown list (for OTB games) and then click on the 
              <i class="bi bi-send" />
              icon.
            </p>
          </div>
        </div>
      </div>

      <!-- FAQ Item 2 -->
      <div class="accordion-item">
        <h2
          id="headingTwo"
          class="accordion-header"
        >
          <button
            class="accordion-button collapsed shadow-sm"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseTwo"
            aria-expanded="false"
            aria-controls="collapseTwo"
          >
            How can administrators add players to a tournament?
          </button>
        </h2>
        <div
          id="collapseTwo"
          class="accordion-collapse collapse"
          aria-labelledby="headingTwo"
          data-bs-parent="#faqAccordion"
        >
          <div class="accordion-body">
            <p>
              Players are added using the CSV file format. Comma-separated values (CSV) is a text format that uses commas to separate values,
              and newlines to separate records. The first row of the CSV file must contain the column names.
            </p>
            <p>
              The column names must match the fields of the player. The more common fields are: name, email, lichess_username.
            </p>
            <p>
              For lichess tournaments, the lichess_username is required. For OTB tournaments, the name and email are required.
            </p>
            <p>
              For lichess tournaments, the lichess_username will be checked again lichess database and the player ranking will be retrieved.
              For OTB tournaments, the email will be used as user password.
            </p>
            <p>
              Example lichess tournament:
              <br>
              <code>
                lichess_username<br>
                username1<br>
                username2<br>
                username3<br>
              </code>
            </p>
            <p>
              Example OTB tournament:
              <br>
              <code>
                name, email<br>
                name1 familyname1, name1@gmail.com<br>
                name2 familyname2, name2@gmail.com<br>
                name3 familyname3, name3@gmail.com<br>
              </code>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scope>
</style>