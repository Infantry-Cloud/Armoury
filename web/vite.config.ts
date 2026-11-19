import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	test: {
		expect: { requireAssertions: true },
		environment: 'node',
		// Playwright specs in e2e/ run against a deployment, never under Vitest.
		include: ['src/**/*.test.ts']
	}
});
