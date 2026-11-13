// Acceptance test STORY-1.1 VAL-15 (AC-14, AC-3 Pod cleanup): every task that calls `okteto` or
// `kubectl` requires its context variables and passes them explicitly:
// `okteto --context "$ARMOURY_OKTETO_CONTEXT"` (or OKTETO_CONTEXT for an okteto command without
// that flag), `kubectl --context "$ARMOURY_KUBE_CONTEXT"`, with an explicit namespace. `helm` only
// runs local commands, and no task removes what it does not own.
// ATDD red phase: locked at contract approval. Task T12 activates it by removing `.skip` only.
// Runs in the fast-tier `test-tasks` gate step (node:test over `mise-tasks/`, except
// `*.cluster.test.mjs`) and needs no cluster, no Okteto context and no network.
// Safety: each task runs with a closed environment (no inherited site values, no GitHub values),
// in a temporary working directory, with HOME in that directory and KUBECONFIG pointing at a
// missing file. `okteto`, `kubectl`, `helm`, `cargo`, `crane`, `npm` and `npx` are shims first on
// PATH that record their arguments (and OKTETO_CONTEXT) and exit 0. The call named by
// VAL_15_FAIL (for example `cargo` or `okteto test`) exits 1; the call named by VAL_15_INTERRUPT
// sends SIGINT to its parent process (the task) and exits 130. `kubectl port-forward` prints
// `Forwarding from 127.0.0.1:5432 -> 5432` and exits. `mise`, `git`, `jj`, `docker`, `podman`,
// `buildx`, `skaffold` and `kind` are shims that record and fail: a nested `mise` call would reload
// `mise.local.toml` and put the real tools ahead of the shims; the others are forbidden or removed
// tools (Never list, D6, D8).
// Interface under test:
// - The tasks run as plain executables (no `#MISE`/`#USAGE` header is needed to run them). They
//   find the repository from their own path or MISE_PROJECT_ROOT, and call okteto, kubectl,
//   helm, cargo, crane, npm and npx directly, never mise.
// - Each task starts with one guard line per variable it needs (ARMOURY_OKTETO_CONTEXT,
//   ARMOURY_KUBE_CONTEXT, ARMOURY_NAMESPACE), before any okteto or kubectl call. A task that does
//   not need a context variable never calls that variable's tool.
// - Every `okteto` call starts with its subcommand (`okteto deploy --context …`, never
//   `okteto --context … deploy`). Commands with a `--context` flag in Okteto 3.25.0 (build, deploy,
//   destroy, down, endpoints, preview, test, up) pass it; others (namespace, context show,
//   kubeconfig, registrytoken) run with OKTETO_CONTEXT="$ARMOURY_OKTETO_CONTEXT".
// - Every `okteto` build, deploy, destroy, down, endpoints, test and up call and every `kubectl`
//   call passes `-n`/`--namespace` with a non-empty value. `okteto namespace create` passes
//   `--use=false`.
// - `gen/api` and `check/api` take ROOT as their first argument (see VAL-7).
// - CI values come from the standard GitHub Actions variables: GITHUB_EVENT_NAME, GITHUB_EVENT_PATH
//   (the event payload with the pull request number), GITHUB_REF, GITHUB_REPOSITORY and
//   GITHUB_REPOSITORY_OWNER. `ci/publish` reads the built images as `repository@sha256:digest`
//   from ARMOURY_CONTROL_PLANE_IMAGE and ARMOURY_AGENT_IMAGE, which `build.yml` passes from the
//   outputs of its `build` job, and exits non-zero before any `crane` call unless GITHUB_REF is
//   `refs/heads/main`.
// - Each task bounds its own waits: a run that takes more than 60 seconds against the shims fails.
// - Data-loss guard (AC-14): namespaces are deleted or destroyed only when they are the run's
//   `armoury-ci-*` namespace or the preview `pr-<n>`. The only delete in ARMOURY_NAMESPACE is
//   `kubectl delete pod <name>` (or `pod/<name>`) of the run-unique AGE Pod: no `--all`, label
//   selector or `-f`, no `okteto down --volumes` or `okteto destroy` there.
// - `check/test-db` names its Pod in the port-forward and the delete, treats the `Forwarding from`
//   line as ready (no TCP probe), runs `cargo`, and deletes the Pod on exit, failure and SIGINT.
//   `ci/e2e` deletes its `armoury-ci-*` namespace also when `okteto test` fails.
// One flat test, no subtests, so the JUnit testcase keeps the planned check name.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const TASKS_DIR = fileURLToPath(new URL('.', import.meta.url));
const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const DEV_NAMESPACE = 'val-15-dev-namespace';
const PR_NUMBER = 4242;
const PREVIEW = `pr-${PR_NUMBER}`;
const OWNER = 'val-15-owner';
const DIGEST = `sha256:${'c'.repeat(64)}`;

