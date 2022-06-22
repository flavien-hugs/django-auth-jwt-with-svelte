export { matchers } from './client-matchers.js';

export const components = [
	() => import("../../src/routes/__layout.svelte"),
	() => import("../runtime/components/error.svelte"),
	() => import("../../src/routes/accounts/login/index.svelte"),
	() => import("../../src/routes/accounts/register/index.svelte"),
	() => import("../../src/routes/accounts/user/[id].svelte"),
	() => import("../../src/routes/index.svelte")
];

export const dictionary = {
	"": [[0, 5], [1]],
	"accounts/login": [[0, 2], [1]],
	"accounts/register": [[0, 3], [1]],
	"accounts/user/[id]": [[0, 4], [1]]
};