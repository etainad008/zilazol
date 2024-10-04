<script>
	let isVisible = $state(false);
	let inputType = $state('password');

	const handleClick = () => {
		isVisible = !isVisible;
		if (inputType === 'text') {
			inputType = 'password';
		} else {
			inputType = 'text';
		}
	};
</script>

<main class="main">
	<section class="login">
		<svg
			width="65px"
			height="65px"
			viewBox="0 0 24 24"
			fill="none"
			xmlns="http://www.w3.org/2000/svg"
		>
			<path
				d="M4 14L9 19L20 8M6 8.88889L9.07692 12L16 5"
				stroke="#000000"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
		<h1>ברוכים השבים!</h1>
		<p>אנא הכניסו את פרטיכם</p>
		<form action="">
			<div>
				<input type="" placeholder="שם משתמש" />
			</div>

			<div class="password-field">
				<input type={inputType} placeholder="סיסמא" id="password" />
				{#if isVisible}
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<!-- svelte-ignore a11y_no_static_element_interactions -->
					<svg
						class="eye-icon"
						onclick={handleClick}
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M2.99902 3L20.999 21M9.8433 9.91364C9.32066 10.4536 8.99902 11.1892 8.99902 12C8.99902 13.6569 10.3422 15 11.999 15C12.8215 15 13.5667 14.669 14.1086 14.133M6.49902 6.64715C4.59972 7.90034 3.15305 9.78394 2.45703 12C3.73128 16.0571 7.52159 19 11.9992 19C13.9881 19 15.8414 18.4194 17.3988 17.4184M10.999 5.04939C11.328 5.01673 11.6617 5 11.9992 5C16.4769 5 20.2672 7.94291 21.5414 12C21.2607 12.894 20.8577 13.7338 20.3522 14.5"
							stroke="#000000"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{:else}
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<!-- svelte-ignore a11y_no_static_element_interactions -->
					<svg
						class="eye-icon"
						onclick={handleClick}
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M15.0007 12C15.0007 13.6569 13.6576 15 12.0007 15C10.3439 15 9.00073 13.6569 9.00073 12C9.00073 10.3431 10.3439 9 12.0007 9C13.6576 9 15.0007 10.3431 15.0007 12Z"
							stroke="#000000"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M12.0012 5C7.52354 5 3.73326 7.94288 2.45898 12C3.73324 16.0571 7.52354 19 12.0012 19C16.4788 19 20.2691 16.0571 21.5434 12C20.2691 7.94291 16.4788 5 12.0012 5Z"
							stroke="#000000"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{/if}
			</div>
			<button type="submit" class="submit">התחבר</button>
		</form>

		<span class="signup">אין לך חשבון? הרשם <a href="/">כאן</a></span>
	</section>
	<section class="blobs">
		<div class="blobl">
			<div class="eye"></div>
			<div class="mouth"></div>
			<div class="tongue"></div>
		</div>
		<div class="cart-wrapper">
			<div class="baby-blob">
				<div class="eyes">
					<div></div>
					<div></div>
				</div>

				<div class="hands">
					<div class="right-hand"></div>
					<div class="left-hand"></div>
				</div>
			</div>
			<svg class="cart" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path
					d="M6.29977 5H21L19 12H7.37671M20 16H8L6 3H3M9 20C9 20.5523 8.55228 21 8 21C7.44772 21 7 20.5523 7 20C7 19.4477 7.44772 19 8 19C8.55228 19 9 19.4477 9 20ZM20 20C20 20.5523 19.5523 21 19 21C18.4477 21 18 20.5523 18 20C18 19.4477 18.4477 19 19 19C19.5523 19 20 19.4477 20 20Z"
					stroke="#000000"
					stroke-width="2"
					stroke-linejoin="round"
				/>
			</svg>
		</div>
	</section>
</main>

<style>
	main {
		display: flex;
		align-items: center;
		margin: 10rem auto 0;
		width: clamp(35rem, 80%, 65rem);
		background-color: rgb(238, 238, 238);
		border-radius: 15px;
		padding: 0.5rem;
	}

	.login {
		text-align: center;
		background-color: white;
		border-radius: 10px;
		width: 45%;
		min-width: 18rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 2rem 4rem;
	}

	h1 {
		font-size: 2em;
		font-weight: 600;
		margin: 3rem 0 1rem;
	}

	form {
		margin-top: 4rem;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	input {
		width: 32ch;
		padding: 0.75rem 0.5rem;
		border: 1px solid #ced4da;
		margin: 0.5rem 0;
		border-radius: 0.25rem;
		transition:
			border-color 0.15s ease-in-out,
			box-shadow 0.15s ease-in-out;
	}

	input:focus {
		outline: 0;
		border-color: #80bdff;
		box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
	}

	.password-field {
		position: relative;
	}

	.eye-icon {
		width: 1.25rem;
		aspect-ratio: 1;
		position: absolute;
		inset: 0;
		left: 0.5rem;
		margin-right: auto;
		margin-block: auto;
		opacity: 0.6;
	}

	.eye-icon:hover {
		cursor: pointer;
	}

	.submit {
		font-size: 1rem;
		margin-top: 1rem;
		/* width: 10rem; */
		padding: 0.5em 4.5em;
		border-radius: 100vw;
		border: none;
		background-color: #a3ea28;
		transition: 0.4s;
	}

	.submit:hover {
		/* background-color: #91d122; */
		filter: brightness(0.9);
		cursor: pointer;
	}

	.signup {
		margin-top: 8rem;
		font-size: 0.75em;
	}

	.blobs {
		flex-grow: 1;
		position: relative;
	}

	.blobl {
		width: 10rem;
		aspect-ratio: 0.5;
		background-color: #a3ea28;
		border-radius: 100vw 100vw 0 0;
		margin-right: 18rem;
		position: relative;
		animation: blob-walk infinite forwards 1.5s ease-in-out;
	}

	.eye {
		position: absolute;
		background-color: black;
		width: 10px;
		aspect-ratio: 1;
		border-radius: 50%;
		top: 3rem;
		right: 7.5rem;
	}

	.mouth {
		position: absolute;
		background-color: black;
		width: 7rem;
		aspect-ratio: 13;
		top: 5rem;
	}

	.tongue {
		position: absolute;
		background-color: rgb(231, 100, 100);
		width: 1.75rem;
		aspect-ratio: 1;
		top: 5.5rem;
		right: 4rem;
		border-radius: 0 0 100vw 100vw;
	}

	.tongue::after {
		content: '';
		position: absolute;
		background-color: black;
		width: 0.25rem;
		aspect-ratio: 0.3;
		right: 0.7rem;
	}

	.cart-wrapper {
		position: absolute;
		isolation: isolate;
		width: 35%;
		top: 8rem;
		right: 7rem;
	}

	.cart {
		z-index: -1;
	}

	.cart-wrapper::after {
		content: '';
		position: absolute;
		width: 2rem;
		aspect-ratio: 1.25;
		background-color: #a3ea28;
		top: 0.25rem;
		left: 0.25rem;
		box-shadow: 0 0 2rem #648f1a;
		border-radius: 0 100vw 100vw 0;
		z-index: 1;
	}

	.baby-blob {
		position: absolute;
		width: 3rem;
		aspect-ratio: 0.6;
		background-color: #648f1a;
		bottom: 6.8rem;
		right: 3rem;
		border-radius: 100vw 100vw 0 0;
		z-index: -1;

		& .eyes {
			display: flex;
			gap: 0.5rem;

			& * {
				position: relative;
				width: 100%;
				aspect-ratio: 1;
				background-color: white;
				border-radius: 50%;

				&::after {
					content: '';
					position: absolute;
					inset: 0.25rem;
					margin: auto;
					aspect-ratio: 1;
					background-color: black;
					border-radius: 50%;
				}
			}
		}
	}

	@keyframes blob-walk {
		50% {
			transform: translateY(-0.75rem);
		}
	}

	@keyframes baby-jump {
		50% {
			transform: translateY(-5rem);
		}
	}
</style>
