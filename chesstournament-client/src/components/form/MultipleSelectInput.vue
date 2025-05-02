<template>
  <div class="mb-4">
    <h6
      v-if="title"
      class="fw-bold"
    >
      {{ title }}
    </h6>

    <label
      v-if="label"
      class="form-text mb-2"
    >
      {{ label }}
    </label>

    <div
      v-for="current in options"
      :key="current.value"
      class="form-check"
    >
      <input
        class="form-check-input"
        type="checkbox"
        :id="`${idPrefix}_${current.value}`"
        :checked="local_data.includes(current.value)"
        @change="onCheck(current.value, $event.target.checked)"
      >

      <label
        class="form-check-label"
        :for="`${idPrefix}_${current.value}`"
      >
        {{ current.label }} {{ current.value }}
      </label>
    </div>

    <div
      class="mt-2"
    >
      <small
        v-if="helpText"
        class="form-text fst-italic"
      >
        {{ helpText }}: [ {{ local_data.join(', ') }} ]
      </small>
    </div>
  </div>
</template>

<script setup>
import { watch, ref } from 'vue';

/* Define the input and the output event */
const props = defineProps({
  idPrefix: { type: String, required: true },
  title: { type: String, default: undefined},
  label: { type: String, default: undefined },
  modelValue: { required: true },
  options: { type: Array, default: () => []},
  helpText: { type: String, default: undefined }
});
const emit = defineEmits(['update:modelValue']);

/* Define the local variable and check the updates */
const local_data = ref([...props.modelValue]);

watch(() => props.modelValue, v => {
  local_data.value = [...v];
});

function onCheck(value, checked) {
  if (checked) {
    local_data.value.push(value);
  } else {
    local_data.value = local_data.value.filter(v => v !== value);
  }
  emit('update:modelValue', [...local_data.value]);
}
</script>

<style scoped>
</style>