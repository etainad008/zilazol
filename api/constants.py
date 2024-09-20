from enum import Enum

CHAIN = Enum(
    "CHAIN",
    [
        "DorAlon",
        "TivTaam",
        "HaziHinam",
        "Yohananof",
        "OsherAd",
        "SalachDabach",
        "StopMarket",
        "Politzer",
        "PazBo",
        "Freshmarket",
        "Keshet",
        "RamiLevi",
        "SuperCofixApp",
        "Shufersal",
        "SuperPharm",
        "Victory",
        "HCohen",
        "MachsaneiHashook",
    ],
)
SERVER_TYPE = Enum("SERVER_TYPE", ["Cerberus", "Shufersal", "SuperPharm", "Nibit"])
FILE_CATEGORY = Enum(
    "FILE_CATEGORY", ["All", "Prices", "PricesFull", "Promos", "PromosFull", "Stores"]
)
ENTITY_TYPE = Enum("ENTITY_TYPE", ["Item", "Promo", "Store"])
FILE_CATEGORY_TO_ITEM_TYPE = {
    FILE_CATEGORY.All: None,
    FILE_CATEGORY.Prices: ENTITY_TYPE.Item,
    FILE_CATEGORY.PricesFull: ENTITY_TYPE.Item,
    FILE_CATEGORY.Promos: ENTITY_TYPE.Promo,
    FILE_CATEGORY.PromosFull: ENTITY_TYPE.Promo,
    FILE_CATEGORY.Stores: ENTITY_TYPE.Store,
}

FILE_FORMAT_SUPER_PHARM = {
    "root": "OrderXml Envelope",
    "entity_list": "Header Details",
    "item": "Line",
}

FILE_FORMAT_PRICES_DEFAULT = {
    "root": "root",
    "entity_list": "Items Item",
    "item": "Item",
}

FILE_FORMAT_PROMOS_DEFAULT = {
    "root": "root",
    "entity_list": "Promotions",
    "item": "Promotion",
}

FILE_FORMAT_STORES_DEFAULT = {
    "root": "root",
    "entity_list": "Promotions",
    "item": "Promotion",
}

SERVER_TYPE_DATA = {
    SERVER_TYPE.Cerberus: {
        "domain": "url.publishedprices.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "Price",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "PriceFull",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "Promo",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "PromoFull",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "Stores",
                "format": FILE_FORMAT_STORES_DEFAULT,
            },
        },
    },
    SERVER_TYPE.Shufersal: {
        "domain": "prices.shufersal.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "0", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "1",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "2",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "3",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "4",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "5",
                "format": FILE_FORMAT_STORES_DEFAULT,
            },
        },
    },
    SERVER_TYPE.SuperPharm: {
        "domain": "prices.super-pharm.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "Price",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "PriceFull",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "Promo",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "PromoFull",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "StoresFull",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
        },
    },
    SERVER_TYPE.Nibit: {
        "domain": "laibcatalog.co.il/",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "all", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "price",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "pricefull",
                "format": FILE_FORMAT_PRICES_DEFAULT,
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "promo",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "promofull",
                "format": FILE_FORMAT_PROMOS_DEFAULT,
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "storesfull",
                "format": FILE_FORMAT_STORES_DEFAULT,
            },
        },
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
            },
        },
    },
    CHAIN.TivTaam: {
        "id": "7290873255550",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "TivTaam",
                "password": "",
            },
        },
    },
    CHAIN.HaziHinam: {
        "id": "7290700100008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "HaziHinam",
                "password": "",
            },
        },
    },
    CHAIN.Yohananof: {
        "id": "7290100700006",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "yohananof",
                "password": "",
            },
        },
    },
    CHAIN.OsherAd: {
        "id": "7290103152017",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "osherad",
                "password": "",
            },
        },
    },
    CHAIN.SalachDabach: {
        "id": "7290526500006",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "SalachD",
                "password": "12345",
            },
        },
    },
    CHAIN.StopMarket: {
        "id": "7290639000004",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Stop_Market",
                "password": "",
            },
        },
    },
    CHAIN.Politzer: {
        "id": "7291059100008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "politzer",
                "password": "",
            },
        },
    },
    CHAIN.PazBo: {
        "id": "7290644700005",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Paz_bo",
                "password": "paz468",
            },
        },
    },
    CHAIN.Freshmarket: {
        "id": "7290876100000",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "freshmarket",
                "password": "",
            },
        },
    },
    CHAIN.Keshet: {
        "id": "7290785400000",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "Keshet",
                "password": "",
            },
        },
    },
    CHAIN.RamiLevi: {
        "id": "7290058140886",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "RamiLevi",
                "password": "",
            },
        },
    },
    CHAIN.SuperCofixApp: {
        "id": "7291056200008",
        "server": {
            "type": SERVER_TYPE.Cerberus,
            "creds": {
                "username": "SuperCofixApp",
                "password": "",
            },
        },
    },
    # SHUFERSAL
    CHAIN.Shufersal: {
        "id": "7290027600007",
        "server": {"type": SERVER_TYPE.Shufersal, "creds": None},
    },
    # SUPER PHARM
    CHAIN.SuperPharm: {
        "id": "7290172900007",
        "server": {"type": SERVER_TYPE.SuperPharm, "creds": None},
    },
    # NIBIT
    CHAIN.Victory: {
        "id": "7290696200003",
        "server": {"type": SERVER_TYPE.Nibit, "creds": None},
    },
    CHAIN.HCohen: {
        "id": "7290455000004",
        "server": {"type": SERVER_TYPE.Nibit, "creds": None},
    },
    CHAIN.MachsaneiHashook: {
        "id": "7290661400001",
        "server": {"type": SERVER_TYPE.Nibit, "creds": None},
    },
}
