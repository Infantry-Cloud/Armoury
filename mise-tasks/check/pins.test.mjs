// Acceptance test STORY-1.1 VAL-5 (AC-2): the pin checker rejects every floating reference.
// ATDD red phase: locked at contract approval. Task T7 activates it by removing `.skip` only.
// Run with `node --test mise-tasks/check/pins.test.mjs` (a step of `mise run check`).
// The file is not executable, so mise does not treat it as a task.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const PINS = fileURLToPath(new URL('./pins', import.meta.url));
const REPO_ROOT = fileURLToPath(new URL('../..', import.meta.url));
const SHA = 'a'.repeat(40);
const DIGEST = `sha256:${'b'.repeat(64)}`;

// A minimal tree in which every reference is pinned exactly.
const CLEAN = {
	'mise.toml': '[tools]\nnode = "24.11.1"\nrust = "1.91.1"\n',
	'mise.lock': '# lock\n',
	'Cargo.toml':
		'[workspace]\nresolver = "3"\nmembers = ["agent-proto"]\n\n[workspace.dependencies]\nprost = "=0.14.1"\ntokio = { version = "=1.48.0", features = ["full"] }\n',
	'Cargo.lock': '# lock\n',
	'web/package.json': '{\n  "devDependencies": { "vite": "7.2.2", "vitest": "4.0.8" }\n}\n',
	'web/package-lock.json': '{}\n',
	'control-plane/Dockerfile': `FROM docker.io/library/rust:1.91.1-bookworm@${DIGEST} AS build\n`,
	'.github/workflows/ci.yml': `jobs:\n  check:\n    steps:\n      - uses: actions/checkout@${SHA} # v5\n`,
};

// One defect per case: the file it touches, its new content (null deletes it), and the file
// the checker must name.
const DEFECTS = [
	['a latest tool', 'mise.toml', '[tools]\nnode = "latest"\n', 'mise.toml'],
	['a non-exact mise tool version', 'mise.toml', '[tools]\nnode = "24"\n', 'mise.toml'],
	['a FROM without a digest', 'control-plane/Dockerfile', 'FROM docker.io/library/rust:1.91.1-bookworm AS build\n', 'control-plane/Dockerfile'],
	['an action ref that is not a SHA', '.github/workflows/ci.yml', 'jobs:\n  check:\n    steps:\n      - uses: actions/checkout@v5\n', '.github/workflows/ci.yml'],
	['a Cargo requirement without =', 'Cargo.toml', '[workspace]\nresolver = "3"\n\n[workspace.dependencies]\nprost = "0.14.1"\n', 'Cargo.toml'],
	['a ^ npm range', 'web/package.json', '{ "devDependencies": { "vite": "^7.2.2" } }\n', 'web/package.json'],
	['a ~ npm range', 'web/package.json', '{ "devDependencies": { "vite": "~7.2.2" } }\n', 'web/package.json'],
	['a missing Cargo.lock', 'Cargo.lock', null, 'Cargo.lock'],
	['a missing web/package-lock.json', 'web/package-lock.json', null, 'web/package-lock.json'],
	['a missing mise.lock', 'mise.lock', null, 'mise.lock'],
];

function fixture(overrides = {}) {
	const root = mkdtempSync(join(tmpdir(), 'val-5-pins-'));
	for (const [path, content] of Object.entries({ ...CLEAN, ...overrides })) {
		if (content === null) continue;
		mkdirSync(dirname(join(root, path)), { recursive: true });
		writeFileSync(join(root, path), content);
	}
	return root;
}

function runPins(root) {
	return spawnSync(PINS, [root], { encoding: 'utf8' });
}

test.skip('VAL-5 pins check rejects floating references', async (t) => {
	for (const [name, path, content, named] of DEFECTS) {
		await t.test(`rejects ${name}`, (st) => {
			const root = fixture({ [path]: content });
			st.after(() => rmSync(root, { recursive: true, force: true }));
			const result = runPins(root);

			assert.equal(result.status, 1);
			assert.match(result.stdout + result.stderr, new RegExp(named.replaceAll('.', '\\.')));
		});
	}

	await t.test('accepts a fully pinned tree', (st) => {
		const root = fixture();
		st.after(() => rmSync(root, { recursive: true, force: true }));

		assert.equal(runPins(root).status, 0);
	});

	await t.test('accepts this repository', () => {
		assert.equal(runPins(REPO_ROOT).status, 0);
	});
});
