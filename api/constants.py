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
FILE_CATEGORY_TO_ENTITY_TYPE = {
    FILE_CATEGORY.All: None,
    FILE_CATEGORY.Prices: ENTITY_TYPE.Item,
    FILE_CATEGORY.PricesFull: ENTITY_TYPE.Item,
    FILE_CATEGORY.Promos: ENTITY_TYPE.Promo,
    FILE_CATEGORY.PromosFull: ENTITY_TYPE.Promo,
    FILE_CATEGORY.Stores: ENTITY_TYPE.Store,
}

ENTITY_TYPE_TO_FILE_CATEGORY = {
    ENTITY_TYPE.Item: FILE_CATEGORY.Prices,
    ENTITY_TYPE.Promo: FILE_CATEGORY.Promos,
    ENTITY_TYPE.Store: FILE_CATEGORY.Stores,
}

FILE_FORMAT_SUPER_PHARM = {
    "root": "OrderXml Envelope",
    "entity_list": "Header Details",
}

FILE_FORMAT_PRICES_CERBERUS = {
    "root": "root",
    "entity_list": "Items Item",
}

FILE_FORMAT_PROMOS_CERBERUS = {
    "root": "root",
    "entity_list": "Promotions Promotion",
}

FILE_FORMAT_PRICES_SHUFERSAL = {"root": "root", "entity_list": "Items Item"}

FILE_FORMAT_PRICES_NIBIT = {
    "root": "Prices",
    "entity_list": "Products Product",
}

ENTITY_FORMAT_ITEM_CERBERUS = {
    "update_date": "PriceUpdateDate",
    "item_code": "ItemCode",
    "item_type": "ItemType",
    "item_name": "ItemName",
    "manufacturer_name": "ManufacturerName",
    "manufacture_country": "ManufactureCountry",
    "manufacturer_item_description": "ManufacturerItemDescription",
    "unit_quantity": "UnitQty",
    "quantity": "Quantity",
    "b_is_weighted": "bIsWeighted",
    "unit_of_measurement": "UnitOfMeasure",
    "quantity_in_package": "QtyInPackage",
    "item_price": "ItemPrice",
    "unit_of_measurement_price": "UnitOfMeasurePrice",
    "allow_discount": "AllowDiscount",
    "item_status": "ItemStatus",
}

ENTITY_FORMAT_ITEM_NIBIT = {
    "update_date": "PriceUpdateDate",
    "item_code": "ItemCode",
    "item_type": "ItemType",
    "item_name": "ItemName",
    "manufacturer_name": "ManufactureName",
    "manufacture_country": "ManufactureCountry",
    "manufacturer_item_description": "ManufactureItemDescription",
    "unit_quantity": "UnitQty",
    "quantity": "Quantity",
    "b_is_weighted": "BisWeighted",
    "unit_of_measurement": "UnitMeasure",
    "quantity_in_package": "QtyInPackage",
    "item_price": "ItemPrice",
    "unit_of_measurement_price": "UnitOfMeasurePrice",
    "allow_discount": "AllowDiscount",
    "item_status": "itemStatus",
}

ENTITY_FORMAT_ITEM_SUPER_PHARM = {
    "update_date": "PriceUpdateDate",
    "item_code": "ItemCode",
    "item_type": None,
    "item_name": "ItemName",
    "manufacturer_name": "ManufacturerName",
    "manufacture_country": "ManufactureCountry",
    "manufacturer_item_description": "ManufacturerItemDescription",
    "unit_quantity": "UnitQty",
    "quantity": "Quantity",
    "b_is_weighted": "blsWeighted",
    "unit_of_measurement": "UnitOfMeasure",
    "quantity_in_package": "QtyInPackage",
    "item_price": "ItemPrice",
    "unit_of_measurement_price": "UnitOfMeasurePrice",
    "allow_discount": "AllowDiscount",
    "item_status": "ItemStatus",
}

ENTITY_FORMAT_ITEM_SHUFERSAL = {
    "update_date": "PriceUpdateDate",
    "item_code": "ItemCode",
    "item_type": "ItemType",
    "item_name": "ItemName",
    "manufacturer_name": "ManufacturerName",
    "manufacture_country": "ManufactureCountry",
    "manufacturer_item_description": "ManufacturerItemDescription",
    "unit_quantity": "UnitQty",
    "quantity": "Quantity",
    "b_is_weighted": "bIsWeighted",
    "unit_of_measurement": "UnitOfMeasure",
    "quantity_in_package": "QtyInPackage",
    "item_price": "ItemPrice",
    "unit_of_measurement_price": "UnitOfMeasurePrice",
    "allow_discount": "AllowDiscount",
    "item_status": "ItemStatus",
}

