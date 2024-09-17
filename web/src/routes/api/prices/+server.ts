import { json } from '@sveltejs/kit';
import * as cheerio from 'cheerio';

import type { RequestHandler } from './$types';
import type { Chain, CerberusAuthenticationTokens } from '$lib/prices/types';

import { CHAINS, CERBERUS_URLS } from '$lib/prices/constants';

export const GET: RequestHandler = async ({ params }) => {
	return json(await getFileList(CHAINS.find((chain) => chain.name == 'HaziHinam') as Chain, 1));
};

const getFileList = async (chain: Chain, amount: number, search: string = '') => {
	if (amount < 1) {
		throw Error('Amount must be equal or greater to 1');
	}

	let fileAuth = await login(chain);

	// console.log(`file: ${JSON.stringify(fileAuth)}`);

	const data = new URLSearchParams({
		iDisplayLength: amount.toString(), // how many we want the server to return
		mDataProp_1: 'typeLabel',
		sSearch_1: 'file', // we only want files
		sSearch: search,
		csrftoken: fileAuth.csrf ?? ''
	});

	const res = await fetch(CERBERUS_URLS.base + '/file', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: data,
		credentials: 'include'
	});

	checkResponse(res);

	// const fileMetadata = await res.json();
	// const fileList = fileMetadata.get('aaData');
	// console.log(fileList);
};

const login = async (chain: Chain) => {
	const auth = await getTokens(CERBERUS_URLS.base + CERBERUS_URLS.login);

	const data = new URLSearchParams({
		r: '',
		username: chain.name,
		password: chain.password,
		Submit: 'Sign in',
		csrftoken: auth.csrf ?? ''
	});

	const headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		Referer: CERBERUS_URLS.base + CERBERUS_URLS.login,
		'Accept-Encoding': 'gzip, deflate, br',
		Connection: 'keep-alive'
	};

	const res = await fetch(CERBERUS_URLS.base + CERBERUS_URLS.user, {
		method: 'POST',
		headers: headers,
		body: data,
		credentials: 'include',
		redirect: 'error'
	});

	checkResponse(res);

	console.log(res.url);

	return await extractTokens(res);
};

const getTokens = async (url: string) => {
	const res = await fetch(url);
	checkResponse(res);

	return await extractTokens(res);
};

const extractTokens = async (res: Response): Promise<CerberusAuthenticationTokens> => {
	const setCookieHeader = res.headers.get('set-cookie');
	const cftp = getCookieValueFromCookiesString(setCookieHeader ?? '', 'cftpSID');
	const csrf = extractCsrf(await res.text());

	return {
		cftp: cftp,
		csrf: csrf
	};
};

const extractCsrf = (text: string) => {
	const $ = cheerio.load(text);
	return $('meta[name="csrftoken"]').attr('content');
};

const getCookieValueFromCookiesString = (cookieString: string, cookieName: string) => {
	return cookieString
		.split(';')
		.map((cookie) => cookie.trimStart())
		.find((cookie) => cookie.startsWith(cookieName))
		?.slice(cookieName.length + 1); // +1 for '='
};

const checkResponse = (res: Response) => {
	if (!res.ok) {
		throw Error(`CODE ${res.status} (${res.statusText}): Request to ${res.url} failed`);
	}
};
