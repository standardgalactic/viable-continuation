// Usage: node simulator/test_simulator.js
// 1. Extracts the core and the embedded spec from the built HTML and checks the spec equals spec/housing_v2.json.
// 2. Runs the companion checks reproduced in the page.
// 3. Replays traces produced by the Python companion (simulator/trace_fixture.json) and compares them exactly.
const fs = require("fs"), path = require("path"), vm = require("vm");
const here = __dirname;
const html = fs.readFileSync(path.join(here, "housing_v2_simulator.html"), "utf8");
const embedded = JSON.parse(html.match(/<script id="spec" type="application\/json">([\s\S]*?)<\/script>/)[1].replace(/<\\\//g, "</"));
const file = JSON.parse(fs.readFileSync(path.join(here, "..", "spec", "housing_v2.json"), "utf8"));
let bad = 0;
function ok(c, msg) { console.log((c ? "PASS  " : "FAIL  ") + msg); if (!c) bad++; }
ok(JSON.stringify(embedded) === JSON.stringify(file), "embedded specification equals spec/housing_v2.json");
const core = html.match(/\/\*CORE_START\*\/([\s\S]*?)\/\*CORE_END\*\//)[1];
const ctx = { module: { exports: {} } }; vm.createContext(ctx); vm.runInContext(core, ctx);
const HV2 = ctx.module.exports; const m = HV2.makeModel(embedded);
HV2.companionChecks(m).forEach(r => ok(r.ok, r.name + (r.detail ? " [" + r.detail + "]" : "")));
const fx = JSON.parse(fs.readFileSync(path.join(here, "trace_fixture.json"), "utf8"));
let n = 0, diff = 0;
for (const c of fx.cases) {
  const r = m.simulate(c.init, c.spends.length, (ks, t) => c.spends[t], 1e9, null);
  n++;
  if (JSON.stringify(r.final) !== JSON.stringify(c.final) || r.total !== c.total) diff++;
}
ok(diff === 0, "replayed " + n + " Python traces: final conditions and surplus identical");
const k1 = fx.kernel1;
let kd = 0;
for (const key of Object.keys(k1)) {
  const [cap, shock] = key.split(",").map(Number);
  if (JSON.stringify(Array.from(m.kernel1(cap, shock)).sort((a, b) => a - b)) !== JSON.stringify(k1[key])) kd++;
}
ok(kd === 0, "one-unit kernels agree with Python for " + Object.keys(k1).length + " (ceiling, shock) pairs");
process.exit(bad ? 1 : 0);
