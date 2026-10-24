// Optional browser smoke test: npm install --no-save playwright && npx playwright install chromium
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(process.env.STILL_TEST_URL||'http://127.0.0.1:3000');
 await page.getByText('Your model, when you’re ready',{exact:true}).waitFor();
 await page.screenshot({path:'docs/still-desktop.png',fullPage:true});
 await page.locator('#sample').click();
 await page.locator('#story-title').getByText('The light at the end of the lane').waitFor();
 await page.locator('#font-size').click();assert(await page.locator('#story-body').evaluate(e=>e.classList.contains('large')));
 await page.locator('#reader .close').click();
 await page.locator('[data-setting="A night train"]').click();
 assert.equal(await page.locator('[data-setting="A night train"]').getAttribute('aria-pressed'),'true');
 await page.locator('#generate').click();await page.locator('#message.error').waitFor();
 assert((await page.locator('#message').textContent()).includes('Could not reach'));
 await page.locator('[data-page="library"]').click();await page.locator('.empty-library').waitFor();
 await page.locator('[data-page="create"]').click();
 await page.locator('#setup-toggle').click();await page.locator('#setup').waitFor();await page.locator('#setup .close').click();
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({path:'docs/still-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);await browser.close();console.log('Desktop and mobile smoke tests passed.');
})().catch(e=>{console.error(e);process.exit(1)});
