<template>
  <div class="mb-3">
    <label
      :for="id"
      class="form-label fw-bold"
    >
      {{ label }}
    </label>

    <textarea
      :id="id"
      v-model="local_data"
      :rows="rows"
      class="form-control"
      :placeholder="placeholder"
    />

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
modelValue:	  { required: true },
rows:			    { type: String, default: '4' },
placeholder:  { type: String, default: '' },
helpText: 	  { type: String, default: '' },
});
const emit = defineEmits(['update:modelValue']);

/* Define the local variable and check the updates */
const local_data = ref(props.modelValue);
watch(local_data, v => emit('update:modelValue', v));
watch(() => props.modelValue, v => (local_data.value = v))
</script>

<style scope>
</style>