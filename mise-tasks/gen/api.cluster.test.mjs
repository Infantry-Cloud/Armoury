// Acceptance test STORY-1.1 VAL-7 (AC-6): gen:api is repeatable, needs no Java and no local
// container runtime, runs no VCS command, and the `api` drift step names an edited generated file.
// ATDD red phase: locked at contract approval. Task T4 activates it by removing `.skip` only.
// Runs in the cluster-tier `test-tasks-cluster` gate step (node:test over
// `mise-tasks/**/*.cluster.test.mjs`). It needs a working Okteto context: the mise environment
// provides `okteto`, Node and the site values (ARMOURY_OKTETO_CONTEXT, ARMOURY_NAMESPACE).
// Interface under test:
//   mise-tasks/gen/api [ROOT]    generate from ROOT/api/openapi.yaml into ROOT, at the same
//                                relative paths as the committed output (default ROOT: the repo).
//                                The Rust types come from an `okteto test` container whose
//                                `artifacts` return the files (D7); the TS types come from
//                                `openapi-typescript`.
//   mise-tasks/check/api [ROOT]  generate ROOT's spec into a temporary directory and compare it
//                                with ROOT's committed output; exit 1 names each differing,
//                                missing or extra file by its path relative to ROOT
// Both tasks run no VCS command, and no process they start may run one. Okteto 3.25.0 runs the
// `git` binary for repository metadata when it works inside a Git repository
// (`pkg/repository.LocalGit`), so run `okteto test` from a temporary directory outside the
// repository; otherwise the `git` shim below records the call (correct red).
// The test copies only `api/openapi.yaml`; a spec split into `$ref` files needs Correct Course.
// Budget: seven `okteto test` runs (three by `gen:api`, four inside `check/api`); each run times
// out after five minutes. Record the step time against the budget in docs/agent-readiness.md.
// One flat test, no subtests, so the JUnit testcase keeps the planned check name.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import {
	appendFileSync,
	chmodSync,
	copyFileSync,
	existsSync,
	mkdirSync,
	mkdtempSync,
	readFileSync,
	readdirSync,
	rmSync,
	writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join, relative } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const GEN_API = fileURLToPath(new URL('./api', import.meta.url));
const CHECK_API = fileURLToPath(new URL('../check/api', import.meta.url));
const REPO_ROOT = fileURLToPath(new URL('../..', import.meta.url));
const SPEC = join('api', 'openapi.yaml');

// Shims first on PATH: each records its call and fails. The contract names `java`, `git` and
// `jj`; `docker`, `podman` and `buildx` catch a local container runtime (AC-6).
const FORBIDDEN = ['java', 'git', 'jj', 'docker', 'podman', 'buildx'];

function shimBin(dir) {
	const bin = join(dir, 'bin');
	mkdirSync(bin);
	for (const tool of FORBIDDEN) {
		const shim = join(bin, tool);
		writeFileSync(shim, `#!/bin/sh\necho "${tool} $*" >> "${join(dir, 'calls.log')}"\nexit 127\n`);
		chmodSync(shim, 0o755);
	}
	return bin;
}

function rootWithSpec(dir, name) {
	const root = join(dir, name);
	mkdirSync(join(root, 'api'), { recursive: true });
	copyFileSync(join(REPO_ROOT, SPEC), join(root, SPEC));
	return root;
}

function run(command, root, bin) {
	return spawnSync(command, [root], {
		encoding: 'utf8',
		env: { ...process.env, PATH: `${bin}${delimiter}${process.env.PATH}` },
		timeout: 300_000,
	});
}

// Exit status plus any spawn error (missing task, timeout), so a hang cannot look like a pass.
function outcome(result) {
	return { status: result.status, error: result.error?.code };
}

// Relative path -> SHA-256 of every generated file under root (the spec itself excluded).
function generatedTree(root) {
	const entries = readdirSync(root, { recursive: true, withFileTypes: true })
		.filter((entry) => entry.isFile())
		.map((entry) => relative(root, join(entry.parentPath, entry.name)))
		.filter((path) => path !== SPEC)
		.sort();
	return Object.fromEntries(
		entries.map((path) => [path, createHash('sha256').update(readFileSync(join(root, path))).digest('hex')]),
	);
}

function escapeRegExp(text) {
	return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test.skip('VAL-7 gen:api is repeatable and the api step names an edited generated file', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'val-7-gen-api-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	const bin = shimBin(dir);
	const first = rootWithSpec(dir, 'first');
	const second = rootWithSpec(dir, 'second');

	const firstRun = run(GEN_API, first, bin);
	assert.deepEqual(outcome(firstRun), { status: 0, error: undefined }, firstRun.stderr);
	const firstTree = generatedTree(first);

	const rerun = run(GEN_API, first, bin);
	assert.deepEqual(outcome(rerun), { status: 0, error: undefined }, rerun.stderr);
	assert.deepEqual(generatedTree(first), firstTree, 'a second run in place gives identical output');

	const secondRun = run(GEN_API, second, bin);
	assert.deepEqual(outcome(secondRun), { status: 0, error: undefined }, secondRun.stderr);
	assert.deepEqual(generatedTree(second), firstTree, 'a run in another copy gives identical output');

	const paths = Object.keys(firstTree);
	assert.ok(paths.some((path) => path.endsWith('.rs')), 'Rust server types are generated');
	assert.ok(paths.some((path) => path.endsWith('.ts')), 'TS types are generated');

	assert.deepEqual(outcome(run(CHECK_API, REPO_ROOT, bin)), { status: 0, error: undefined }, 'committed output matches the spec');
	assert.deepEqual(outcome(run(CHECK_API, first, bin)), { status: 0, error: undefined }, 'fresh output matches its own spec');

	const edited = paths.filter((path) => path.endsWith('.rs'))[0];
	appendFileSync(join(first, edited), '\n// hand edit\n');
	const drift = run(CHECK_API, first, bin);
	assert.deepEqual(outcome(drift), { status: 1, error: undefined }, 'an edited generated file fails the api step');
	assert.match(`${drift.stdout}${drift.stderr}`, new RegExp(escapeRegExp(edited)));

	const deleted = paths.filter((path) => path.endsWith('.ts'))[0];
	rmSync(join(second, deleted));
	const missing = run(CHECK_API, second, bin);
	assert.deepEqual(outcome(missing), { status: 1, error: undefined }, 'a deleted generated file fails the api step');
	assert.match(`${missing.stdout}${missing.stderr}`, new RegExp(escapeRegExp(deleted)));

	const calls = existsSync(join(dir, 'calls.log')) ? readFileSync(join(dir, 'calls.log'), 'utf8') : '';
	assert.equal(calls, '', `${FORBIDDEN.join(', ')} are never called`);
});
