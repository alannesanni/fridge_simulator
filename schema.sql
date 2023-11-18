CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

CREATE TABLE ingredients (id SERIAL PRIMARY KEY, name TEXT, place TEXT);

CREATE TABLE selected_ingredients (id INTEGER PRIMARY KEY, selected TEXT);


