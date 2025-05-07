<template>
  <div class="mb-3">
    <label
      :for="id"
      class="form-label fw-bold"
    >
      {{ label }}
    </label>

    <input
      :id="id"
      v-model="local_data"
      :type="type"
      :step="step"
      class="form-control"
      :placeholder="placeholder"
      :data-cy="cypress"
    >

    <div
      v-if="helpText"
      class="form-text fst-italic"
    >
      {{ helpText }}
    </div>
  </div>
</template>

<script setup>
import { watch, ref } from 'vue';

/* Define the input and the output event */
const props = defineProps({
  id:			      { type: String, required: true },
  label:		    { type: String, required: true },
  modelValue:	  { type: String, required: true },
  type:			    { type: String, default: 'text' },
  step:         { type: String, default: undefined },
  placeholder:  { type: String, default: '' },
  helpText: 	  { type: String, default: '' },
  cypress:      { type: String, default: undefined },
});
const emit = defineEmits(['update:modelValue']);

/* Define the local variable and check the updates */
const local_data = ref(props.modelValue);
watch(local_data, v => emit('update:modelValue', v));
watch(() => props.modelValue, v => (local_data.value = v))
</script>

<style scope>
</style>