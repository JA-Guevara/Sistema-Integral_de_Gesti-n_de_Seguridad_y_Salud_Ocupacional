import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Analytics', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la página de brechas de competencia', async ({ page }) => {
    await page.goto('/analitica/brechas/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/analitica\/brechas\/?$/);
    await expect(page.getByRole('heading', { name: /brechas de competencia/i })).toBeVisible();
  });
});
