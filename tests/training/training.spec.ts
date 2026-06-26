import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Training', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la lista de planes de capacitación', async ({ page }) => {
    await page.goto('/capacitaciones/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/capacitaciones\/?$/);
    await expect(page.getByRole('heading', { name: /capacitaciones/i })).toBeVisible();
  });
});
