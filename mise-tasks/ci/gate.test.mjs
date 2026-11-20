// AC-10: `ci:gate` (the required ci-gate job) fails unless every needed job succeeded.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const GATE = fileURLToPath(new URL('./gate', import.meta.url));

function gate(needs) {
	const env = { ...process.env };
	delete env.ARMOURY_CI_NEEDS;
	if (needs !== undefined) env.ARMOURY_CI_NEEDS = typeof needs === 'string' ? needs : JSON.stringify(needs);
	const result = spawnSync(GATE, [], { encoding: 'utf8', env, timeout: 30_000 });
	return { status: result.status, output: `${result.stdout}${result.stderr}` };
}

const jobs = (results) => Object.fromEntries(Object.entries(results).map(([job, result]) => [job, { result }]));

test('AC-10 ci-gate passes only when every needed job succeeded', () => {
	assert.equal(gate(jobs({ fast: 'success', cluster: 'success', e2e: 'success' })).status, 0);

	for (const result of ['failure', 'skipped', 'cancelled']) {
		const outcome = gate(jobs({ fast: 'success', cluster: result, e2e: 'success' }));
		assert.equal(outcome.status, 1, `${result} must fail the gate`);
		assert.match(outcome.output, /FAILED, not successful: cluster/);
	}

	for (const needs of [undefined, {}, 'not json']) {
		assert.notEqual(gate(needs).status, 0, `ARMOURY_CI_NEEDS=${JSON.stringify(needs)} must fail the gate`);
	}
});
