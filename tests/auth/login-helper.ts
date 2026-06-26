import { Page, expect } from '@playwright/test';

const AUTH_USER = 'DPadmin';
const AUTH_PASSWORD = 'admin2026123';

export async function login(page: Page) {
  await page.goto('/auth/login/?next=/dashboard/');
  await page.getByLabel('Usuario').fill(AUTH_USER);
  await page.getByLabel('Contraseña').fill(AUTH_PASSWORD);
  await Promise.all([
    page.waitForURL(/\/dashboard\/?$/),
    page.getByRole('button', { name: /ingresar/i }).click(),
  ]);
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveURL(/\/dashboard\/?$/);
}
