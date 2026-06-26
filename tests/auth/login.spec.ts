import { test, expect } from '@playwright/test';

test.describe('Autenticación', () => {

  test('Debe cargar la página de login', async ({ page }) => {
    await page.goto('/auth/login/?next=/dashboard/');

    await expect(page.getByRole('heading', { name: /iniciar sesión/i }))
      .toBeVisible();

    if (process.env.PLAYWRIGHT_KEEP_OPEN === '1') {
      await page.pause();
    }
  });

  test('Debe iniciar sesión correctamente', async ({ page }) => {
    await page.goto('/auth/login/?next=/dashboard/');

    await page.getByLabel('Usuario').fill('DPadmin');
    await page.getByLabel('Contraseña').fill('admin2026123');

    await page.getByRole('button', { name: /ingresar/i }).click();

    await expect(page).toHaveURL(/\/dashboard\/?$/);

    if (process.env.PLAYWRIGHT_KEEP_OPEN === '1') {
      await page.pause();
    }
  });

});