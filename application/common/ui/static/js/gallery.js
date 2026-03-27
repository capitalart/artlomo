document.addEventListener(
	'error',
	(event) => {
		const target = event.target;
		if (!(target instanceof HTMLImageElement)) return;
		if (target.getAttribute('data-thumb-fallback') !== 'true') return;

		target.classList.add('thumb-image-hidden');
		const placeholder = target.nextElementSibling;
		if (placeholder instanceof HTMLElement && placeholder.classList.contains('thumb-placeholder')) {
			placeholder.classList.remove('thumb-placeholder-hidden');
			placeholder.classList.add('thumb-placeholder-visible');
		}
	},
	true,
);
