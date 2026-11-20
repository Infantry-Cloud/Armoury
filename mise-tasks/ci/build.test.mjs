// AC-11/AC-14: `ci:build` builds both images with an explicit Okteto context and namespace and outputs their digests.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const BUILD = fileURLToPath(new URL('./build', import.meta.url));
const DIGEST = `sha256:${'a'.repeat(64)}`;

// Shims that answer the calls `ci:build` reads output from and record every call.
const SHIMS = {
	okteto: `case "$1 $2" in
  "context show") echo '{"registry":"registry.invalid"}' ;;
  "registrytoken get") cat >/dev/null; echo '{"Username":"u","Secret":"s"}' ;;
esac`,
	crane: `case "$1" in
  digest) echo ${DIGEST} ;;
  auth) cat >/dev/null ;;
esac`,
	helm: '',
};

function shimBin(dir) {
	const bin = join(dir, 'bin');
	mkdirSync(bin);
	for (const [tool, body] of Object.entries(SHIMS)) {
		const shim = join(bin, tool);
		writeFileSync(shim, `#!/bin/sh\necho "${tool} $*" >> "$BUILD_CALLS"\n${body}\nexit 0\n`);
		chmodSync(shim, 0o755);
	}
	return bin;
}

test('AC-11 ci:build builds both images in the explicit context and outputs their digests', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'ci-build-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	const calls = join(dir, 'calls.log');
	const output = join(dir, 'github-output');
	const result = spawnSync(BUILD, [], {
		encoding: 'utf8',
		env: {
			...process.env,
			PATH: `${shimBin(dir)}${delimiter}${process.env.PATH}`,
			ARMOURY_OKTETO_CONTEXT: 'okteto-probe',
			ARMOURY_NAMESPACE: 'namespace-probe',
			BUILD_CALLS: calls,
			GITHUB_OUTPUT: output,
			RUNNER_TEMP: dir,
		},
		timeout: 60_000,
	});
	assert.equal(result.status, 0, `${result.stdout}${result.stderr}`);

	const recorded = readFileSync(calls, 'utf8').split('\n').filter(Boolean);
	const builds = recorded.filter((call) => call.startsWith('okteto build '));
	assert.deepEqual(builds.map((call) => call.split(' ')[2]), ['control-plane', 'agent']);
	for (const call of builds) {
		assert.match(call, / --context okteto-probe /);
		assert.match(call, / --namespace namespace-probe /);
	}
	assert.ok(recorded.some((call) => call.startsWith('helm package charts/armoury')), 'the chart is packaged');

	assert.ok(existsSync(output), 'GITHUB_OUTPUT is written');
	assert.deepEqual(readFileSync(output, 'utf8').split('\n').filter(Boolean).sort(), [
		`agent_image=registry.invalid/namespace-probe/armoury-agent@${DIGEST}`,
		`control_plane_image=registry.invalid/namespace-probe/armoury-control-plane@${DIGEST}`,
	]);
});