// The variables a task may need. A context variable belongs to one tool and its `--context` flag.
const OKTETO = { variable: 'ARMOURY_OKTETO_CONTEXT', tool: 'okteto', probe: 'val-15-okteto-context' };
const KUBE = { variable: 'ARMOURY_KUBE_CONTEXT', tool: 'kubectl', probe: 'val-15-kube-context' };
const NAMESPACE = { variable: 'ARMOURY_NAMESPACE', tool: null, probe: DEV_NAMESPACE };
const CONTEXTS = [OKTETO, KUBE];
const VARIABLES = [OKTETO, KUBE, NAMESPACE];
const CLUSTER_TOOLS = CONTEXTS.map(({ tool }) => tool);
const RECORD_AND_PASS = [...CLUSTER_TOOLS, 'helm', 'cargo', 'crane', 'npm', 'npx'];
const RECORD_AND_FAIL = ['mise', 'git', 'jj', 'docker', 'podman', 'buildx', 'skaffold', 'kind'];
const LOCAL_HELM_COMMANDS = ['package', 'lint', 'dependency'];
const NAMESPACED_OKTETO_COMMANDS = ['build', 'deploy', 'destroy', 'down', 'endpoints', 'test', 'up'];
const OKTETO_CONTEXT_FLAG_COMMANDS = [...NAMESPACED_OKTETO_COMMANDS, 'preview'];
const KUBECTL_VALUE_FLAGS = ['-n', '--namespace', '--context', '--grace-period', '--timeout', '-o', '--output', '--cascade', '-f', '--filename'];

const PUSH = (branch) => ({
	GITHUB_ACTIONS: 'true',
	GITHUB_EVENT_NAME: 'push',
	GITHUB_REF: `refs/heads/${branch}`,
	GITHUB_REF_NAME: branch,
	GITHUB_REPOSITORY: `${OWNER}/armoury`,
	GITHUB_REPOSITORY_OWNER: OWNER,
});
const PULL_REQUEST = (action) => ({
	GITHUB_ACTIONS: 'true',
	GITHUB_EVENT_NAME: 'pull_request',
	GITHUB_REF: `refs/pull/${PR_NUMBER}/merge`,
	GITHUB_HEAD_REF: 'val-15-branch',
	GITHUB_BASE_REF: 'main',
	GITHUB_REPOSITORY: `${OWNER}/armoury`,
	GITHUB_REPOSITORY_OWNER: OWNER,
	event: {
		action,
		number: PR_NUMBER,
		pull_request: {
			number: PR_NUMBER,
			head: { ref: 'val-15-branch', repo: { full_name: `${OWNER}/armoury` } },
			base: { ref: 'main', repo: { full_name: `${OWNER}/armoury` } },
		},
		repository: { full_name: `${OWNER}/armoury` },
	},
});
const BUILT_IMAGES = {
	ARMOURY_CONTROL_PLANE_IMAGE: `registry.invalid/val-15/armoury-control-plane@${DIGEST}`,
	ARMOURY_AGENT_IMAGE: `registry.invalid/val-15/armoury-agent@${DIGEST}`,
};

