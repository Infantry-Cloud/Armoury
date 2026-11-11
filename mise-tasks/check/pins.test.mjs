// Acceptance test STORY-1.1 VAL-5 (AC-2): the pin checker rejects every floating reference.
// ATDD red phase: locked at contract approval. Task T7 activates it by removing `.skip` only.
// Runs in the `test-tasks` gate step (node:test over `mise-tasks/`). The file is not
// executable, so mise does not treat it as a task.
// Interface under test: `mise-tasks/check/pins <root>` exits 0 when every reference under
// <root> is pinned, and exits 1 with the offending file path in stdout or stderr otherwise.
// The checker finds files by kind, not by fixed path: `Dockerfile` and `*.Dockerfile`, every
// `Cargo.toml`, Kubernetes manifests and workflows. On this repository it must skip `_bmad/`,
// `.agents/`, `node_modules/`, `target/`, `.jj/` and `.git/`, accept mise inline-table pins and
// Helm-templated `image:` lines.
// One flat test, no subtests: node's JUnit reporter turns a test with subtests into a
// <testsuite>, and then CI results cannot match the planned check name.
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
	'.gitignore': 'mise.local.toml\ntarget/\n',
	'mise.toml': '[tools]\nnode = "24.11.1"\nrust = "1.91.1"\n',
	'mise.lock': '# lock\n',
	'mise.local.toml.example': '[env]\nARMOURY_KUBE_CONTEXT = "your-dev-context"\n',
	'Cargo.toml':
		'[workspace]\nresolver = "3"\nmembers = ["agent"]\n\n[workspace.dependencies]\nprost = "=0.14.1"\ntokio = { version = "=1.48.0", features = ["full"] }\nk8s-openapi = { version = "=0.26.0", features = ["v1_33"] }\n',
	'agent/Cargo.toml': '[package]\nname = "agent"\nedition = "2024"\n\n[dependencies]\ntokio = { workspace = true }\nkube = { version = "=2.0.1", features = ["runtime"] }\n',
	'Cargo.lock': '# lock\n',
	'web/package.json': '{\n  "devDependencies": { "vite": "7.2.2", "vitest": "4.0.8" }\n}\n',
	'web/package-lock.json': '{}\n',
	'control-plane/Dockerfile': `FROM docker.io/library/rust:1.91.1-bookworm@${DIGEST} AS build\n`,
	'agent/Dockerfile': `FROM gcr.io/distroless/cc-debian12:nonroot@${DIGEST}\n`,
	'mise-tasks/gen/openapi.Dockerfile': `FROM docker.io/openapitools/openapi-generator-cli:v7.17.0@${DIGEST} AS generate\n`,
	'mise-tasks/check/test-db.yaml': `apiVersion: v1\nkind: Pod\nmetadata:\n  name: age\nspec:\n  containers:\n    - name: age\n      image: docker.io/apache/age:release_PG18_1.8.0@${DIGEST}\n`,
	'.github/workflows/ci.yml': `jobs:\n  check:\n    services:\n      db:\n        image: docker.io/library/postgres:18.1@${DIGEST}\n    steps:\n      - uses: actions/checkout@${SHA} # v5\n`,
	'.github/workflows/build.yml': `jobs:\n  images:\n    steps:\n      - uses: docker/setup-buildx-action@${SHA} # v3\n`,
};

// One defect per case: the file it touches, its new content (null deletes it), and the file
// the checker must name.
const DEFECTS = [
	['a latest tool', 'mise.toml', '[tools]\nnode = "latest"\n', 'mise.toml'],
	['a non-exact mise tool version', 'mise.toml', '[tools]\nnode = "24"\n', 'mise.toml'],
	['a FROM without a digest', 'agent/Dockerfile', 'FROM gcr.io/distroless/cc-debian12:nonroot\n', 'agent/Dockerfile'],
	['a generator stage FROM without a digest', 'mise-tasks/gen/openapi.Dockerfile', 'FROM docker.io/openapitools/openapi-generator-cli:v7.17.0 AS generate\n', 'mise-tasks/gen/openapi.Dockerfile'],
	['a Kubernetes manifest image without a digest', 'mise-tasks/check/test-db.yaml', 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: age\nspec:\n  containers:\n    - name: age\n      image: docker.io/apache/age:release_PG18_1.8.0\n', 'mise-tasks/check/test-db.yaml'],
	['a workflow services image without a digest', '.github/workflows/ci.yml', 'jobs:\n  check:\n    services:\n      db:\n        image: docker.io/library/postgres:18.1\n', '.github/workflows/ci.yml'],
	['a workflow container image without a digest', '.github/workflows/ci.yml', 'jobs:\n  check:\n    container:\n      image: docker.io/library/rust:1.91.1-bookworm\n', '.github/workflows/ci.yml'],
	['an action ref that is not a SHA', '.github/workflows/build.yml', 'jobs:\n  images:\n    steps:\n      - uses: docker/setup-buildx-action@v3\n', '.github/workflows/build.yml'],
	['a Cargo requirement without =', 'agent/Cargo.toml', '[package]\nname = "agent"\nedition = "2024"\n\n[dependencies]\nkube = "2.0.1"\n', 'agent/Cargo.toml'],
	['a latest crate feature', 'Cargo.toml', '[workspace]\nresolver = "3"\n\n[workspace.dependencies]\nk8s-openapi = { version = "=0.26.0", features = ["latest"] }\n', 'Cargo.toml'],
	['a ^ npm range', 'web/package.json', '{ "devDependencies": { "vite": "^7.2.2" } }\n', 'web/package.json'],
	['a ~ npm range', 'web/package.json', '{ "devDependencies": { "vite": "~7.2.2" } }\n', 'web/package.json'],
	['a missing Cargo.lock', 'Cargo.lock', null, 'Cargo.lock'],
	['a missing web/package-lock.json', 'web/package-lock.json', null, 'web/package-lock.json'],
	['a missing mise.lock', 'mise.lock', null, 'mise.lock'],
	['a missing mise.local.toml.example', 'mise.local.toml.example', null, 'mise.local.toml.example'],
	['a mise.local.toml that is not ignored', '.gitignore', 'target/\n', '.gitignore'],
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

function escapeRegExp(text) {
	return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test.skip('VAL-5 pins check rejects floating references', (t) => {
	const roots = [];
	t.after(() => roots.forEach((root) => rmSync(root, { recursive: true, force: true })));

	// Every defect is checked, then compared in one assertion, so a failure lists all cases.
	const observed = DEFECTS.map(([name, path, content, named]) => {
		const root = fixture({ [path]: content });
		roots.push(root);
		const result = runPins(root);
		return {
			defect: name,
			status: result.status,
			namesFile: new RegExp(escapeRegExp(named)).test(`${result.stdout}${result.stderr}`),
		};
	});
	assert.deepEqual(
		observed,
		DEFECTS.map(([name]) => ({ defect: name, status: 1, namesFile: true })),
	);

	const clean = fixture();
	roots.push(clean);
	assert.equal(runPins(clean).status, 0, 'a fully pinned tree is accepted');
	assert.equal(runPins(REPO_ROOT).status, 0, 'this repository is accepted');
});
