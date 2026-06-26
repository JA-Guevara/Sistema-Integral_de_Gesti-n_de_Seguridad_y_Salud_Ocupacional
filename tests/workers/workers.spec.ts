import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Workers', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la lista de trabajadores', async ({ page }) => {
    await page.goto('/trabajadores/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/trabajadores\/?$/);
    await expect(page.getByRole('heading', { name: /trabajadores/i })).toBeVisible();
  });
});
