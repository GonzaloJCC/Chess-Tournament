<template>
  <div class="mb-3">
    <label
      :for="id"
      class="form-label fw-bold"
    >
      {{ label }}
    </label>

    <select
      v-model="local_data"
      class="form-select"
      :id="id"
      :data-cy="cypress"
    >
      <option
        v-for="current in options"
        :key="current.value"
        :value="current.value"
      >
        {{ current.label }}
      </option> 
    </select>

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
  id:         { type: String, required: true },
  label:      { type: String, required: true },
  modelValue: { required: true },
  options:    { type: Array, default: () => []},
  helpText:   { type: String, default: undefined },
  cypress:    { type: String, default: undefined },
});
const emit = defineEmits(['update:modelValue']);

/* Define the local variable and check the updates */
const local_data = ref(props.modelValue);
watch(local_data, v => emit('update:modelValue', v));
watch(() => props.modelValue, v => (local_data.value = v))
</script>

<style scoped>
</style>