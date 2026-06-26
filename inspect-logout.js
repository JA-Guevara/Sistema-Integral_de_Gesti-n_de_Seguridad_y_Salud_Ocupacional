const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const base = 'https://jaguevara.pythonanywhere.com';
  try {
    await page.goto(`${base}/auth/login/?next=/dashboard/`, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.getByLabel('Usuario').fill('DPadmin');
    await page.getByLabel('Contraseña').fill('admin2026123');
    await Promise.all([
      page.waitForURL('**/dashboard/**', { timeout: 20000 }),
      page.getByRole('button', { name: /ingresar/i }).click(),
    ]);
    await page.waitForLoadState('networkidle');

    const logoutForm = page.locator('form[action="/auth/logout/"]').first();
    console.log('logout form count', await logoutForm.count());
    console.log('logout form visible', await logoutForm.isVisible());
    console.log('logout form outerHTML', await logoutForm.evaluate(el => el.outerHTML));

    const triggerHtml = await page.evaluate(() => {
      const form = document.querySelector('form[action="/auth/logout/"]');
      if (!form) return null;
      let el = form.parentElement;
      while (el) {
        if (el.classList.contains('dropdown')) break;
        el = el.parentElement;
      }
      if (!el) return null;
      const toggle = el.querySelector('[data-bs-toggle="dropdown"], .dropdown-toggle, button');
      return toggle ? toggle.outerHTML : null;
    });
    console.log('detected trigger outerHTML', triggerHtml);

    const visibleButtons = await page.locator('button:visible').all();
    console.log('visible button count', visibleButtons.length);
    for (let i = 0; i < visibleButtons.length; i++) {
      const outer = await visibleButtons[i].evaluate(el => el.outerHTML);
      console.log(`visible button ${i}: ${outer}`);
    }

    const visibleLinks = await page.locator('a:visible').all();
    console.log('visible link count', visibleLinks.length);
    for (let i = 0; i < Math.min(visibleLinks.length, 20); i++) {
      const outer = await visibleLinks[i].evaluate(el => el.outerHTML);
      console.log(`visible link ${i}: ${outer}`);
    }
  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
