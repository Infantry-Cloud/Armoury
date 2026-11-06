// Acceptance test STORY-1.1 VAL-4 (AC-1, AC-5): the web app is a static SPA.
// ATDD red phase: locked at contract approval. Task T5 activates it by removing `.skip` only.
// Imports are dynamic so the file loads while the skipped test's targets do not exist yet.
import { expect, test } from 'vitest';

test.skip('VAL-4 root layout disables SSR and uses the static adapter', async () => {
	const rootLayout = await import('./+layout');
	const { default: svelteConfig } = await import('../../svelte.config.js');

	expect(rootLayout.ssr).toBe(false);
	expect(svelteConfig.kit?.adapter?.name).toBe('@sveltejs/adapter-static');
});
