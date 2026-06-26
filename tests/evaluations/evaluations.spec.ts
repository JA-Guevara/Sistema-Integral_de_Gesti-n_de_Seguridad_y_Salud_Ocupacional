import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Evaluations', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la lista de evaluaciones', async ({ page }) => {
    await page.goto('/evaluaciones/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/evaluaciones\/?$/);
    await expect(page.getByRole('heading', { name: /evaluaciones/i })).toBeVisible();
  });

  test('Debe cargar la página de nueva evaluación', async ({ page }) => {
    await page.goto('/evaluaciones/nueva/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/evaluaciones\/nueva\/?$/);
    await expect(page.getByRole('heading', { name: /nueva evaluación/i })).toBeVisible();
  });
});
