import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Audit', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la bitácora', async ({ page }) => {
    await page.goto('/bitacora/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/bitacora\/?$/);
    await expect(page.getByRole('heading', { name: /bitácora del sistema/i })).toBeVisible();
  });
});
