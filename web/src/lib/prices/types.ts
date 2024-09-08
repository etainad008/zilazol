export type Chain = {
	name: string;
	chainId: string;
	password: string;
	serverType: 'cerberus';
};

/* CERBERUS */
export type CerberusAuthenticationTokens = {
	cftp: string | undefined;
	csrf: string | undefined;
};
