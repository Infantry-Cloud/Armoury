// Acceptance test STORY-1.1 VAL-10 (AC-9): the web app loads from an Okteto deployment made by
// `mise run dev` or `mise run ci:e2e`.
// ATDD red phase: locked at contract approval. Task T9 activates it by removing `.skip` only.
// The base URL comes from playwright.config.ts: ARMOURY_E2E_BASE_URL, default
// http://localhost:8080 (`mise run e2e` on the workstation). Inside `ci:e2e`, `okteto test` runs
// this same spec and configuration with ARMOURY_E2E_BASE_URL set to the in-cluster service URL.
// There is no `webServer`, so the test fails when no deployment is reachable.
import { expect, test } from '@playwright/test';

// SSR is off, so the title alone comes from app.html even when the JavaScript bundle fails.
// The visible product name proves the client app rendered; page errors fail the test.
test('loads the web app @VAL-10', async ({ page }) => {
	const pageErrors: string[] = [];
	page.on('pageerror', (error) => pageErrors.push(error.message));

	const response = await page.goto('/');

	expect(response?.status()).toBe(200);
	await expect(page).toHaveTitle(/Armoury/);
	await expect(page.getByText('Armoury').first()).toBeVisible();
	expect(pageErrors).toEqual([]);
});