SERVER_TYPE_DATA = {
    SERVER_TYPE.Cerberus: {
        "domain": "https://url.publishedprices.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "Price",
                "format": {
                    "file": FILE_FORMAT_PRICES_CERBERUS,
                    "entity": ENTITY_FORMAT_ITEM_CERBERUS,
                },
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "PriceFull",
                "format": {
                    "file": FILE_FORMAT_PRICES_CERBERUS,
                    "entity": ENTITY_FORMAT_ITEM_CERBERUS,
                },
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "Promo",
                "format": {
                    "file": FILE_FORMAT_PROMOS_CERBERUS,
                    "entity": ENTITY_FORMAT_ITEM_SHUFERSAL,
                },
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "PromoFull",
                "format": {
                    "file": FILE_FORMAT_PROMOS_CERBERUS,
                    "entity": ENTITY_FORMAT_ITEM_SHUFERSAL,
                },
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "Stores",
                "format": {
                    "file": {
                        "root": "Root",
                        "entity_list": "SubChains SubChain Stores Store",
                    },
                    "entity": {
                        "chain_id": None,
                        "store_id": "StoreId",
                        "store_name": "StoreName",
                        "store_type": "StoreType",
                        "chain": None,
                        "bikoret_number": "BikoretNo",
                        "subchain_id": None,
                        "subchain_name": None,
                        "city": "City",
                        "address": "Address",
                        "zipcode": "ZipCode",
                    },
                },
            },
        },
    },
    SERVER_TYPE.Shufersal: {
        "domain": "https://prices.shufersal.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "0", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "1",
                "format": {
                    "file": FILE_FORMAT_PRICES_SHUFERSAL,
                    "entity": ENTITY_FORMAT_ITEM_SHUFERSAL,
                },
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "2",
                "format": {
                    "file": FILE_FORMAT_PRICES_SHUFERSAL,
                    "entity": ENTITY_FORMAT_ITEM_SHUFERSAL,
                },
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "3",
                "format": {
                    "file": {
                        "root": "root",
                        "entity_list": "Promotions Promotion",
                    },
                    "entity": {
                        "promotion_id": "PromotionId",
                        "promotion_description": "PromotionDescription",
                        "promotion_update_date": "PromotionUpdateDate",
                        "allow_multiple_discounts": "AllowMultipleDiscounts",
                        "promotion_start_date": "PromotionStartDate",
                        "promotion_start_hour": "PromotionStartHour",
                        "promotion_end_date": "PromotionEndDate",
                        "promotion_end_hour": "PromotionEndHour",
                        "min_quantity": "MinQty",
                        "reward_type": "RewardType",
                        "discounted_price": "DiscountedPrice",
                        "min_number_of_item_offered": "MinNoOfItemOfered",
                        "promotion_items": "PromotionItems Item",
                        "additional_restrictions": "AdditionalRestrictions",
                        "club_id": "Clubs ClubId",
                    },
                },
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "4",
                "format": {
                    "file": {
                        "root": "root",
                        "entity_list": "Promotions Promotion",
                    },
                    "entity": {
                        "promotion_id": "PromotionId",
                        "promotion_description": "PromotionDescription",
                        "promotion_update_date": "PromotionUpdateDate",
                        "allow_multiple_discounts": "AllowMultipleDiscounts",
                        "promotion_start_date": "PromotionStartDate",
                        "promotion_start_hour": "PromotionStartHour",
                        "promotion_end_date": "PromotionEndDate",
                        "promotion_end_hour": "PromotionEndHour",
                        "min_quantity": "MinQty",
                        "reward_type": "RewardType",
                        "discounted_price": "DiscountedPrice",
                        "min_number_of_item_offered": "MinNoOfItemOfered",
                        "promotion_items": "PromotionItems Item",
                        "additional_restrictions": "AdditionalRestrictions",
                        "club_id": "Clubs ClubId",
                    },
                },
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "5",
                "format": {
                    "file": {
                        "root": "asx:abap asx:values",
                        "entity_list": "STORES STORE",
                    },
                    "entity": {
                        "chain_id": None,
                        "store_id": "STOREID",
                        "store_name": "STORENAME",
                        "store_type": "STORETYPE",
                        "chain": "CHAINNAME",
                        "bikoret_number": "BIKORETNO",
                        "subchain_id": "SUBCHAINID",
                        "subchain_name": "SUBCHAINNAME",
                        "city": "CITY",
                        "address": "ADDRESS",
                        "zipcode": "ZIPCODE",
                    },
                },
            },
        },
    },
    SERVER_TYPE.SuperPharm: {
        "domain": "https://prices.super-pharm.co.il",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "Price",
                "format": {
                    "file": FILE_FORMAT_SUPER_PHARM,
                    "entity": ENTITY_FORMAT_ITEM_SUPER_PHARM,
                },
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "PriceFull",
                "format": {
                    "file": FILE_FORMAT_SUPER_PHARM,
                    "entity": ENTITY_FORMAT_ITEM_SUPER_PHARM,
                },
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "Promo",
                "format": {
                    "file": FILE_FORMAT_SUPER_PHARM,
                    "entity": {
                        "promotion_id": "PromotionId",
                        "promotion_description": "PromotionDescription",
                        "promotion_update_date": "PromotionUpdateDate",
                        "allow_multiple_discounts": "AllowMultipleDiscounts",
                        "promotion_start_date": "PromotionStartDate",
                        "promotion_start_hour": "PromotionStartHour",
                        "promotion_end_date": "PromotionEndDate",
                        "promotion_end_hour": "PromotionEndHour",
                        "min_quantity": "MinQty",
                        "reward_type": "RewardType",
                        "discounted_price": "DiscountedPrice",
                        "min_number_of_item_offered": "MinNoOfItemOfered",
                        "promotion_items": "PromotionItems Item",
                        "additional_restrictions": "AdditionalRestrictions",
                        "clubs": "Clubs",
                    },
                },
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "PromoFull",
                "format": FILE_FORMAT_SUPER_PHARM,
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "StoresFull",
                "format": {
                    "file": FILE_FORMAT_SUPER_PHARM,
                    "entity": {
                        "chain_id": None,
                        "store_id": "StoreId",
                        "store_name": "StoreName",
                        "store_type": "StoreType",
                        "chain": "ChainName",
                        "bikoret_number": "BikoretNo",
                        "subchain_id": "SUBCHAINID",
                        "subchain_name": "SUBCHAINNAME",
                        "city": "City",
                        "address": "Address",
                        "zipcode": "ZipCode",
                    },
                },
            },
        },
    },
    SERVER_TYPE.Nibit: {
        "domain": "https://laibcatalog.co.il/",
        "categories": {
            FILE_CATEGORY.All: {"parameter_name": "all", "format": None},
            FILE_CATEGORY.Prices: {
                "parameter_name": "price",
                "format": {
                    "file": FILE_FORMAT_PRICES_NIBIT,
                    "entity": ENTITY_FORMAT_ITEM_NIBIT,
                },
            },
            FILE_CATEGORY.PricesFull: {
                "parameter_name": "pricefull",
                "format": {
                    "file": FILE_FORMAT_PRICES_NIBIT,
                    "entity": ENTITY_FORMAT_ITEM_NIBIT,
                },
            },
            FILE_CATEGORY.Promos: {
                "parameter_name": "promo",
                "format": {
                    "file": {
                        "root": "Promos",
                        "entity_list": "Sales Sale",
                    },
                    "entity": {
                        "promotion_id": "PromotionID",
                        "promotion_description": "PromotionDescription",
                        "promotion_update_date": "PriceUpdateDate",
                        "allow_multiple_discounts": "AllowMultipleDiscounts",
                        "promotion_start_date": "PromotionStartDate",
                        "promotion_start_hour": "PromotionStartHour",
                        "promotion_end_date": "PromotionEndDate",
                        "promotion_end_hour": "PromotionEndHour",
                        "min_quantity": "MinQty",
                        "reward_type": "RewardType",
                        "discounted_price": "DiscountedPrice",
                        "min_number_of_item_offered": "MinNoOfItemsOffered",
                        "promotion_items": "PromotionItems Item",
                        "additional_restrictions": "AdditionalRestrictions",
                        "club_id": "ClubID",
                    },
                },
            },
            FILE_CATEGORY.PromosFull: {
                "parameter_name": "promofull",
                "format": {
                    "root": "Promos",
                    "entity_list": "Sales Sale",
                    "item": "Sale",
                },
            },
            FILE_CATEGORY.Stores: {
                "parameter_name": "storesfull",
                "format": {
                    "file": {
                        "root": "Store",
                        "entity_list": "Branches Branch",
                    },
                    "entity": {
                        "chain_id": "ChainID",
                        "store_id": "StoreID",
                        "store_name": "StoreName",
                        "store_type": "StoreType",
                        "chain": "ChainName",
                        "bikoret_number": "BikoretNo",
                        "subchain_id": "SubChainID",
                        "subchain_name": "SubChainName",
                        "city": "City",
                        "address": "Address",
                        "zipcode": "ZIPCode",
                    },
                },
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
