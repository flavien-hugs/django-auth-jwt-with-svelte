<script lang="ts">
	import { loading } from '$lib/store/loadingStore';

	$: if ($loading.status === 'NAVIGATING') {
		setTimeout(() => {
			if ($loading.status === 'NAVIGATING') {
				$loading.status = 'LOADING';
			}
		}, 100);
	}
</script>

{#if $loading.status === 'LOADING'}
	<div class="loader-container">
		<div class="loader" />
		{#if $loading.message}
			<p>{$loading.message}</p>
		{/if}
	</div>
{/if}
