CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

CREATE TABLE ingredients (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE selected_ingredients (id INTEGER PRIMARY KEY, selected TEXT);

INSERT INTO ingredients (name) VALUES ('milk'), ('eggs'), ('bread'), ('juice'), ('apple'), ('banana');

