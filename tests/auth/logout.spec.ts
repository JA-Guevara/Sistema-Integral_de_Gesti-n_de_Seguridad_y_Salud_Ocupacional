import { test, expect } from '@playwright/test';
import { login } from './login-helper';

test.describe('Logout', () => {
  test('Debe cerrar sesión desde el dashboard', async ({ page }) => {
    await login(page);
    await page.goto('/dashboard/');
    await page.waitForLoadState('networkidle');

    const accountToggle = page.getByRole('button', { name: /Diego Alejandro Pereira Negrete/i }).first();
    await expect(accountToggle).toBeVisible();
    await accountToggle.click();

    const logoutButton = page.getByRole('button', { name: /cerrar sesión/i }).first();
    await expect(logoutButton).toBeVisible();

    await Promise.all([
      page.waitForURL(/\/auth\/login\/?/),
      logoutButton.click(),
    ]);

    await expect(page.getByRole('heading', { name: /iniciar sesión/i })).toBeVisible();
  });
});
