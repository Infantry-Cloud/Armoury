// Loads a real extension with a minimal fake pi and replays tool calls.
// Input (stdin JSON): { extension, cwd, steps: [{ tool, input } | { command, args }], inspect? }
// Output: results array; with inspect, { results, events, commands }.
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const spec = JSON.parse(readFileSync(0, "utf8"));
const handlers: Record<string, ((event: any, ctx: any) => any)[]> = {};
const commands: Record<string, { handler: (args: string, ctx: any) => any }> = {};
const pi = {
  cwd: spec.cwd,
  on: (name: string, fn: any) => (handlers[name] ??= []).push(fn),
  registerCommand: (name: string, def: any) => (commands[name] = def),
  exec: async (command: string, args: string[], options: any = {}) => {
    const result = spawnSync(command, args, { encoding: "utf8", cwd: options.cwd, timeout: options.timeout });
    return { stdout: result.stdout ?? "", stderr: result.stderr ?? "", code: result.status ?? 1 };
  },
};
const ctx = { cwd: spec.cwd, hasUI: false, ui: { notify: () => undefined } };

const extension = await import(pathToFileURL(spec.extension).href);
extension.default(pi);

const results: unknown[] = [];
for (const step of spec.steps) {
  if (step.command) {
    await commands[step.command].handler(step.args ?? "", ctx);
    results.push("ok");
    continue;
  }
  let outcome: any;
  for (const handler of handlers.tool_call ?? []) {
    outcome = await handler({ toolName: step.tool, input: step.input }, ctx);
    if (outcome?.block) break;
  }
  results.push({ blocked: Boolean(outcome?.block), reason: outcome?.reason ?? "" });
}
const output = spec.inspect
  ? { results, events: Object.keys(handlers), commands: Object.keys(commands) }
  : results;
process.stdout.write(JSON.stringify(output));
