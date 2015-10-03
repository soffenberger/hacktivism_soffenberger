DROP TABLE IF EXISTS users;

CREATE TABLE users(
	user_id		serial primary key,
	screen_name	text UNIQUE,
	follower_count	integer,
	location 	text,
	verified 	boolean
);

