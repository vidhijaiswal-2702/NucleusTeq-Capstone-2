CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	total_amount FLOAT NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_orders_id ON orders (id);
CREATE TABLE password_reset_tokens (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	token VARCHAR(255) NOT NULL, 
	expiration_time DATETIME NOT NULL, 
	used BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (token)
);
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	price FLOAT NOT NULL, 
	stock INTEGER NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	image_url VARCHAR(255) NOT NULL, 
	created_by INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE CASCADE
);
CREATE INDEX ix_products_id ON products (id);
CREATE TABLE user_tokens (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	access_key VARCHAR(250), 
	refresh_key VARCHAR(250), 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	expires_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE INDEX ix_user_tokens_access_key ON user_tokens (access_key);
CREATE INDEX ix_user_tokens_refresh_key ON user_tokens (refresh_key);
CREATE TABLE cart (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_id) REFERENCES products (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	CONSTRAINT _user_product_uc UNIQUE (user_id, product_id)
);
CREATE TABLE order_items (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	product_id INTEGER, 
	quantity INTEGER NOT NULL, 
	price_at_purchase FLOAT NOT NULL, product_name VARCHAR, product_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE SET NULL
);
CREATE INDEX ix_order_items_id ON order_items (id);
CREATE TABLE IF NOT EXISTS "users" (
	id INTEGER NOT NULL, 
	name VARCHAR(150), 
	email VARCHAR(255) NOT NULL, 
	password VARCHAR(100), 
	role VARCHAR(50) NOT NULL, 
	is_active BOOLEAN, 
	verified_at DATETIME, 
	updated_at DATETIME, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);
