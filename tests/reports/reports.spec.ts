import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Reports', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar el dashboard de reportes', async ({ page }) => {
    await page.goto('/reportes/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/reportes\/?$/);
    await expect(page.getByRole('heading', { name: /dashboard de cumplimiento/i })).toBeVisible();
  });

  test('Debe cargar el reporte de cumplimiento', async ({ page }) => {
    await page.goto('/reportes/cumplimiento/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/reportes\/cumplimiento\/?$/);
    await expect(page.getByRole('heading', { name: /reporte de cumplimiento/i })).toBeVisible();
  });
});
