// Playwright smoke tests against a running Okteto deployment, never a local web server.
import { defineConfig } from '@playwright/test';

// The base URL is `mise run dev` (localhost:8080) or the in-cluster URL in `ci:e2e`.
const junitOutput = process.env.PLAYWRIGHT_JUNIT_OUTPUT_FILE;

export default defineConfig({
	testDir: 'e2e',
	forbidOnly: Boolean(process.env.CI),
	reporter: junitOutput ? [['list'], ['junit', { outputFile: junitOutput }]] : [['list']],
	use: {
		baseURL: process.env.ARMOURY_E2E_BASE_URL ?? 'http://localhost:8080'
	}
});
