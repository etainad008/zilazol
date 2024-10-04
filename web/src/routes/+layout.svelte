<script>
	let buttonIsClicked = $state(false);

	const handleClick = () => {
		buttonIsClicked = !buttonIsClicked;
	};
</script>

<div dir="rtl">
	<section>
		<nav class="nav">
			<p>שם ולוגו</p>
			<section class="links">
				<a href="/" class="link">בית</a>
				<a href="/" class="link">לתחילת קנייה</a>
				<a href="/" class="link">צרו קשר</a>
			</section>
			<div class="side-nav">
				<img class="icon" src="/cart-icon.svg" alt="" />
				<a href="/login" class="signup link">הרשמו</a>
			</div>
		</nav>
		<hr class="hr" />
	</section>
	<slot />
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');

	:global(*) {
		padding: 0;
		margin: 0;
		box-sizing: border-box;
	}

	:global(img) {
		max-width: 100%;
	}

	:root {
		--accent: #a3ea28;
		font-family: 'Fredoka', sans-serif;
	}

	.nav {
		display: flex;
		justify-content: space-between;
		padding: 0.5rem 1rem;
		align-items: center;
	}

	.links {
		display: flex;
		gap: 2.5rem;
		align-items: center;
	}

	.side-nav {
		display: flex;
		gap: 1rem;
		align-items: center;
	}

	.link {
		text-decoration: none;
		color: black;
	}

	.icon {
		width: 32px;
		aspect-ratio: 1;
	}

	.signup {
		padding: 0.5em 1em;
		background-color: var(--accent);
		border-style: none;
		border-radius: 5px;
	}

	.signup:hover {
		background-color: #91d122;
		transition: 0.4s;
		cursor: pointer;
	}

	.hr {
		margin-inline: 1rem;
		border: none;
		border-bottom: 1px solid rgba(0, 0, 0, 0.3);
	}
</style>
