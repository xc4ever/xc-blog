import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import vm from "node:vm";
import { test } from "node:test";
import ts from "typescript";

const source = await readFile(new URL("../src/utils/sakura-manager.ts", import.meta.url), "utf8");
const compiled = ts.transpileModule(source, {
	compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 },
}).outputText;

test("sakura limits redraws on fast displays and releases animation on hide/stop", () => {
	const frames = new Map();
	const listeners = new Map();
	let id = 0;
	let draws = 0;
	const canvas = {
		setAttribute() {},
		getContext: () => ({ clearRect() { draws++; } }),
	};
	const document = {
		hidden: false,
		createElement: () => canvas,
		body: { appendChild() {}, removeChild() {} },
		addEventListener: (type, handler) => listeners.set(type, handler),
		removeEventListener: (type) => listeners.delete(type),
	};
	const exports = {};
	vm.runInNewContext(compiled, {
		exports, document,
		window: { innerWidth: 1000, innerHeight: 800, addEventListener() {}, removeEventListener() {} },
		requestAnimationFrame: (fn) => { frames.set(++id, fn); return id; },
		cancelAnimationFrame: (key) => frames.delete(key),
	});
	const manager = new exports.SakuraManager({});
	// Supply an already-loaded scene to exercise animation lifecycle directly.
	manager.createCanvas();
	const scales = [];
	manager.sakuraList = { update: (scale) => scales.push(scale), draw() {} };
	manager.isRunning = true;
	manager.startAnimation();
	function tick(timestamp) {
		const pending = [...frames.values()];
		frames.clear();
		pending.forEach((fn) => fn(timestamp));
	}
	for (let n = 0; n <= 144; n++) tick(n * 1000 / 144);
	assert.ok(draws >= 29 && draws <= 31, `redraws: ${draws}`);
	// The final partial drawing interval may still be pending at one second.
	assert.ok(Math.abs(scales.reduce((a, b) => a + b, 0) - 60) < 3);
	document.hidden = true;
	listeners.get("visibilitychange")();
	assert.equal(frames.size, 0);
	document.hidden = false;
	listeners.get("visibilitychange")();
	assert.equal(frames.size, 1);
	tick(10_000);
	tick(10_034);
	assert.ok(scales.at(-1) < 3, "resume must not include hidden-tab elapsed time");
	manager.stop();
	assert.equal(frames.size, 0);
	assert.equal(listeners.has("visibilitychange"), false);
});
