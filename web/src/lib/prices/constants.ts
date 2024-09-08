import type { Chain } from './types';

export const CHAINS: Chain[] = [
	{ name: 'TivTaam', chainId: '7290873255550', serverType: 'cerberus', password: '' },
	{ name: 'HaziHinam', chainId: '7290700100008', serverType: 'cerberus', password: '' },
	{ name: 'yohananof', chainId: '7290100700006', serverType: 'cerberus', password: '' },
	{ name: 'osherad', chainId: '7290103152017', serverType: 'cerberus', password: '' },
	{ name: 'SalachD', chainId: '7290526500006', serverType: 'cerberus', password: '12345' },
	{ name: 'Stop_Market', chainId: '7290639000004', serverType: 'cerberus', password: '' },
	{ name: 'politzer', chainId: '7291059100008', serverType: 'cerberus', password: '' },
	{ name: 'Paz_bo', chainId: '7290644700005', serverType: 'cerberus', password: 'paz468' },
	{ name: 'freshmarket', chainId: '7290876100000', serverType: 'cerberus', password: '' },
	{ name: 'Keshet', chainId: '7290785400000', serverType: 'cerberus', password: '' },
	{ name: 'RamiLevi', chainId: '7290058140886', serverType: 'cerberus', password: '' },
	{ name: 'SuperCofixApp', chainId: '7291056200008', serverType: 'cerberus', password: '' }
];

/* CERBERUS */
export const CERBERUS_URLS = {
	base: 'https://url.publishedprices.co.il',
	login: '/login',
	user: '/login/user',
	metadata: '/file/json/dir',
	downloads: '/file/d'
};
