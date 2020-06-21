<script>
	import {onMount} from 'svelte';
	const numBooks = 9;
	let books = [];
	async function fetchJson(url) {
		let response = await fetch(url);
		return await response.json();
	}
	onMount(async () => {
		let metadata = await fetchJson("/data/meta.json");
		let totalBooks = Object.values(metadata).reduce((a, b) => a + b);
		let bookIds = new Set();
		while (bookIds.size < numBooks) {
			bookIds.add(Math.floor(Math.random() * totalBooks));
		}
		bookIds = [...bookIds].sort((a, b) => a - b);
		console.log(bookIds);
		let currentCount = 0;
		for (let category in metadata) {
			let count = metadata[category];
			if (bookIds.length == 0) {
				break;
			}
			if (currentCount + count > bookIds[0]) {
				let data = await fetchJson(`/data/${category}.json`)
				while (bookIds.length > 0 && currentCount + count > bookIds[0]) {
					books = [...books, data[bookIds[0] - currentCount]];
					bookIds = bookIds.slice(1);
				}
			}
			currentCount += count;
		}
	});
</script>

<main>
<h1>瞎读</h1>
<div class="content">
{#each books as book}
	<div class="book">
		<a href={book.bookUrl}>
			<img src={book.cover} alt={book.title}/>
			<p class="title">{book.title}</p>
		</a>
		<p class="author">作者: {book.author}</p>
	</div>
{/each}
</div>
</main>

<style>
	main {
		margin: 0 auto;
		text-align: center;
		max-width: 720px;
	}
	.content {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(240px, 1fr) );
	}
	.book {
		padding: 12px;
	}
	.title {
		margin-bottom: 0px;
	}
	.author {
		margin-top: 5px;
		font-size: 10px;
	}
</style>