const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    await page.goto('https://jaguevara.pythonanywhere.com/auth/login/?next=/dashboard/');
    await page.getByLabel('Usuario').fill('DPadmin');
    await page.getByLabel('Contraseña').fill('admin2026123');
    await page.getByRole('button', { name: /ingresar/i }).click();
    await page.waitForURL('**/dashboard/**', { timeout: 20000 });
    console.log('dashboard url', page.url());
    console.log('dashboard h1', await page.locator('h1').allTextContents());
    console.log('dashboard h2', await page.locator('h2').allTextContents());
    const pages = ['bitacora','reportes','reportes/cumplimiento','capacitaciones','evaluaciones','usuarios','trabajadores'];
    for (const path of pages) {
      const url = 'https://jaguevara.pythonanywhere.com/' + path + '/';
      console.log('---', url, '---');
      await page.goto(url);
      await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
      console.log('url', page.url());
      console.log('h1', await page.locator('h1').allTextContents());
      console.log('h2', await page.locator('h2').allTextContents());
      const body = await page.locator('body').textContent();
      console.log('body snippet', body ? body.slice(0,300).replace(/\s+/g,' ') : '');
    }
  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
