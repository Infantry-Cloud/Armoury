// Acceptance test STORY-1.1 VAL-15 (AC-14): every cluster task requires ARMOURY_KUBE_CONTEXT
// and passes it explicitly to kubectl (`--context`), helm and skaffold (`--kube-context`).
// ATDD red phase: locked at contract approval. Task T12 activates it by removing `.skip` only.
// Runs in the `test-tasks` gate step (node:test over `mise-tasks/`) and needs no cluster.
// Safety: each task runs with a closed environment (no inherited site values), in a temporary
// working directory, with KUBECONFIG pointing at a missing file. `kubectl`, `helm`, `skaffold`
// and `cargo` are shims first on PATH that record their arguments and exit 0. `mise`, `docker`
// and `buildx` are shims that record and fail, because a nested `mise` call would reload
// `mise.local.toml` and put the real tools ahead of the shims.
// Interface under test:
// - The tasks run as plain executables (no `#MISE`/`#USAGE` header is needed to run them).
// - They call kubectl, helm, skaffold and cargo directly, never mise, docker or buildx.
// - Site values come from the environment: ARMOURY_NAMESPACE, SKAFFOLD_DEFAULT_REPO,
//   ARMOURY_BUILDX_BUILDER. `ci/teardown` takes its namespace as the first argument or from
//   ARMOURY_CI_NAMESPACE (the test passes both) and never touches ARMOURY_NAMESPACE.
// One flat test, no subtests, so the JUnit testcase keeps the planned check name.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const TASKS_DIR = fileURLToPath(new URL('.', import.meta.url));
const CLUSTER_TASKS = ['check/test-db', 'dev', 'ci/deploy', 'ci/teardown'];
const CONTEXT_FLAG = { kubectl: '--context', helm: '--kube-context', skaffold: '--kube-context' };
const RECORD_AND_PASS = [...Object.keys(CONTEXT_FLAG), 'cargo'];
const RECORD_AND_FAIL = ['mise', 'docker', 'buildx'];
const PROBE_CONTEXT = 'val-15-probe-context';
const DEV_NAMESPACE = 'val-15-dev-namespace';
const CI_NAMESPACE = 'armoury-ci-val-15';

function shimBin(dir) {
	const bin = join(dir, 'bin');
	mkdirSync(bin);
	for (const tool of [...RECORD_AND_PASS, ...RECORD_AND_FAIL]) {
		const shim = join(bin, tool);
		const exit = RECORD_AND_FAIL.includes(tool) ? 127 : 0;
		writeFileSync(shim, `#!/bin/sh\nprintf '%s\\t%s\\n' "${tool}" "$*" >> "$VAL_15_CALLS"\nexit ${exit}\n`);
		chmodSync(shim, 0o755);
	}
	return bin;
}

function carriesContext(tool, args) {
	return new RegExp(`(^| )${CONTEXT_FLAG[tool]}(=| )${PROBE_CONTEXT}( |$)`).test(args);
}

// Runs one task in a closed environment and returns its outcome and recorded calls.
function runTask(dir, bin, task, context) {
	const workdir = mkdtempSync(join(dir, 'cwd-'));
	const calls = join(dir, `${task.replaceAll('/', '-')}-${context ? 'set' : 'unset'}.log`);
	const env = {
		PATH: `${bin}${delimiter}${process.env.PATH}`,
		HOME: workdir,
		TMPDIR: workdir,
		KUBECONFIG: join(dir, 'missing-kubeconfig'),
		ARMOURY_NAMESPACE: DEV_NAMESPACE,
		ARMOURY_CI_NAMESPACE: CI_NAMESPACE,
		SKAFFOLD_DEFAULT_REPO: 'registry.invalid/val-15',
		ARMOURY_BUILDX_BUILDER: 'val-15-probe-builder',
		VAL_15_CALLS: calls,
		...(context ? { ARMOURY_KUBE_CONTEXT: context } : {}),
	};
	const args = task === 'ci/teardown' ? [CI_NAMESPACE] : [];
	const result = spawnSync(join(TASKS_DIR, task), args, { cwd: workdir, encoding: 'utf8', env, timeout: 60_000 });
	const recorded = existsSync(calls) ? readFileSync(calls, 'utf8').split('\n').filter(Boolean) : [];
	const parsed = recorded.map((line) => {
		const [tool, ...rest] = line.split('\t');
		return { tool, args: rest.join('\t') };
	});
	return {
		result,
		clusterCalls: parsed.filter(({ tool }) => tool in CONTEXT_FLAG),
		escapes: parsed.filter(({ tool }) => RECORD_AND_FAIL.includes(tool)),
	};
}

test.skip('VAL-15 cluster tasks require and pass an explicit kube context', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'val-15-context-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	const bin = shimBin(dir);

	// Unset: each task exits non-zero by itself, names the variable and makes no cluster call.
	const unset = CLUSTER_TASKS.map((task) => {
		const { result, clusterCalls } = runTask(dir, bin, task, undefined);
		return {
			task,
			error: result.error?.code,
			failed: result.status !== 0,
			namesVariable: /ARMOURY_KUBE_CONTEXT/.test(`${result.stdout}${result.stderr}`),
			clusterCalls,
		};
	});
	assert.deepEqual(
		unset,
		CLUSTER_TASKS.map((task) => ({ task, error: undefined, failed: true, namesVariable: true, clusterCalls: [] })),
	);

	// Set: each task makes a cluster call, every call carries the context with that tool's flag,
	// and nothing escapes through mise, docker or buildx.
	const set = CLUSTER_TASKS.map((task) => {
		const { clusterCalls, escapes } = runTask(dir, bin, task, PROBE_CONTEXT);
		return {
			task,
			madeClusterCall: clusterCalls.length > 0,
			callsWithoutContext: clusterCalls.filter(({ tool, args }) => !carriesContext(tool, args)),
			escapes,
		};
	});
	assert.deepEqual(
		set,
		CLUSTER_TASKS.map((task) => ({ task, madeClusterCall: true, callsWithoutContext: [], escapes: [] })),
	);

	// Teardown deletes the CI namespace it was given, never the developer namespace.
	const teardown = runTask(dir, bin, 'ci/teardown', PROBE_CONTEXT).clusterCalls.map(({ args }) => args);
	assert.deepEqual(
		{
			touchesCiNamespace: teardown.some((args) => args.includes(CI_NAMESPACE)),
			touchesDevNamespace: teardown.some((args) => args.includes(DEV_NAMESPACE)),
		},
		{ touchesCiNamespace: true, touchesDevNamespace: false },
	);
});
