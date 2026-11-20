// AC-3/AC-4: `check` runs the fast tier then the cluster tier in order, stops at the first failing step and names it.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, copyFileSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const FAST = ['pins', 'rust', 'test-rust', 'web', 'chart', 'test-tasks'];
const CLUSTER = ['api', 'test-db', 'test-tasks-cluster', 'codeql'];

// A copy of the two runners next to shim steps that record their name and fail when named in CHECK_FAIL.
function stepsDir(dir) {
	for (const runner of ['_default', 'fast']) {
		copyFileSync(fileURLToPath(new URL(`./${runner}`, import.meta.url)), join(dir, runner));
		chmodSync(join(dir, runner), 0o755);
	}
	for (const step of [...FAST, ...CLUSTER]) {
		writeFileSync(join(dir, step), `#!/bin/sh\necho ${step} >> "$CHECK_CALLS"\n[ "$CHECK_FAIL" = ${step} ] && exit 1\nexit 0\n`);
		chmodSync(join(dir, step), 0o755);
	}
}

function run(dir, runner, failing) {
	const calls = join(dir, `calls-${runner}-${failing ?? 'none'}.log`);
	const result = spawnSync(join(dir, runner), [], {
		encoding: 'utf8',
		env: { ...process.env, CHECK_CALLS: calls, CHECK_FAIL: failing ?? '' },
		timeout: 30_000,
	});
	return {
		status: result.status,
		calls: existsSync(calls) ? readFileSync(calls, 'utf8').split('\n').filter(Boolean) : [],
		namesStep: failing === undefined || `${result.stdout}${result.stderr}`.includes(`FAILED at step '${failing}'`),
	};
}

test('AC-3 check runs every step in tier order and stops at the first failure', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'check-gate-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	stepsDir(dir);

	assert.deepEqual(run(dir, 'fast'), { status: 0, calls: FAST, namesStep: true });
	assert.deepEqual(run(dir, '_default'), { status: 0, calls: [...FAST, ...CLUSTER], namesStep: true });

	const all = [...FAST, ...CLUSTER];
	for (const [index, failing] of all.entries()) {
		assert.deepEqual(run(dir, '_default', failing), { status: 1, calls: all.slice(0, index + 1), namesStep: true }, failing);
	}
});
