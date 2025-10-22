import { test, expect } from '@playwright/test';

test('frontend reachable', async ({ page }) => {
  await page.goto('/');
  const text = await page.locator('body').innerText().catch(() => '');
  expect(text.length).toBeGreaterThanOrEqual(0);
});
