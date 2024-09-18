from enum import Enum

CHAIN = Enum("CHAIN", ["DorAlon", "TivTaam", "HaziHinam", "Yohananof", "OsherAd", "SalachDabach", "StopMarket", "Politzer", "PazBo", "Freshmarket", "Keshet", "RamiLevi", "SuperCofixApp", "Shufersal", "SuperPharm"])
SERVER_TYPE = Enum("SERVER_TYPE", ["Cerberus", "Shufersal", "SuperPharm"])
FILE_CATEGORY = Enum("FILE_CATEGORIE", ["All", "Prices", "PricesFull", "Promos", "PromosFull", "Stores"])


SERVER_TYPE_DATA = {
    SERVER_TYPE.Cerberus: {
        "domain": "url.publishedprices.co.il",
        "categories": {
            FILE_CATEGORY.All: "",
            FILE_CATEGORY.Prices: "Price",
            FILE_CATEGORY.PricesFull: "PriceFull",
            FILE_CATEGORY.Promos: "Promo",
            FILE_CATEGORY.PromosFull: "PromoFull",
            FILE_CATEGORY.Stores: "Stores",
        }
    },
    SERVER_TYPE.Shufersal: {
        "domain": "prices.shufersal.co.il",
        "categories": {
            FILE_CATEGORY.All: "0",
            FILE_CATEGORY.Prices: "1",
            FILE_CATEGORY.PricesFull: "2",
            FILE_CATEGORY.Promos: "3",
            FILE_CATEGORY.PromosFull: "4",
            FILE_CATEGORY.Stores: "5",
        }
    },
    SERVER_TYPE.SuperPharm: {
        "domain": "prices.super-pharm.co.il",
        "categories": {
            FILE_CATEGORY.All: "",
            FILE_CATEGORY.Prices: "Price",
            FILE_CATEGORY.PricesFull: "PriceFull",
            FILE_CATEGORY.Promos: "Promo",
            FILE_CATEGORY.PromosFull: "PromoFull",
            FILE_CATEGORY.Stores: "StoresFull",
        }
    },
}


CHAINS_DATA = {
    # CERBERUS
    CHAIN.DorAlon: {
        "id": "7290492000005",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "doralon",
                "password": "",
            }
        }
    },
    CHAIN.TivTaam: {
        "id": "7290873255550",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "TivTaam",
                "password": "",
            }
        }
    },
    CHAIN.HaziHinam: {
        "id": "7290700100008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "HaziHinam",
                "password": "",
            }
        }
    },
    CHAIN.Yohananof: {
        "id": "7290100700006",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "yohananof",
                "password": "",
            }
        }
    },
    CHAIN.OsherAd: {
        "id": "7290103152017",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "osherad",
                "password": "",
            }
        }
    },
    CHAIN.SalachDabach: {
        "id": "7290526500006",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "SalachD",
                "password": "12345",
            }
        }
    },
    CHAIN.StopMarket: {
        "id": "7290639000004",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Stop_Market",
                "password": "",
            }
        }
    },
    CHAIN.Politzer: {
        "id": "7291059100008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "politzer",
                "password": "",
            }
        }
    },
    CHAIN.PazBo: {
        "id": "7290644700005",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Paz_bo",
                "password": "paz468",
            }
        }
    },
    CHAIN.Freshmarket: {
        "id": "7290876100000",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "freshmarket",
                "password": "",
            }
        }
    },
    CHAIN.Keshet: {
        "id": "7290785400000",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Keshet",
                "password": "",
            }
        }
    },
    CHAIN.RamiLevi: {
        "id": "7290058140886",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "RamiLevi",
                "password": "",
            }
        }
    },
    CHAIN.SuperCofixApp: {
        "id": "7291056200008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "SuperCofixApp",
                "password": "",
            }
        }
    },

    # SHUFERSAL
    CHAIN.Shufersal: {
        "id": "7290027600007",
        "server": {
            "type": SERVER_TYPE.Shufersal,
            "creds": None
        }
    },

    # SUPER PHARM
    CHAIN.SuperPharm: {
        "id": "7290172900007",
        "server": {
            "type": SERVER_TYPE.SuperPharm,
            "creds": None
        }
    }
}
