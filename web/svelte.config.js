import adapter from '@sveltejs/adapter-static';

/** The web app is a static SPA that the control plane serves; index.html is the fallback route. */
/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
		runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
	},
	kit: {
		adapter: adapter({ fallback: 'index.html' })
	}
};

export default config;
