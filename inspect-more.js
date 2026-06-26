const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const base = 'https://jaguevara.pythonanywhere.com';
  try {
    console.log('login...');
    await page.goto(`${base}/auth/login/?next=/dashboard/`, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.getByLabel('Usuario').fill('DPadmin');
    await page.getByLabel('Contraseña').fill('admin2026123');
    await Promise.all([
      page.waitForURL('**/dashboard/**', { timeout: 20000 }),
      page.getByRole('button', { name: /ingresar/i }).click(),
    ]);
    console.log('logged in', page.url());
    const paths = [
      'usuarios/',
      'usuarios/roles/',
      'usuarios/roles/nuevo/',
      'evaluaciones/',
      'evaluaciones/nueva/',
      'evaluaciones/1/preguntas/',
      'evaluaciones/1/asignar/',
      'evaluaciones/rendir/1/',
      'evaluaciones/resultado/1/',
      'analitica/brechas/',
      'capacitaciones/',
      'capacitaciones/1/asignar/',
      'capacitaciones/asignacion/1/asistencia/',
      'reportes/',
      'reportes/cumplimiento/?export=pdf',
      'bitacora/',
      'trabajadores/',
      'auth/logout/'
    ];
    for (const path of paths) {
      const url = `${base}/${path}`;
      try {
        console.log('---', url, '---');
        const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
        console.log('status', response && response.status());
        console.log('url', page.url());
        console.log('title', await page.title());
        console.log('h1', await page.locator('h1').allTextContents());
        console.log('body snippet', (await page.locator('body').textContent() || '').slice(0,200).replace(/\s+/g,' '));
      } catch (err) {
        console.log('ERROR', err.message);
      }
    }
  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
