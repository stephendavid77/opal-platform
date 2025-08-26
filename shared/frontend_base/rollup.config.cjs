const babel = require('@rollup/plugin-babel');
const resolve = require('@rollup/plugin-node-resolve');
const commonjs = require('@rollup/plugin-commonjs');
const postcss = require('rollup-plugin-postcss');

module.exports = {
  input: 'src/index.js', // Your main entry file for the library
  output: [
    {
      file: 'dist/index.js',
      format: 'es', // ES module format
      sourcemap: true,
    },
    {
      file: 'dist/index.cjs',
      format: 'cjs', // CommonJS format
      sourcemap: true,
    },
  ],
  plugins: [
    resolve(), // So Rollup can find `node_modules`
    babel({
      babelHelpers: 'runtime',
      presets: ['@babel/preset-env', '@babel/preset-react'],
      plugins: [
        require.resolve('@babel/plugin-transform-runtime'),
        require.resolve('@babel/plugin-transform-react-jsx') // Add this plugin
      ],
      exclude: 'node_modules/**',
    }),
    commonjs(), // So Rollup can convert `commonjs` to `es` modules
    postcss({
      extract: false, // Extract CSS to a separate file
      modules: true, // Enable CSS modules
    }),
  ],
  external: ['react', 'react-dom', 'react-bootstrap', 'bootstrap'], // Mark peer dependencies as external
};
