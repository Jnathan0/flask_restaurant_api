PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users"
(
user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
email NVARCHAR(256) NOT NULL,
hash_pass NVARCHAR(2048) NOT NULL,
first_name NVARCHAR(256) NOT NULL,
last_name NVARCHAR(256),
user_address NVARCHAR(256) NOT NULL,
user_city NVARCHAR(128) NOT NULL,
user_zip NVARCHAR(12) NOT NULL,
user_state NVARCHAR(12) NOT NULL,
user_phone INTEGER(10) NOT NULL
);
INSERT INTO users (user_id, email, hash_pass, first_name, last_name, user_address, user_city, user_zip, user_state, user_phone) VALUES(1, "test@test.com", "sha256$ft0nijwz$ebc0a2e5ad9c76cd981d0fcad6a4d1d9d888585e0603c634d10ab254d952b336", "test", "user", "27 Edinger Ave", "Santa Ana", 92707, "CA", 17145556867);
INSERT INTO users (user_id, email, hash_pass, first_name, last_name, user_address, user_city, user_zip, user_state, user_phone) VALUES(2, "test2@test.com", "sha256$ft0nijwz$ebc0a2e5ad9c76cd981d0fcad6a4d1d9d888585e0603c634d10ab254d952b336", "test2", "user", "11 foo way", "Irvine", 92620, "CA", 19495558934);
CREATE TABLE IF NOT EXISTS "restaurants"
(
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_name TEXT,
    restaurant_address TEXT,
    restaurant_description TEXT,
    restaurant_city TEXT,
    restaurant_zip INTEGER,
    restaurant_state TEXT,
    restaurant_phone INTEGER,
    restaurant_hours TEXT,
    latitude FLOAT,
    longitude FLOAT,
    delivery BOOLEAN,
    pickup BOOLEAN
);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(1, "Burntzilla", "14413 Culver Dr", "Small plates and barbeque, specializing in sliders", "Irvine", 92606, "CA", 19493925995, "11am-7pm", 33.706, -117.787, False, True);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(2, "Native Foods", "2937 Bristol St e100", "Chain for creative, Californian-style vegan fare, including mock-meat dishes, ordered at a counter.", "Costa Mesa", 92626, "CA", 17147512151, "11am-9pm", 33.678, -117.886, False, True);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(3, "Domino's Pizza", "3902 E Chapman Ave", "Franchise pizza chain specializing in quick, made to order pizzas.", "Orange", 92869, "CA", 17145388881, "10am-1am", 33.787, -117.812, True, True);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(4, "TK Burgers", "24902 Chrisanta Dr", "Mom and pop american burger joint specializing in all the classics", "Mission Viejo", 92691, "CA", 19495887200, "7am-9pm", 33.601, -117.672, False, True);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(5, "Taqueria El Zamorano", "925 W Warner Ave", "Counter-serve Mexican resaurant offering a traditional menu in a warm, low-key atmosphere", "Santa Ana", 92707, "CA", 17148844073, "9am-8pm", 33.716, -117.877, False, True);
INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, restaurant_description, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, restaurant_hours, latitude, longitude, delivery, pickup) VALUES(6, "Starbucks", "14456 Culver Dr", "Chain coffee retailer that offers seasonal beverages and pasteries.", "Irvine", 92606, "CA", 19495557879, "11am-10pm", 33.704, -117.720, False, True);

CREATE TABLE IF NOT EXISTS "products"
(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    product_description TEXT NOT NULL,
    image_path TEXT,
    stock INT NOT NULL,
    restaurant_id INTEGER NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES "restaurants" (restaurant_id) ON DELETE CASCADE
);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(1, "Grilled Pork Sliders", 8.99, "Three grilled pork belly sliders topped with american cheese and grilled onions.", 19, 1);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(2, "Large Fries", 5.99, "Thick cut steak fries with organic sea salt.", 2, 1);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(3, "Organic Ahi Tuna Salad", 22.99, "Seven slices of grilled ahi tuna ontop a bed of leafy greens.", 0, 2);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(4, "Large Garlic Chicken Pizza", 12.99, "Garlic Chicken with white sauce on New York thin crust.", 100, 3);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(5, "Avocado Bacon Burger", 6.99, "American beef patty with cheese, avocado and bacon", 20, 4);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(6, "Fried Zucchini", 3.99, "Breaded zucchini with garlic seasoning", 12, 4);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(7, "Tacos El Pastor", 7.99, "Two tacos with onion and cabbage", 9, 5);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(8, "California Burrito", 10.99, "Pork burrito with secret sauce and french fries", 23, 5);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(9, "Venti Holiday Latte", 7.99, "Allspice and vanilla with creamy foam and topped with peppermine whipped cream.", 23, 6 );
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(10, "Tall Drip Coffee", 2.99, "House Dark roast", 20, 6);
INSERT INTO products (product_id, product_name, product_price, product_description, stock, restaurant_id) VALUES(11, "Lemon Scone", 6.99, "Lemon zested dense pastery topped with vanilla icing", 2, 6);



CREATE TABLE IF NOT EXISTS "cart"
(
    user_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES "users" (user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES "products" (product_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orders"
(
    user_id INTEGER,
    product_id INTEGER,
    created_at TEXT,
    FOREIGN KEY (user_id) REFERENCES "users" (user_id),
    FOREIGN KEY (product_id) REFERENCES "products" (product_id)
);
COMMIT;
