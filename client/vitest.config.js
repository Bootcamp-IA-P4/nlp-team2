import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup/setupTests.js'],
    globals: true,
    include: ['tests/**/*.test.{js,jsx}', 'tests/**/*.spec.{js,jsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      exclude: [
        'node_modules/**',
        'tests/setup/**',
        'coverage/**',
        '**/*.config.{js,ts}',
        '**/*.test.{js,jsx}',
        '**/*.spec.{js,jsx}',
        'public/**',
        'dist/**'
      ],
      include: [
        'src/**/*.{js,jsx,ts,tsx}'
      ],
      all: true,
      skipFull: false,
      thresholds: {
        global: {
          branches: 60,
          functions: 60,
          lines: 60,
          statements: 60
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});