// The AC-14 tasks. `ci/e2e` runs once locally (fresh namespace) and once for a pull request
// (preview). `gen/api` and `check/api` get a temporary ROOT, so nothing is written to the repo.
const CASES = [
	{ name: 'gen:api', task: 'gen/api', root: true },
	{ name: 'api', task: 'check/api', root: true },
	{ name: 'test-db', task: 'check/test-db' },
	{ name: 'dev', task: 'dev' },
	{ name: 'ci:e2e (workstation)', task: 'ci/e2e' },
	{ name: 'ci:e2e (pull request)', task: 'ci/e2e', github: PULL_REQUEST('opened') },
	{ name: 'ci:build', task: 'ci/build' },
	{ name: 'ci:publish', task: 'ci/publish', github: PUSH('main'), env: BUILT_IMAGES },
	{ name: 'ci:preview-destroy', task: 'ci/preview-destroy', github: PULL_REQUEST('closed') },
];
const byName = (name) => CASES.find((kase) => kase.name === name);

function shimBin(dir) {
	const bin = join(dir, 'bin');
	mkdirSync(bin);
	for (const tool of [...RECORD_AND_PASS, ...RECORD_AND_FAIL]) {
		const shim = join(bin, tool);
		const exit = RECORD_AND_FAIL.includes(tool) ? 127 : 0;
		writeFileSync(
			shim,
			[
				'#!/bin/sh',
				`printf '%s\\t%s\\t%s\\n' "${tool}" "\${OKTETO_CONTEXT-}" "$*" >> "$VAL_15_CALLS"`,
				'matches() {',
				'  [ -n "$1" ] || return 1',
				'  want_tool=${1%% *}; want_word=${1#"$want_tool"}; want_word=${want_word# }; shift',
				`  [ "$want_tool" = "${tool}" ] || return 1`,
				'  [ -z "$want_word" ] && return 0',
				'  for arg in "$@"; do [ "$arg" = "$want_word" ] && return 0; done',
				'  return 1',
				'}',
				'if matches "$VAL_15_INTERRUPT" "$@"; then kill -INT "$PPID"; exit 130; fi',
				'if matches "$VAL_15_FAIL" "$@"; then exit 1; fi',
				`if [ "${tool}" = kubectl ]; then for arg in "$@"; do [ "$arg" = port-forward ] && echo 'Forwarding from 127.0.0.1:5432 -> 5432'; done; fi`,
				`exit ${exit}`,
				'',
			].join('\n'),
		);
		chmodSync(shim, 0o755);
	}
	return bin;
}

