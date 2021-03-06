-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABle player (
	ID SERIAL PRIMARY KEY,
	name TEXT,
	wins INT, 
	matches INT
);

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	player1_id INT REFERENCES player(ID),
	player2_id INT REFERENCES player(ID)
);
