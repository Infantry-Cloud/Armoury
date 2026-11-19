import { defineConfig } from '@playwright/test';

// Runs against an Okteto deployment: `mise run dev` (localhost:8080) or the in-cluster URL in
// `ci:e2e`. There is no webServer, so the run fails when no deployment is reachable.
const junitOutput = process.env.PLAYWRIGHT_JUNIT_OUTPUT_FILE;

export default defineConfig({
	testDir: 'e2e',
	forbidOnly: Boolean(process.env.CI),
	reporter: junitOutput ? [['list'], ['junit', { outputFile: junitOutput }]] : [['list']],
	use: {
		baseURL: process.env.ARMOURY_E2E_BASE_URL ?? 'http://localhost:8080'
	}
});