function escapeRegExp(text) {
	return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function carriesFlag(args, probe) {
	return new RegExp(`(^| )--context(=| )${escapeRegExp(probe)}( |$)`).test(args);
}

// kubectl: the `--context` flag. okteto: the flag, or OKTETO_CONTEXT for a command without it.
function carriesContext({ tool, args, words, oktetoContext }) {
	if (tool === 'kubectl') return carriesFlag(args, KUBE.probe);
	if (carriesFlag(args, OKTETO.probe)) return true;
	return !OKTETO_CONTEXT_FLAG_COMMANDS.includes(words[0]) && oktetoContext === OKTETO.probe;
}

// Positional words of a kubectl call (flags and their values removed).
function positionals(words) {
	const out = [];
	for (let index = 0; index < words.length; index += 1) {
		const word = words[index];
		if (word === '') continue;
		if (word.startsWith('-')) {
			if (!word.includes('=') && KUBECTL_VALUE_FLAGS.includes(word)) index += 1;
			continue;
		}
		out.push(word);
	}
	return out;
}

// The Pod names of `kubectl delete pod <name>…` or `delete pod/<name>…`, or null for any other
// delete (other kinds, `-f`, `--all`, a label selector).
function deletedPods(words) {
	if (words.some((word) => ['--all', '-l', '--selector', '-f', '--filename'].includes(word) || /^(-l|--selector|-f|--filename)=/.test(word))) return null;
	const rest = positionals(words).slice(positionals(words).indexOf('delete') + 1);
	if (['pod', 'pods', 'po'].includes(rest[0]) && rest.length > 1) return rest.slice(1);
	if (rest.length > 0 && rest.every((word) => /^pods?\/.+/.test(word))) return rest.map((word) => word.split('/')[1]);
	return null;
}

const hasUseFalse = (words) =>
	words.includes('--use=false') || words.some((word, index) => word === '--use' && words[index + 1] === 'false');
const hasVolumes = (words) => words.some((word) => ['-v', '--volumes', '--volumes=true'].includes(word));

// The value of `-n`/`--namespace`, '' when the flag has an empty value, undefined without the flag.
function namespaceOf(words) {
	const flag = words.findIndex((word) => word === '-n' || word === '--namespace');
	if (flag >= 0) return words[flag + 1] ?? '';
	return words.find((word) => /^(-n|--namespace)=/.test(word))?.split('=')[1];
}

function lacksNamespace({ tool, words }) {
	const namespaced = tool === 'kubectl' || NAMESPACED_OKTETO_COMMANDS.includes(words[0]);
	return namespaced && !namespaceOf(words);
}

const ownNamespace = (name) => name?.startsWith('armoury-ci-') || name === PREVIEW;
const deletesNamespace = (words) =>
	(words[0] === 'namespace' && words[1] === 'delete') ||
	(words.includes('delete') && words.some((word) => ['namespace', 'namespaces', 'ns'].includes(word)));

// True when a call removes something the task does not own (see the data-loss guard above).
// `createdPods` holds every Pod name that the same run named in a kubectl call other than delete.
function removesForeign(createdPods, { tool, words }) {
	if (tool === 'okteto' && words[0] === 'destroy') return !ownNamespace(namespaceOf(words));
	if (tool === 'okteto' && words[0] === 'down') return hasVolumes(words) && !ownNamespace(namespaceOf(words));
	if (tool === 'okteto' && words[0] === 'preview' && words[1] === 'destroy') return !words.includes(PREVIEW);
	if (deletesNamespace(words)) return words.includes(DEV_NAMESPACE) || !words.some(ownNamespace);
	if (tool === 'kubectl' && positionals(words).includes('delete')) {
		const namespace = namespaceOf(words);
		if (ownNamespace(namespace)) return false;
		const pods = deletedPods(words);
		return namespace !== DEV_NAMESPACE || pods === null || !pods.every((pod) => createdPods.has(pod));
	}
	return false;
}

// Runs one case in a closed environment with the given variables set. Returns the outcome and
// the recorded calls.
function runCase(dir, bin, kase, variables, extra = {}) {
	const workdir = mkdtempSync(join(dir, 'cwd-'));
	const calls = join(workdir, 'calls.log');
	const { event, ...github } = kase.github ?? {};
	const env = {
		PATH: `${bin}${delimiter}${process.env.PATH}`,
		HOME: workdir,
		TMPDIR: workdir,
		KUBECONFIG: join(dir, 'missing-kubeconfig'),
		MISE_PROJECT_ROOT: REPO_ROOT,
		VAL_15_CALLS: calls,
		...github,
		...kase.env,
		...Object.fromEntries(variables.map(({ variable, probe }) => [variable, probe])),
		...extra,
	};
	if (event) {
		env.GITHUB_EVENT_PATH = join(workdir, 'event.json');
		writeFileSync(env.GITHUB_EVENT_PATH, JSON.stringify(event));
	}
	const args = [];
	if (kase.root) {
		const root = join(workdir, 'root');
		mkdirSync(join(root, 'api'), { recursive: true });
		copyFileSync(join(REPO_ROOT, 'api', 'openapi.yaml'), join(root, 'api', 'openapi.yaml'));
		args.push(root);
	}
	const result = spawnSync(join(TASKS_DIR, kase.task), args, { cwd: workdir, encoding: 'utf8', env, timeout: 60_000 });
	const recorded = existsSync(calls) ? readFileSync(calls, 'utf8').split('\n').filter(Boolean) : [];
	const parsed = recorded.map((line) => {
		const [tool, oktetoContext, ...rest] = line.split('\t');
		const args = rest.join('\t');
		return { tool, oktetoContext, args, words: args.split(' ') };
	});
	const clusterCalls = parsed.filter(({ tool }) => CLUSTER_TOOLS.includes(tool));
	const kubectlCalls = clusterCalls.filter(({ tool }) => tool === 'kubectl');
	const createdPods = new Set(
		kubectlCalls
			.filter(({ words }) => !positionals(words).includes('delete'))
			.flatMap(({ words }) => positionals(words).map((word) => word.replace(/^pods?\//, ''))),
	);
	const podDeletes = kubectlCalls.filter(({ words }) => positionals(words).includes('delete')).map(({ words }) => deletedPods(words));
	return {
		error: result.error?.code,
		failed: result.status !== 0,
		output: `${result.stdout}${result.stderr}`,
		clusterCalls,
		clusterArgs: clusterCalls.map(({ tool, args }) => `${tool} ${args}`),
		namespaceGaps: clusterCalls.filter(lacksNamespace).map(({ tool, args }) => `${tool} ${args}`),
		foreignRemovals: clusterCalls.filter((call) => removesForeign(createdPods, call)).map(({ tool, args }) => `${tool} ${args}`),
		deletedPods: podDeletes.flatMap((pods) => pods ?? []),
		subcommandAfterFlag: clusterCalls.filter(({ tool, words }) => tool === 'okteto' && words[0].startsWith('-')).map(({ args }) => `okteto ${args}`),
		namespaceCreateWithoutUseFalse: clusterCalls
			.filter(({ tool, words }) => tool === 'okteto' && words[0] === 'namespace' && words[1] === 'create' && !hasUseFalse(words))
			.map(({ args }) => `okteto ${args}`),
		called: (tool, word) => parsed.some((call) => call.tool === tool && (word === undefined || call.words.includes(word))),
		helmCalls: parsed.filter(({ tool }) => tool === 'helm'),
		craneCalls: parsed.filter(({ tool }) => tool === 'crane'),
		escapes: parsed.filter(({ tool }) => RECORD_AND_FAIL.includes(tool)).map(({ tool, args }) => `${tool} ${args}`),
	};
}

test.skip('VAL-15 cluster tasks require and pass an explicit Okteto and kube context', (t) => {
	const dir = mkdtempSync(join(tmpdir(), 'val-15-context-'));
	t.after(() => rmSync(dir, { recursive: true, force: true }));
	const bin = shimBin(dir);
	const foreignRemovals = [];

	// Both contexts unset: each task exits non-zero by itself, names a context variable and makes
	// no okteto or kubectl call.
	const bothUnset = CASES.map((kase) => {
		const run = runCase(dir, bin, kase, [NAMESPACE]);
		foreignRemovals.push(...run.foreignRemovals);
		return {
			task: kase.name,
			error: run.error,
			failed: run.failed,
			namesVariable: CONTEXTS.some(({ variable }) => run.output.includes(variable)),
			clusterCalls: run.clusterArgs,
		};
	});
	assert.deepEqual(
		bothUnset,
		CASES.map((kase) => ({ task: kase.name, error: undefined, failed: true, namesVariable: true, clusterCalls: [] })),
	);

	// One variable unset: a task that needs it stops before any okteto or kubectl call and names
	// it; a task that does not need it never names it, never calls its tool and still passes an
	// explicit namespace.
	for (const missing of VARIABLES) {
		const oneUnset = CASES.map((kase) => {
			const run = runCase(dir, bin, kase, VARIABLES.filter((variable) => variable !== missing));
			foreignRemovals.push(...run.foreignRemovals);
			const namesMissing = run.output.includes(missing.variable);
			const guarded = run.failed && namesMissing && run.clusterCalls.length === 0;
			const independent =
				!namesMissing && !run.clusterCalls.some(({ tool }) => tool === missing.tool) && run.namespaceGaps.length === 0;
			return { task: kase.name, unset: missing.variable, error: run.error, guardedOrIndependent: guarded || independent };
		});
		assert.deepEqual(
			oneUnset,
			CASES.map((kase) => ({ task: kase.name, unset: missing.variable, error: undefined, guardedOrIndependent: true })),
		);
	}

	// All set: each task makes an okteto or kubectl call, every call carries its own tool's
	// context and a namespace, helm only runs local commands, and nothing escapes through a
	// forbidden tool.
	const allSet = CASES.map((kase) => {
		const run = runCase(dir, bin, kase, VARIABLES);
		foreignRemovals.push(...run.foreignRemovals);
		return {
			task: kase.name,
			error: run.error,
			madeClusterCall: run.clusterCalls.length > 0,
			callsWithoutContext: run.clusterCalls.filter((call) => !carriesContext(call)).map(({ tool, args }) => `${tool} ${args}`),
			oktetoFlagsBeforeSubcommand: run.subcommandAfterFlag,
			callsWithoutNamespace: run.namespaceGaps,
			namespaceCreateWithoutUseFalse: run.namespaceCreateWithoutUseFalse,
			clusterHelmCalls: run.helmCalls.filter(({ words }) => !LOCAL_HELM_COMMANDS.includes(words[0])).map(({ args }) => args),
			escapes: run.escapes,
		};
	});
	assert.deepEqual(
		allSet,
		CASES.map((kase) => ({
			task: kase.name,
			error: undefined,
			madeClusterCall: true,
			callsWithoutContext: [],
			oktetoFlagsBeforeSubcommand: [],
			callsWithoutNamespace: [],
			namespaceCreateWithoutUseFalse: [],
			clusterHelmCalls: [],
			escapes: [],
		})),
	);

	// Cleanup on failure and interrupt, run-unique Pods and the main-only publish guard.
	const testDbPass = runCase(dir, bin, byName('test-db'), VARIABLES);
	const testDbFail = runCase(dir, bin, byName('test-db'), VARIABLES, { VAL_15_FAIL: 'cargo' });
	const testDbInterrupt = runCase(dir, bin, byName('test-db'), VARIABLES, { VAL_15_INTERRUPT: 'cargo' });
	const e2eFail = runCase(dir, bin, byName('ci:e2e (workstation)'), VARIABLES, { VAL_15_FAIL: 'okteto test' });
	const publishBranch = runCase(dir, bin, { ...byName('ci:publish'), github: PUSH('val-15-branch') }, VARIABLES);
	for (const run of [testDbPass, testDbFail, testDbInterrupt, e2eFail, publishBranch]) foreignRemovals.push(...run.foreignRemovals);
	assert.deepEqual(
		{
			testDbDeletesItsPod: testDbPass.deletedPods.length > 0,
			testDbFailRanCargo: testDbFail.called('cargo'),
			testDbFailExitsNonZero: testDbFail.failed,
			testDbDeletesOnFailure: testDbFail.deletedPods.length > 0,
			testDbInterruptRanCargo: testDbInterrupt.called('cargo'),
			testDbInterruptExitsNonZero: testDbInterrupt.failed,
			testDbDeletesOnInterrupt: testDbInterrupt.deletedPods.length > 0,
			testDbRunsUseDifferentPods: !testDbPass.deletedPods.some((pod) => testDbFail.deletedPods.includes(pod)),
			e2eFailRanOktetoTest: e2eFail.called('okteto', 'test'),
			e2eFailExitsNonZero: e2eFail.failed,
			e2eDeletesItsNamespaceOnFailure: e2eFail.clusterCalls.some(
				({ words }) => deletesNamespace(words) && words.some((word) => word.startsWith('armoury-ci-')),
			),
			publishOffMainExitsNonZero: publishBranch.failed,
			publishOffMainCraneCalls: publishBranch.craneCalls.length,
		},
		{
			testDbDeletesItsPod: true,
			testDbFailRanCargo: true,
			testDbFailExitsNonZero: true,
			testDbDeletesOnFailure: true,
			testDbInterruptRanCargo: true,
			testDbInterruptExitsNonZero: true,
			testDbDeletesOnInterrupt: true,
			testDbRunsUseDifferentPods: true,
			e2eFailRanOktetoTest: true,
			e2eFailExitsNonZero: true,
			e2eDeletesItsNamespaceOnFailure: true,
			publishOffMainExitsNonZero: true,
			publishOffMainCraneCalls: 0,
		},
	);

	// Data-loss guard over every run above.
	assert.deepEqual(foreignRemovals, [], 'no call removes a namespace or resource the task does not own');
});
