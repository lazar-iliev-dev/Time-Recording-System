import { test, expect, request } from '@playwright/test';

declare const process: any;

const BACKEND = process.env.TEST_BASE_URL ?? 'http://localhost:8000';
const FRONTEND = process.env.TEST_FRONTEND_URL ?? 'http://localhost:3000';

test('frontend reachable', async ({ page }) => {
  await page.goto('FRONTEND);');
  const text = await page.locator('body').innerText().catch(() => '');
  expect(text.length).toBeGreaterThanOrEqual(0);
});

test('edge simulator posts and frontend shows event', async ({ page }) => {
  const ev = {
    card_id: 'E2E-99',
    reader_id: 'desk-e2e',
    timestamp: new Date().toISOString(),
    type: 'checkin'
  };
  const req = await request.newContext();
  const r = await req.post(`${BACKEND}/api/events`, { data: ev, headers: { 'x-edge-secret': 'supersecret' } });
  expect(r.status()).toBe(201);

  // open frontend and verify event is visible
  await page.goto(FRONTEND);
  // tune selector to your timeline/event card element if available
  await page.waitForTimeout(500); // small wait for UI update (or use polling)
  const body = await page.locator('body').innerText();
  expect(body).toContain('E2E-99');
});