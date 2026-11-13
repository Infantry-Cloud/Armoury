// Acceptance test STORY-1.1 VAL-16 (AC-15): `mise run ci` runs `ci:fast`, `ci:cluster` and
// `ci:e2e` in that order, stops at the first failing tier, exits non-zero and names that tier.
// ATDD red phase: locked at contract approval. Task T10 activates it by removing `.skip` only.
// Runs in the fast-tier `test-tasks` gate step and needs no cluster: a `mise` shim first on PATH
// records each call and exits 1 for the tier named by VAL_16_FAIL, 0 otherwise.
// Interface under test: `mise-tasks/ci/_default` runs as a plain executable and calls exactly
// `mise run ci:fast`, `mise run ci:cluster` and `mise run ci:e2e`, one after the other. It prints
// the failing tier's name itself (the shim prints nothing). `ci:build` and `ci:publish` belong to
// `build.yml` and are not called.
// One flat test, no subtests, so the JUnit testcase keeps the planned check name.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const CI = fileURLToPath(new URL('./_default', import.meta.url));
const TIERS = ['ci:fast', 'ci:cluster', 'ci:e2e'];

function shimBin(dir) {
	const bin = join(dir, 'bin');
	mkdirSync(bin);
	const shim = join(bin, 'mise');
	writeFileSync(
		shim,
		'#!/bin/sh\nprintf \'%s\\n\' "$*" >> "$VAL_16_CALLS"\n[ "$*" = "run $VAL_16_FAIL" ] && exit 1\nexit 0\n',
	);
	chmodSync(shim, 0o755);
	return bin;
}

// Runs `mise run ci` with the given tier failing (or none) and returns what happened.
function runCi(dir, bin, failing) {
	const workdir = mkdtempSync(join(dir, 'run-'));
	const calls = join(workdir, 'calls.log');
	const result = spawnSync(CI, [], {
		cwd: workdir,
		encoding: 'utf8',
		env: { ...process.env, PATH: `${bin}${delimiter}${process.env.PATH}`, VAL_16_CALLS: calls, VAL_16_FAIL: failing ?? '' },
		timeout: 60_000,
	});
	const output = `${result.stdout}${result.stderr}`;
	return {
		error: result.error?.code,
		exitedZero: result.status === 0,
		calls: existsSync(calls) ? readFileSync(calls, 'utf8').split('\n').filter(Boolean) : [],
		namesFailingTier: failing === undefined ? null : new RegExp(`(^|[^\\w:-])${failing}($|[^\\w:-])`, 'm').test(output),
	};
}

test.skip('VAL-16 mise run ci runs the CI tiers in order and stops at the first failure', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'val-16-ci-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	const bin = shimBin(dir);

	// No tier fails, then each tier fails in turn: the calls stop at the failing tier.
	const observed = [undefined, ...TIERS].map((failing) => ({ failing, ...runCi(dir, bin, failing) }));
	assert.deepEqual(observed, [
		{ failing: undefined, error: undefined, exitedZero: true, calls: TIERS.map((tier) => `run ${tier}`), namesFailingTier: null },
		...TIERS.map((failing, index) => ({
			failing,
			error: undefined,
			exitedZero: false,
			calls: TIERS.slice(0, index + 1).map((tier) => `run ${tier}`),
			namesFailingTier: true,
		})),
	]);
});
