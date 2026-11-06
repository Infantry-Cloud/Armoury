// Acceptance test STORY-1.1 VAL-10 (AC-9): the web app loads from the Skaffold deployment.
// ATDD red phase: locked at contract approval. Task T9 activates it by removing `.skip` only.
// The base URL comes from playwright.config.ts (localhost:8080); there is no `webServer`,
// so the test fails when no deployment is reachable.
import { expect, test } from '@playwright/test';

test.skip('loads the web app @VAL-10', async ({ page }) => {
	const response = await page.goto('/');

	expect(response?.status()).toBe(200);
	await expect(page).toHaveTitle(/Armoury/);
});
