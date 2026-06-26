import { test, expect } from '@playwright/test';
import { login } from '../auth/login-helper';

test.describe('Usuarios', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Debe cargar la lista de usuarios', async ({ page }) => {
    await page.goto('/usuarios/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/usuarios\/?$/);
    await expect(page.getByRole('heading', { name: /usuarios/i })).toBeVisible();
  });

  test('Debe cargar la lista de roles', async ({ page }) => {
    await page.goto('/usuarios/roles/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/usuarios\/roles\/?$/);
    await expect(page.getByRole('heading', { name: /roles y permisos/i })).toBeVisible();
  });

  test('Debe cargar la página de nuevo rol', async ({ page }) => {
    await page.goto('/usuarios/roles/nuevo/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/usuarios\/roles\/nuevo\/?$/);
    await expect(page.getByRole('heading', { name: /nuevo rol/i })).toBeVisible();
  });
});
