import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar el dashboard después del login', async ({ page }) => {
    await page.goto('/dashboard/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/dashboard\/?$/);
    await expect(page.getByRole('heading', { name: /hola,/i })).toBeVisible();
  });
});
