<template>
  <div class="container my-5">
  <h2 class="mb-4">FAQ</h2>
  <div class="accordion" id="faqAccordion">
    <!-- FAQ Item 1 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="headingOne">
        <button class="accordion-button collapsed shadow-sm" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
          How can players update the result of a game?
        </button>
      </h2>
      <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          <p>
            Go to the tournament page, open the "pairing/results" tab, provide de lichess game id in the input field (for lichess games)
            or select the result from the dropdown list (for OTB games) and then click on the 
            <i class="bi bi-send"></i>
            icon.
          </p>
        </div>
      </div>
    </div>

    <!-- FAQ Item 2 -->
    <div class="accordion-item">
      <h2 class="accordion-header" id="headingTwo">
        <button class="accordion-button collapsed shadow-sm" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
          Example 2
        </button>
      </h2>
      <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#faqAccordion">
        <div class="accordion-body">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus metus leo, sollicitudin ut pulvinar a, faucibus non nunc.
          Ut porta nibh sed nunc vehicula, non ornare turpis rutrum. Integer ac urna neque. Maecenas et nulla sit amet ipsum sagittis
          porta eu eget nisi. Sed accumsan tincidunt mauris non tempor. Suspendisse finibus tortor vel libero blandit laoreet. Donec
          accumsan, mi eget tempus elementum, tortor nisl mattis arcu, et pretium mi neque ac sem. Pellentesque posuere velit a ante
          semper tempus.
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