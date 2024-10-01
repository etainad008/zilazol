CREATE TYPE STORE_TYPE AS ENUM ('physical', 'online', 'physical_and_online');
CREATE TYPE UNIT AS ENUM (
    'unit',
    'milligram',
    'gram',
    'kilogram',
    'milliliter',
    'liter',
    'millimeter',
    'centimeter',
    'meter'
);

CREATE TABLE IF NOT EXISTS Chain (
    id CHAR(13) PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Subchain (
    id VARCHAR(8) NOT NULL,
    chain_id VARCHAR(16) NOT NULL,
    name VARCHAR(64) NOT NULL,

    PRIMARY KEY (id, chain_id),
    FOREIGN KEY (chain_id) REFERENCES Chain(id)
);

CREATE TABLE IF NOT EXISTS Store (
    id VARCHAR(4) NOT NULL,
    chain_id VARCHAR(16) NOT NULL,
    subchain_id VARCHAR(8) NOT NULL,
    bikoret_number CHAR(1) NOT NULL,
    type STORE_TYPE NOT NULL,
    name VARCHAR(64) NOT NULL,
    address VARCHAR(64),
    city VARCHAR(32),
    zip_code CHAR(7),

    PRIMARY KEY (id, chain_id, subchain_id),
    FOREIGN KEY (subchain_id, chain_id) REFERENCES Subchain(id, chain_id)
);

CREATE TABLE IF NOT EXISTS Item (
    code VARCHAR(16) PRIMARY KEY,
    type CHAR(1) NOT NULL,
    name TEXT NOT NULL,
    manufacturer_name VARCHAR(32),
    manufacture_country VARCHAR(32),
    manufacturer_item_description TEXT,
    unit_quantity UNIT NOT NULL,
    quantity INT NOT NULL,
    is_weighted BOOLEAN NOT NULL,
    quantity_in_package INT
);

CREATE TABLE IF NOT EXISTS Item_Instance (
	code VARCHAR(16) NOT NULL,
	store_id VARCHAR(4) NOT NULL,
    chain_id VARCHAR(16) NOT NULL,
    subchain_id VARCHAR(8) NOT NULL,
	price INT NOT NULL,
	allow_discount BOOLEAN NOT NULL,

	PRIMARY KEY (code, store_id, chain_id, subchain_id),
	FOREIGN KEY (code) REFERENCES Item(code),
	FOREIGN KEY (store_id, chain_id, subchain_id) REFERENCES Store(id, chain_id, subchain_id)
);
