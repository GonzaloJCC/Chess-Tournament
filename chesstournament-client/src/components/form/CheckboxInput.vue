<template>
  <div class="form-check mb-3">
    <input
      :id="id"
      v-model="local_data"
      class="form-check-input"
      type="checkbox"
    >

    <label
      class="form-check-label fw-bold"
      :for="id"
    >
      {{ label }}
    </label>

    <div class="form-text">
      {{ helpText }}
    </div>
  </div>
</template>

<script setup>
import { watch, ref } from 'vue';

/* Define the input and the output event */
const props = defineProps({
  id:		  	  { type: String, required: true },
  label:		  { type: String, required: true },
  modelValue:	{ required: true },
  helpText: 	{ type: String, default: '' },
});
const emit = defineEmits(['update:modelValue']);

/* Define the local variable and check the updates */
const local_data = ref(props.modelValue);
watch(local_data, v => emit('update:modelValue', v));
watch(() => props.modelValue, v => (local_data.value = v))
</script>

<style scoped>
</style>