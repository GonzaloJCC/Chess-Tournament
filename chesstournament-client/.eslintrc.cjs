/* eslint-env node */
// require('@rushstack/eslint-patch/modern-module-resolution')

// module.exports = {
//   root: true,
//   'extends': [
//     'plugin:vue/vue3-essential',
//     'eslint:recommended',
//     '@vue/eslint-config-prettier'
//   ],
//   overrides: [
//     {
//       files: [
//         '**/__tests__/*.{cy,spec}.{js,ts,jsx,tsx}',
//         'cypress/e2e/**/*.{cy,spec}.{js,ts,jsx,tsx}'
//       ],
//       'extends': [
//         'plugin:cypress/recommended'
//       ]
//     }
//   ],
//   parserOptions: {
//     ecmaVersion: 'latest'
//   }
// }

module.exports = {
  extends: [
    'plugin:vue/vue3-recommended',
  ],
  rules: {
    'vue/no-unused-vars': 'error'
  }
}