import { defineConfig } from '@playwright/test';
import dotenv from 'dotenv';

// Load .env so running `npx playwright test` or clicking Run uses BASE_URL automatically
dotenv.config();

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:8000';
const webServer = process.env.BASE_URL
  ? undefined
  : {
      command: 'python manage.py runserver 127.0.0.1:8000',
      url: BASE_URL,
      timeout: 120000,
      reuseExistingServer: true,
    };

export default defineConfig({
  testDir: './tests',

  use: {
    baseURL: BASE_URL,
    headless: false,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },
  webServer,
  fullyParallel: false,
});