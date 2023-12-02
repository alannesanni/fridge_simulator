CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, role TEXT);

CREATE TABLE ingredients (id SERIAL PRIMARY KEY, name TEXT, place TEXT);

CREATE TABLE recipes (id SERIAL PRIMARY KEY, name TEXT, ingredient_ids TEXT, instructions TEXT);

CREATE TABLE selected_ingredients (id INTEGER PRIMARY KEY, selected TEXT);

CREATE TABLE liked_recipes (id SERIAL PRIMARY KEY, user_id INTEGER, recipe_id INTEGER)


